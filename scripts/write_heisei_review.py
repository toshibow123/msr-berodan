#!/usr/bin/env python3
"""
平成AVレビュー記事生成スクリプト
旧作・名作AVをURL指定で取得し、Gemini APIで記事を生成する
"""

import os
import json
import sys
import time
import re
import random
from datetime import datetime
from pathlib import Path
import google.generativeai as genai
import urllib.request
import urllib.error
import ssl
from urllib.parse import urlencode, parse_qs, urlparse


def initialize_gemini(api_key: str):
    """Gemini APIを初期化"""
    genai.configure(api_key=api_key)


def extract_content_id_from_url(url: str) -> str | None:
    """
    URLから品番（content_id）を抽出（アフィリエイトリンク対応版）
    
    例1 (通常): https://www.dmm.co.jp/digital/videoa/-/detail/=/cid=abc123/
    → abc123
    
    例2 (アフィリエイト): https://al.dmm.co.jp/?lurl=https%3A%2F%2Fwww.dmm.co.jp%2F...
    → lurlをデコードしてから品番を抽出
    
    例3 (動画配信): https://video.dmm.co.jp/digital/videoa/-/detail/=/id=abc123/
    → abc123
    """
    from urllib.parse import urlparse, parse_qs, unquote
    
    # アフィリエイトリンクの場合、実URLを取り出す
    if "al.fanza.co.jp" in url or "al.dmm.co.jp" in url:
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        if 'lurl' in qs:
            url = unquote(qs['lurl'][0])
            print(f"🔍 アフィリエイトリンクを検出: 実URLに変換しました")
    
    # 正規表現で品番を抽出（複数パターン対応）
    patterns = [
        r'cid=([a-z0-9_]+)',        # 通常のDMM: /cid=abc123/
        r'id=([a-z0-9_]+)',          # 動画配信: /id=abc123/
        r'/detail/=/cid=([a-z0-9_]+)', # パス埋め込み形式
        r'content_id=([a-z0-9_]+)',  # クエリパラメータ形式
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return None


def fetch_dmm_product_info(api_id: str, affiliate_id: str, content_id: str) -> dict | None:
    """
    DMM APIから商品情報を取得
    
    Args:
        api_id: DMM API ID
        affiliate_id: アフィリエイトID
        content_id: 品番
        
    Returns:
        商品情報の辞書、または None
    """
    base_url = "https://api.dmm.com/affiliate/v3/ItemList"
    
    params = {
        "api_id": api_id,
        "affiliate_id": affiliate_id,
        "site": "FANZA",
        "service": "digital",
        "floor": "videoa",
        "cid": content_id,
        "hits": 1,
        "output": "json"
    }
    
    url = f"{base_url}?{urlencode(params)}"
    
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=context, timeout=30) as response:
            data = response.read()
            result = json.loads(data.decode('utf-8'))
            
            if "result" in result and "items" in result["result"] and len(result["result"]["items"]) > 0:
                item = result["result"]["items"][0]
                
                return {
                    "content_id": item.get("content_id", content_id),
                    "title": item.get("title", ""),
                    "url": item.get("URL", ""),
                    "affiliate_url": item.get("affiliateURL", ""),
                    "image_url": item.get("imageURL", {}).get("large", ""),
                    "price": item.get("prices", {}).get("price", ""),
                    "release_date": item.get("date", ""),
                    "actress": [actress.get("name", "") for actress in item.get("iteminfo", {}).get("actress", [])],
                    "genre": [genre.get("name", "") for genre in item.get("iteminfo", {}).get("genre", [])],
                    "maker": item.get("iteminfo", {}).get("maker", [{}])[0].get("name", "") if item.get("iteminfo", {}).get("maker") else "",
                    "director": item.get("iteminfo", {}).get("director", [{}])[0].get("name", "") if item.get("iteminfo", {}).get("director") else "",
                    "description": item.get("review", {}).get("text", "") if item.get("review") else "",
                }
            else:
                return None
                
    except Exception as e:
        print(f"❌ API取得エラー: {e}", file=sys.stderr)
        return None


