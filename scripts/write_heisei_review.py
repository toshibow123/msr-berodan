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


def create_prompt(product_info: dict) -> str:
    """
    平成AV名作レビュー記事のプロンプトを作成
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
    
    prompt = f"""あなたは「ビデオ黄金時代を知る愛好家」です。
以下の旧作・名作AVについて、熱のこもったレビュー記事を書いてください。

**【今回の記事のテーマ・視点】**
この記事は、以下の視点を最優先して書いてください：

【{selected_angle['name']}】
{selected_angle['description']}

この視点を軸に、作品の魅力を語ってください。他の視点も補助的に使っても構いませんが、上記の視点を主軸として記事を構成してください。

**【禁止事項】**
以下の表現や考え方は、陳腐になるため絶対に使用しないでください：
{negative_constraints_text}

特に注意：
- 「現代では絶対に作れない」という表現は使わず、もっと具体的で独自の表現を考えてください。
- 「コンプライアンス」という言葉は一切使わず、別の表現で置き換えてください。
- 見出しは「概要」「まとめ」「あらすじ」のような平凡なものではなく、読者の興味を引く、フックのある見出しにしてください。

**【執筆ルール：名作の語り部】**

**1. 基本スタンス**
- 口調は「〜だ」「〜である」という落ち着いた常体、あるいは「〜なんですよ」という熱っぽい語り口。
- 上記の「今回の記事のテーマ・視点」を最優先に、その視点から作品を語ってください。

**2. 描写のポイント**
- **「画質の古さ」をポジティブに変換する。**
  - 画質が粗い・4:3比率であっても、「それが逆に生々しい」「ドキュメント感がある」と表現する。
  - 例：「SD画質の荒い粒子が、逆に生々しさを際立たせている。」
- **「女優の覚悟」を称賛する。**
  - 当時の女優の体当たりな演技や、表情の作り込みを「プロ根性」としてリスペクトする。
  - 例：「この表情の作り込み、今の女優では絶対に出せない。」

**3. 記事の構成**
以下の構成で、Markdown本文のみを出力してください（Frontmatterは不要）：

## [独自のフックのある見出し]
（再発見の感動から入る。ただし「久しぶりに見返して、震えた」という表現は使わず、もっと独自の表現を考えてください）
{f'（{year}年の作品だが、全く色褪せていない）' if year else ''}

## {title}
![パッケージ画像]({image_url})

**出演:** {actresses}
**ジャンル:** {genres}
**メーカー:** {maker}
{f'**監督:** {director}' if director else ''}
{f'**発売:** {year}年' if year else ''}

<div className="affiliate-link-inline">
  <a href="{affiliate_url}" target="_blank" rel="noopener noreferrer">サンプル動画を見る</a>
</div>

## [上記の「今回の記事のテーマ・視点」に基づいた独自の見出し]
（選択された視点（{selected_angle['name']}）に基づいて、作品の魅力を語ってください。見出しも独自のものにしてください）

<div className="affiliate-link-inline">
  <a href="{affiliate_url}" target="_blank" rel="noopener noreferrer">この名作を確認する</a>
</div>

## [画質や映像について語る独自の見出し]
（SD画質、4:3比率、荒い粒子などを「生々しさ」「ドキュメント感」としてポジティブに評価。ただし「画質の粗さが、逆に良い」という見出しは使わず、もっと独自の表現を考えてください）

## コスパ重視の視聴アドバイス
（以下の条件に該当する場合のみ、このセクションを追加してください）
- 紹介する作品が「準新作」〜「旧作」である場合（発売から1年以上経過している場合）
- または、名作・シリーズ物である場合

**【文章の構成】**
1. **価格への言及:**
   「正直、この年代の作品を定価（単品購入）で買うのは、コレクター以外にはおすすめしない。」
   「内容はお墨付きだが、お財布へのダメージは気になるところだ。」

2. **サブスクの提案（解決策）:**
   「もし君がDMM TV（またはFANZA見放題）の会員なら、追加料金なしで再生ボタンを押すだけだ。」
   「まだ会員でないなら、**無料体験枠**を使ってタダで見るのが、最も賢い"勝ち組"の選択だ。」

3. **強烈なひと押し:**
   「浮いたお金で、ローションや別の新作を買うほうが建設的だろう。」
   「ランチ1回分の値段で、この時代の名作が数万本見放題になるのだから、恐ろしい時代になったものだ。」

## [結論の独自の見出し]
（「500円だろうが定価だろうが、これは映像遺産として持っておくべき」と強く推す。ただし「結論：これは映像遺産だ」という見出しは使わず、もっと独自の表現を考えてください）