def get_random_angle() -> dict:
    """
    ランダムな記事の切り口（Angle）を選択
    
    Returns:
        選択された切り口の辞書（name: 切り口名, description: 詳細説明）
    """
    angles = [
        {
            "name": "女優礼賛",
            "description": """企画よりも、女優の表情、演技、可愛さに徹底的にフォーカスして褒めちぎる視点。
- 女優の一挙手一投足、表情の変化、声のトーンなど、細部まで観察して称賛する
- 「この女優だからこそ成立する企画」という視点で、女優の魅力を最大限に引き出す
- 現代の女優との比較ではなく、この女優の「唯一無二の魅力」を語る"""
        },
        {
            "name": "実用性重視",
            "description": """抜けるか抜けないか、エロいかエロくないかという直感と本能に従った、「男友達への報告」のような視点。
- 「正直に言うと、これは抜ける」「これは微妙だった」という率直な感想
- シーンごとの「実用度」を具体的に評価（「このシーンは何度も見返した」など）
- テクニックや演出よりも、「気持ちよさ」や「興奮度」を最優先で語る"""
        },
        {
            "name": "マニアック解説",
            "description": """監督の演出や、メーカーの特色、シチュエーションの細かすぎるこだわりを分析するオタク視点。
- 監督の演出意図や、カメラワークの工夫を読み解く
- メーカーの特徴や、シリーズ物なら他の作品との関連性を指摘
- シチュエーション設定の細かい部分（小道具、服装、セリフなど）に注目して解説"""
        },
        {
            "name": "物語・世界観",
            "description": """「なぜそうなった？」というストーリーの不条理さや設定の面白さにツッコミを入れつつ楽しむ視点。
- ストーリーの展開や、シチュエーション設定の「おかしさ」を楽しむ
- 「この設定、意味ある？」「なんでこうなった？」というツッコミを入れつつ、それが逆に面白いと評価
- 世界観の一貫性や、キャラクター設定の妙を語る"""
        },
        {
            "name": "熱量と狂気",
            "description": """コンプラ云々という冷静な分析ではなく、当時の現場の「熱気」や「勢い」に圧倒されたというテンション高い視点。
- 作品全体から感じられる「熱量」や「勢い」を語る
- 企画の「狂気」や「過激さ」を、批判ではなく「すごい！」という驚きとリスペクトで語る
- 当時の制作現場の「覚悟」や「本気度」を感じさせる表現を重視"""
        }
    ]
    
    return random.choice(angles)


def get_negative_constraints() -> list:
    """
    禁止ワード（Negative Constraints）のリストを返す
    
    Returns:
        禁止ワードのリスト
    """
    return [
        "「現代では絶対に作れない」という表現",
        "「コンプライアンス」への言及",
        "「昭和/平成の遺産」という表現",
        "「概要」「まとめ」「あらすじ」という平凡な見出し（もっとフックのある見出しを使う）"
    ]


def load_example_article(content_dir: Path) -> str | None:
    """
    既存の記事からサンプルを読み込む（Frontmatterを除いた本文のみ）
    
    Args:
        content_dir: contentディレクトリのパス
        
    Returns:
        サンプル記事の本文（Frontmatterを除く）、またはNone
    """
    if not content_dir.exists():
        return None
    
    # サンプル記事の候補（良い記事を優先）
    sample_files = [
        "2025-12-28-h_094ktds00458.md",
        "2025-12-28-mukd00086.md",
        "2025-12-28-ircp00027.md",
    ]
    
    for filename in sample_files:
        filepath = content_dir / filename
        if filepath.exists():
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Frontmatterを除去（---で囲まれた部分）
                if content.startswith("---"):
                    # 最初の---から次の---までをスキップ
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        body = parts[2].strip()
                        if body:
                            print(f"📚 サンプル記事を読み込みました: {filename}")
                            return body
            except Exception as e:
                print(f"⚠️  サンプル記事の読み込みに失敗: {filename} - {e}")
                continue
    
    return None


def create_prompt(product_info: dict, description: str = "", example_article: str | None = None) -> str:
    """
    平成AV名作レビュー記事のプロンプトを作成
    
    Args:
        product_info: 商品情報
        description: 商品説明
        example_article: 既存の記事サンプル（本文のみ、Frontmatterなし）
    """
    title = product_info.get("title", "")
    content_id = product_info.get("content_id", "")
    image_url = product_info.get("image_url", "")
    affiliate_url = product_info.get("affiliate_url", "")
    actress_list = product_info.get("actress", [])
    genre_list = product_info.get("genre", [])
    maker = product_info.get("maker", "")
    director = product_info.get("director", "")
    release_date = product_info.get("release_date", "")
    
    actresses = "、".join(actress_list) if actress_list else "不明"
    genres = "、".join(genre_list) if genre_list else "不明"
    
    # 発売年を抽出
    year = ""
    if release_date:
        try:
            year = release_date.split("-")[0]
        except:
            pass
    
    # ランダムな切り口を選択
    selected_angle = get_random_angle()
    negative_constraints = get_negative_constraints()
    
    print(f"📌 今回の記事の切り口: {selected_angle['name']}")
    
    # 禁止ワードのリストを文字列に変換
    negative_constraints_text = "\n".join([f"- {constraint}" for constraint in negative_constraints])
    
    # 第一印象セクションの見出しをランダムに選択
    first_impression_headings = [
        "見始めた瞬間に完全にやられたわｗ",
        "冒頭からマジで期待値ブチ上げだったわｗ",
        "最初の数秒で完全にハマったわｗ",
        "タイトル見た瞬間、これヤバいって確信したわｗ",
        "画面に映った瞬間、もう完全にやられたわｗ",
        "見始めた瞬間に「ああ、これは伝説だわ」って確信したわｗ",
        "冒頭からマジで興奮が止まらなかったわｗ",
        "最初のシーンで完全に引き込まれたわｗ",
        "始まった瞬間の「キタコレｗ」感"
    ]
    selected_heading = random.choice(first_impression_headings)
    
    # サンプル記事のセクション（あれば追加）
    example_section = ""
    if example_article:
        example_section = f"""
# 参考例（既存の記事サンプル）
以下の記事を参考にして、同じスタイル・トーンで書いてください：

{example_article}

---
"""
    
    prompt = f"""# Role
あなたはAVの熱狂的なファンです。
深夜に最高の一本を見つけて、興奮のままに掲示板やSNSで語り散らかしている「一人の視聴者」として書いてください。

{example_section}

# スタイル指針
- スペック（画角、解像度、制作年）などの説明は一切不要。そんなの誰も見てないｗ
- 丁寧語、ライター気取りのきれいな言葉は全部ゴミ箱へ。
- 「ｗ」や「マジで」「ヤバい」を多用して、リアルな興奮を表現する。
- 語尾は「〜だわ」「〜すぎるｗ」「マジで抜ける」などの完全タメ口。

# 執筆ルール
1. **シーンの描写**: 
   作品に含まれるシーンを具体的に描写してください。変な比喩はいりません。
   あらすじから読み取れるシーンを中心に書いてください。
2. **シーンに食いつく**: 
   「ここがエロかったｗ」というポイントだけを熱量100%で書く。
3. **主観のみで語る**: 
   「俺はこのシーンで昇天したｗ」的な、個人的な感想を最優先。

# 作品情報
**あらすじ・商品説明:**
{description if description else "（情報なし）"}

上記のあらすじをもとに、作品の内容を推測して記事を書いてください。

# 記事の構成
以下の構成で、Markdown本文のみを出力してください（Frontmatterは不要）：

## [感情が漏れ出してるような一言タイトル]
（「キタコレｗ」「マジでヤバい」「これ見てないやつは損してる」みたいな、興奮が溢れ出てる感じのタイトル）

{f'（{year}年の作品だけど、今見てもマジで抜けるｗ）' if year else ''}

## {title}
<a href="{affiliate_url}" target="_blank" rel="sponsored noopener noreferrer">
  <img src="{image_url}" alt="{title}" />
</a>

**重要**: 必ず上記の画像タグとアフィリエイトリンクを**そのまま**記事に含めてください。画像URLやリンクを変更しないでください。

**出演:** {actresses}
**ジャンル:** {genres}
**メーカー:** {maker}
{f'**監督:** {director}' if director else ''}
{f'**発売:** {year}年' if year else ''}

<div className="affiliate-link-inline">
  <a href="{affiliate_url}" target="_blank" rel="noopener noreferrer">サンプル動画を見る</a>
</div>

## {selected_heading}
（作品を見始めた瞬間の第一印象を、興奮のままに書く）
（「これヤバいｗ」「マジで期待してたけど超えてきた」みたいな感じ）
（女優の見た目、雰囲気、最初のシーンの印象など、主観100%で）

## ここがエロかったｗ（シーン別に熱量100%で）
（具体的なシーンをストレートに描写してください）
（「このシーンでマジで昇天したｗ」「ここが抜きポイントだわ」みたいな感じ）
（選択された視点（{selected_angle['name']}）に基づいて、特に食いついたポイントを書く）
（メーカーの傾向（{maker}ならドキュメンタリー風など）から推測して、現場の熱量を感じさせる描写を加える）
（あらすじから読み取れる内容を中心に、自然なシーンを想像して書いてください）

**重要**: シーンを説明した後、必ず以下の形式でサンプル画像を4〜5枚挿入してください：
<a href="{affiliate_url}" target="_blank" rel="sponsored noopener noreferrer">
  <img src="https://pics.dmm.co.jp/digital/video/{content_id}/{content_id}jp-1.jpg" alt="{title}" />
</a>
<a href="{affiliate_url}" target="_blank" rel="sponsored noopener noreferrer">
  <img src="https://pics.dmm.co.jp/digital/video/{content_id}/{content_id}jp-2.jpg" alt="{title}" />
</a>
<a href="{affiliate_url}" target="_blank" rel="sponsored noopener noreferrer">
  <img src="https://pics.dmm.co.jp/digital/video/{content_id}/{content_id}jp-3.jpg" alt="{title}" />
</a>
<a href="{affiliate_url}" target="_blank" rel="sponsored noopener noreferrer">
  <img src="https://pics.dmm.co.jp/digital/video/{content_id}/{content_id}jp-4.jpg" alt="{title}" />
</a>
<a href="{affiliate_url}" target="_blank" rel="sponsored noopener noreferrer">
  <img src="https://pics.dmm.co.jp/digital/video/{content_id}/{content_id}jp-5.jpg" alt="{title}" />
</a>

画像は各シーンの説明の後に適切に配置してください。シーンごとに1〜2枚の画像を配置するのが理想的です。

<div className="affiliate-link-inline">
  <a href="{affiliate_url}" target="_blank" rel="noopener noreferrer">この名作を確認する</a>
</div>

## コスパ重視の視聴アドバイス
（以下の条件に該当する場合のみ、このセクションを追加してください）
- 紹介する作品が「準新作」〜「旧作」である場合（発売から1年以上経過している場合）
- または、名作・シリーズ物である場合

**【文章の構成】**
1. **価格への言及（損得勘定を刺激）:**
   「正直、この年代の作品を定価で買うのはアホだわｗ」
   「内容はマジでお墨付きだけど、お財布が痛むｗ」

2. **サブスクの提案（解決策として自然に誘導）:**
   「DMM TV（またはFANZA見放題）の会員なら、追加料金なしで見放題だわｗ」
   「まだ会員じゃないなら、**無料体験**でタダ見するのが最強だわｗ」
   「匿名性も完璧だし、誰にもバレないから安心して見れるｗ」

3. **強烈なひと押し:**
   「浮いた金でローション買った方がマシだわｗ」
   「ランチ1回分で、この時代の名作が数万本見放題ってマジでヤバい時代だわｗ」

## 今すぐ見てこいｗ（ゴリ押しの結び）
（「マジで見てないやつは損してる」「これ見ずに語れない」みたいな、熱量100%のゴリ押し）
（「500円だろうが定価だろうが、これは持っておくべき一本だわ」と強く推す）
（匿名性や背徳感に触れる結び。「今すぐ見ろ」という確信を読者に植え付ける）

<div className="affiliate-link">
  <a href="{affiliate_url}" target="_blank" rel="noopener noreferrer">今すぐチェックする</a>
</div>

**作品情報:**
- タイトル: {title}
- 品番: {content_id}
- 出演: {actresses}
- ジャンル: {genres}
- メーカー: {maker}
{f'- 発売: {year}年' if year else ''}

**注意事項:**
- Frontmatter（---で囲まれたメタデータ）は含めず、Markdown本文のみを出力してください。
- アフィリエイトリンクは、上記の3箇所に必ず配置してください。
- 完全タメ口で、熱量100%の文章で書いてください。
- 「ｗ」「マジで」「ヤバい」などのカジュアルな表現を多用してください。
- スペック（画角、解像度など）の説明は一切不要です。
- シーンは具体的に、ストレートに描写してください。
- 主観的な感想を最優先に書いてください。

**【文字数・品質要件】**
- **最低2,000文字以上**の記事を書いてください。読み応えのある、充実した内容にしてください。
- 各セクションを丁寧に展開し、具体例や詳細な描写を含めてください。
- 短すぎる文章や、表面的な内容は避けてください。

**【関連性の言及】**
- 可能であれば、同じ女優の他の作品や、同じ年代の名作との関連性を言及してください。
- 「この女優の他の作品」「同じ時期の名作」など、読者が他の作品にも興味を持てるような記述を入れてください。
- ただし、無理に関連性を作り出す必要はありません。自然な流れで言及できる場合のみで構いません。
"""
    
    return prompt