<div className="affiliate-link">
  <a href="{affiliate_url}" target="_blank" rel="noopener noreferrer">平成の名作を今すぐチェック</a>
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
- 熱量のある、リスペクトに満ちた文章で書いてください。
- 上記の「今回の記事のテーマ・視点」を最優先に、その視点から作品を語ってください。
- 禁止事項を必ず守り、陳腐な表現を避けてください。
- 見出しはすべて独自の、読者の興味を引くものにしてください。
"""
    
    return prompt


def generate_article(model: genai.GenerativeModel, product_info: dict) -> str | None:
    """Gemini APIを使って記事本文を生成"""
    prompt = create_prompt(product_info)
    
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
        return None


def extract_video_cid(video_url: str) -> str | None:
    """
    サンプル動画URLからCIDを抽出
    
    Args:
        video_url: サンプル動画のURL
        
    Returns:
        抽出されたCID、またはNone
    """
    # 既存のextract_content_id_from_url関数を再利用
    return extract_content_id_from_url(video_url)


def insert_video_player(content: str, video_cid: str) -> str:
    """
    記事本文に動画プレーヤーを挿入
    
    Args:
        content: 記事本文（Markdown/HTML）
        video_cid: 動画のCID
        
    Returns:
        動画プレーヤーが挿入された記事本文
    """
    video_script = f'<script src="https://g.dmm.com/js/player/litevideo.js" data-cid="{video_cid}" data-width="100%" data-height="auto"></script>'
    
    # 「FANZA TV」に関連する広告コードまたはリンクを検索
    # パターン1: FANZA TVボタン
    fanza_tv_patterns = [
        r'(<a[^>]*href[^>]*premium\.dmm\.co\.jp[^>]*>.*?FANZA TV.*?</a>)',
        r'(<div[^>]*>.*?FANZA TV.*?</div>)',
        r'(FANZA TV)',
    ]
    
    inserted = False
    for pattern in fanza_tv_patterns:
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        if match:
            # マッチした位置の直後に挿入
            insert_pos = match.end()
            content = content[:insert_pos] + '\n\n' + video_script + '\n\n' + content[insert_pos:]
            inserted = True
            print(f"✅ 動画プレーヤーを「FANZA TV」の直後に挿入しました")
            break
    
    # パターン2: サンプル動画ボタン
    if not inserted:
        sample_patterns = [
            r'(<a[^>]*>.*?サンプル動画.*?</a>)',
            r'(<div[^>]*>.*?サンプル動画.*?</div>)',
            r'(サンプル動画を見る)',
        ]
        
        for pattern in sample_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                insert_pos = match.end()
                content = content[:insert_pos] + '\n\n' + video_script + '\n\n' + content[insert_pos:]
                inserted = True
                print(f"✅ 動画プレーヤーを「サンプル動画」の直後に挿入しました")
                break
    
    # パターン3: フォールバック（記事の末尾に挿入）
    if not inserted:
        # 最後のアフィリエイトリンクの後に挿入
        affiliate_pattern = r'(<div[^>]*className="affiliate-link"[^>]*>.*?</div>)'
        matches = list(re.finditer(affiliate_pattern, content, re.IGNORECASE | re.DOTALL))
        if matches:
            last_match = matches[-1]
            insert_pos = last_match.end()
            content = content[:insert_pos] + '\n\n' + video_script + '\n\n' + content[insert_pos:]
            inserted = True
            print(f"✅ 動画プレーヤーを記事の末尾付近に挿入しました")
        else:
            # 最後の手段：記事の最後に追加
            content = content + '\n\n' + video_script
            inserted = True
            print(f"✅ 動画プレーヤーを記事の最後に挿入しました")
    
    return content


def save_article(content: str, product_info: dict, publish_date: str, output_dir: str, video_cid: str | None = None) -> str | None:
    """記事をMarkdownファイルとして保存"""
    content_id = product_info.get("content_id", "unknown")
    title = product_info.get("title", "")
    image_url = product_info.get("image_url", "")
    affiliate_url = product_info.get("affiliate_url", "")
    actress_list = product_info.get("actress", [])
    genre_list = product_info.get("genre", [])
    release_date = product_info.get("release_date", "")
    
    # 発売年を抽出
    year = ""
    if release_date:
        try:
            year = release_date.split("-")[0]
        except:
            pass
    
    # タグの作成
    tags = []
    if year:
        tags.append(f'"{year}年"')
    tags.append('"平成の名作"')
    if actress_list:
        tags.extend([f'"{actress}"' for actress in actress_list[:2]])
    if genre_list:
        tags.extend([f'"{genre}"' for genre in genre_list[:2]])
    tags_str = ", ".join(tags)
    
    # 抜粋を生成
    excerpt = f"{title}の熱いレビュー。平成時代の名作を再評価する。"
    
    # Frontmatterを作成
    frontmatter = f"""---
title: "{title} ー 平成の名作を語る"
date: "{publish_date}"
excerpt: "{excerpt}"
image: "{image_url}"
tags: [{tags_str}]
affiliateLink: "{affiliate_url}"
contentId: "{content_id}"
---

"""
    
    # ファイル名を作成
    filename = f"{publish_date}-{content_id}.md"
    filepath = os.path.join(output_dir, filename)
    
    # 動画プレーヤーを挿入（video_cidが提供されている場合のみ）
    if video_cid:
        content = insert_video_player(content, video_cid)
    
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
    
    # 無料サンプル動画URLの入力
    print("\n" + "-" * 80)
    video_url = input("無料サンプル動画のURL（または動画がある作品URL）があれば貼り付けてください。なければそのままEnterキーを押してください: ").strip()
    
    video_cid = None
    if video_url:
        print("\n🔍 サンプル動画URLからCIDを抽出中...")
        video_cid = extract_video_cid(video_url)
        if video_cid:
            print(f"✅ 動画CID: {video_cid}")
            print("✅ 記事に動画プレーヤーを挿入します")
        else:
            print("⚠️  URLからCIDを抽出できませんでした。動画プレーヤーは挿入されません。")
    else:
        print("✅ 動画URLが入力されませんでした。動画プレーヤーは挿入されません。")
    
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
    
    # 記事を生成
    print("\n✍️  記事生成中...")
    article_content = generate_article(model, product_info)
    
    if article_content:
        # 記事を保存（動画CIDを渡す）
        filepath = save_article(article_content, product_info, publish_date, str(content_dir), video_cid)
        
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