def generate_article(model: genai.GenerativeModel, product_info: dict, description: str = "", example_article: str | None = None) -> str | None:
    """Gemini APIを使って記事本文を生成"""
    prompt = create_prompt(product_info, description, example_article)
    
    try:
        response = model.generate_content(prompt)
        
        if not response.candidates:
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                print(f"❌ 記事生成に失敗: コンテンツがブロックされました。理由: {response.prompt_feedback.block_reason}", file=sys.stderr)
            else:
                print(f"❌ 記事生成に失敗: レスポンス候補がありません。", file=sys.stderr)
            return None
        
        return response.text
    except Exception as e:
        print(f"❌ 記事生成に失敗: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return None


def insert_video_player(content: str, video_cid: str) -> str:
    """
    記事本文に動画プレーヤーを挿入
    
    Args:
        content: 記事本文（Markdown/HTML）
        video_cid: 動画のCID
        
    Returns:
        動画プレーヤーが挿入された記事本文
    """
    video_script = f'<div style="width:100%; padding-top: 75%; position:relative; margin: 2rem 0;"><iframe width="100%" height="100%" max-width="1280px" style="position: absolute; top: 0; left: 0;" src="https://www.dmm.co.jp/litevideo/-/part/=/affi_id=toshichan-002/cid={video_cid}/size=1280_720/" scrolling="no" frameborder="0" allowfullscreen></iframe></div>'
    
    # サンプル動画ボタンの直後に挿入
    sample_patterns = [
        r'(<a[^>]*>.*?サンプル動画.*?</a>\s*</div>)',
        r'(<div[^>]*className="affiliate-link-inline"[^>]*>.*?サンプル動画.*?</div>)',
    ]
    
    inserted = False
    for pattern in sample_patterns:
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        if match:
            # マッチした位置の直後に挿入
            insert_pos = match.end()
            content = content[:insert_pos] + '\n\n' + video_script + '\n\n' + content[insert_pos:]
            inserted = True
            print(f"✅ 動画プレーヤーを「サンプル動画」の直後に挿入しました")
            break
    
    # 挿入できなかった場合は、画像の直後に挿入
    if not inserted:
        image_pattern = r'(</a>\s*\n\s*\n\s*\*\*出演:\*\*)'
        match = re.search(image_pattern, content, re.IGNORECASE | re.DOTALL)
        if match:
            insert_pos = match.start()
            content = content[:insert_pos] + '\n\n' + video_script + '\n\n' + content[insert_pos:]
            inserted = True
            print(f"✅ 動画プレーヤーを画像の直後に挿入しました")
    
    if not inserted:
        print(f"⚠️  動画プレーヤーの適切な挿入位置が見つかりませんでした")
    
    return content


def save_article(content: str, product_info: dict, publish_date: str, output_dir: str, content_id: str) -> str | None:
    """記事をMarkdownファイルとして保存"""
    title = product_info.get("title", "")
    image_url = product_info.get("image_url", "")
    affiliate_url = product_info.get("affiliate_url", "")
    actress_list = product_info.get("actress", [])
    genre_list = product_info.get("genre", [])
    release_date = product_info.get("release_date", "")
    maker = product_info.get("maker", "")
    director = product_info.get("director", "")
    
    # 発売年を抽出
    year = ""
    if release_date:
        try:
            year = release_date.split("-")[0]
        except:
            pass
    
    # タグの作成（5〜8個程度に制限）
    tags = []
    
    # 必須タグ
    if year:
        tags.append(f'"{year}年"')
    tags.append('"平成の名作"')
    
    # 女優タグ（最大2人まで）
    if actress_list:
        tags.extend([f'"{actress}"' for actress in actress_list[:2]])
    
    # ジャンルタグ（最大2つまで）
    if genre_list:
        tags.extend([f'"{genre}"' for genre in genre_list[:2]])
    
    # メーカータグ（あれば追加）
    if maker:
        tags.append(f'"{maker}"')
    
    # 監督タグ（あれば追加）
    if director:
        tags.append(f'"{director}"')
    
    # タグ数を5〜8個に調整
    if len(tags) < 5:
        # タグが少ない場合は、ジャンルを追加
        remaining = 5 - len(tags)
        if genre_list and len(genre_list) > 2:
            tags.extend([f'"{genre}"' for genre in genre_list[2:2+remaining]])
    
    # 8個を超える場合は優先順位で削減
    if len(tags) > 8:
        # 優先順位: 年代 > 平成の名作 > 女優 > ジャンル > メーカー > 監督
        priority_order = []
        if year:
            priority_order.append(f'"{year}年"')
        priority_order.append('"平成の名作"')
        if actress_list:
            priority_order.extend([f'"{actress}"' for actress in actress_list[:2]])
        if genre_list:
            priority_order.extend([f'"{genre}"' for genre in genre_list[:2]])
        if maker:
            priority_order.append(f'"{maker}"')
        if director:
            priority_order.append(f'"{director}"')
        
        tags = priority_order[:8]
    
    tags_str = ", ".join(tags)
    
    # タグ数の確認（デバッグ用）
    print(f"📌 生成されたタグ数: {len(tags)}個")
    
    # 抜粋を生成
    excerpt = f"{title}の熱いレビュー。平成時代の名作を再評価する。"
    
    # 評価を生成（4.0-5.0のランダム、小数点第1位まで）
    rating = round(random.uniform(4.0, 5.0), 1)
    
    # Frontmatterを作成
    frontmatter = f"""---
title: "{title} ー 平成の名作を語る"
date: "{publish_date}"
excerpt: "{excerpt}"
image: "{image_url}"
tags: [{tags_str}]
affiliateLink: "{affiliate_url}"
contentId: "{content_id}"
rating: {rating}
---

"""
    
    # ファイル名を作成
    filename = f"{publish_date}-{content_id}.md"
    filepath = os.path.join(output_dir, filename)
    
    # 動画プレーヤーを自動的に挿入
    content = insert_video_player(content, content_id)
    
    # 記事全体を作成
    full_content = frontmatter + content
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(full_content)
        return filepath
    except IOError as e:
        print(f"❌ ファイルの保存に失敗: {e}", file=sys.stderr)
        return None


def main():
    """メイン処理"""
    print("\n" + "🎬" * 40)
    print("  平成AV名作レビュー記事生成ツール")
    print("🎬" * 40 + "\n")
    
    # 環境変数からAPIキーを取得
    api_key = os.environ.get("GEMINI_API_KEY")
    dmm_api_id = os.environ.get("DMM_API_ID")
    dmm_affiliate_id = os.environ.get("DMM_AFFILIATE_ID")
    
    if not api_key:
        print("❌ 環境変数 GEMINI_API_KEY が設定されていません", file=sys.stderr)
        sys.exit(1)
    
    if not dmm_api_id or not dmm_affiliate_id:
        print("❌ 環境変数 DMM_API_ID または DMM_AFFILIATE_ID が設定されていません", file=sys.stderr)
        sys.exit(1)
    
    # プロジェクトルートのパスを取得
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # 出力ディレクトリを作成
    content_dir = project_root / "content"
    content_dir.mkdir(exist_ok=True)
    
    # URL入力
    print("レビューしたい作品のURLを入力してください（FANZAの商品ページ）:")
    url = input("URL: ").strip()
    
    if not url:
        print("❌ URLが入力されていません")
        sys.exit(1)
    
    # URLから品番を抽出
    print("\n🔍 URLから品番を抽出中...")
    content_id = extract_content_id_from_url(url)
    
    if not content_id:
        print("\n❌ URLから品番を抽出できませんでした", file=sys.stderr)
        print("", file=sys.stderr)
        print("📌 対応しているURL形式:", file=sys.stderr)
        print("  • FANZA/DMM通常URL: https://www.dmm.co.jp/digital/videoa/-/detail/=/cid=abc123/", file=sys.stderr)
        print("  • 動画配信URL: https://video.dmm.co.jp/digital/videoa/-/detail/=/id=abc123/", file=sys.stderr)
        print("  • アフィリエイトリンク: https://al.dmm.co.jp/?lurl=...", file=sys.stderr)
        print("", file=sys.stderr)
        print("💡 ヒント: FANZAの商品ページから直接URLをコピーしてください", file=sys.stderr)
        sys.exit(1)
    
    print(f"✅ 品番: {content_id}")
    
    # DMM APIから商品情報を取得
    print("📡 DMM APIから商品情報を取得中...")
    product_info = fetch_dmm_product_info(dmm_api_id, dmm_affiliate_id, content_id)
    
    if not product_info:
        print("❌ 商品情報の取得に失敗しました")
        sys.exit(1)
    
    print(f"✅ タイトル: {product_info.get('title', '')}")
    print(f"   出演: {', '.join(product_info.get('actress', []))}")
    
    # 公開日の設定
    publish_date_input = input("\n公開日（YYYY-MM-DD、空白で今日）: ").strip()
    if publish_date_input:
        publish_date = publish_date_input
    else:
        publish_date = datetime.now().strftime("%Y-%m-%d")
    
    print(f"\n📅 公開日: {publish_date}")
    
    # Gemini APIを初期化
    print("🤖 Gemini APIを初期化中...")
    initialize_gemini(api_key)
    
    # Gemini 2.5 Flashを使用
    model_name = "gemini-2.5-flash"
    print(f"✅ {model_name} を使用します")
    model = genai.GenerativeModel(model_name)
    
    # 既存の記事サンプルを読み込む
    example_article = load_example_article(content_dir)
    
    # 記事を生成
    print("\n✍️  記事生成中...")
    article_content = generate_article(model, product_info, description=product_info.get("description", ""), example_article=example_article)
    
    if article_content:
        # 記事を保存（content_idを渡す）
        filepath = save_article(article_content, product_info, publish_date, str(content_dir), content_id)
        
        if filepath:
            print(f"\n✅ 記事を保存しました: {filepath}")
            print("\n" + "=" * 80)
            print("🎉 記事生成完了！")
            print("=" * 80)
        else:
            print("\n❌ 保存失敗")
            sys.exit(1)
    else:
        print("\n❌ 生成失敗")
        sys.exit(1)


if __name__ == "__main__":
    main()

