#!/usr/bin/env python3
"""
DMM APIを使って作品情報を取得し、Cursor（AI）に記事を書かせるための
最強の指示プロンプトを生成してクリップボードにコピーするスクリプト
"""

import os
import json
import sys
import re
import ssl
import random
import urllib.request
from datetime import datetime
from pathlib import Path
from urllib.parse import urlencode, parse_qs, urlparse, unquote
import pyperclip

# ============================================================================
# 設定項目: ここにAPI認証情報を設定してください
# ============================================================================
API_ID = os.environ.get("DMM_API_ID", "")  # 環境変数から取得、なければ空文字
AFFILIATE_ID = os.environ.get("DMM_AFFILIATE_ID", "")  # 環境変数から取得、なければ空文字

# 環境変数が設定されていない場合は、ここに直接記入してください
# API_ID = "your_api_id_here"
# AFFILIATE_ID = "your_affiliate_id_here"


def load_example_articles(content_dir: Path, max_articles: int = 3) -> list[str]:
    """
    既存の記事からサンプルを読み込む（Frontmatterを除いた本文のみ）
    
    Args:
        content_dir: contentディレクトリのパス
        max_articles: 読み込む最大記事数
        
    Returns:
        サンプル記事の本文リスト（Frontmatterを除く）
    """
    example_articles = []
    
    if not content_dir.exists():
        return example_articles
    
    # 最新の記事から順に読み込む（日付順で降順）
    md_files = sorted(
        [f for f in content_dir.glob("*.md") if f.is_file()],
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )
    
    for filepath in md_files[:max_articles * 2]:  # 余裕を持って取得
        if len(example_articles) >= max_articles:
            break
            
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Frontmatterを除去（---で囲まれた部分）
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    body = parts[2].strip()
                    if body and len(body) > 500:  # 最低500文字以上の記事のみ
                        example_articles.append(body)
                        print(f"📚 サンプル記事を読み込みました: {filepath.name}")
        except Exception as e:
            print(f"⚠️  サンプル記事の読み込みに失敗: {filepath.name} - {e}")
            continue
    
    return example_articles


def extract_content_id_from_url(url: str) -> str | None:
    """
    URLから品番（content_id）を抽出（アフィリエイトリンク対応版）
    
    Args:
        url: DMM作品URL
        
    Returns:
        content_id または None
    """
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
                
                # 画像URLの取得（大きいサイズを優先）
                image_url_dict = item.get("imageURL", {})
                # large → medium → small の順で取得を試みる
                image_url_large = image_url_dict.get("large", "") or image_url_dict.get("medium", "") or image_url_dict.get("small", "")
                
                # サンプル画像URLの取得（大きいサイズを優先）
                sample_images = []
                sample_image_urls = item.get("sampleImageURL", {})
                
                # 大きいサイズから順に取得を試みる（sample_l → sample_m → sample → sample_s）
                for key in ["sample_l", "sample_m", "sample", "sample_s"]:
                    if key in sample_image_urls and "image" in sample_image_urls[key]:
                        img_data = sample_image_urls[key]["image"]
                        if isinstance(img_data, list):
                            for img_url in img_data:
                                if img_url and img_url not in sample_images:
                                    # URLを大きいサイズに変換を試みる
                                    # 例: -1.jpg → jp-1.jpg, thumb → 削除
                                    converted_url = img_url
                                    if "-" in converted_url and "jp-" not in converted_url:
                                        # -1.jpg パターンを jp-1.jpg に変換
                                        converted_url = converted_url.replace(f"-{content_id}-", f"{content_id}jp-")
                                        converted_url = converted_url.replace(f"/{content_id}-", f"/{content_id}/{content_id}jp-")
                                    if "thumb" in converted_url:
                                        converted_url = converted_url.replace("thumb", "")
                                    if "small" in converted_url and "sample" not in converted_url.lower():
                                        converted_url = converted_url.replace("small", "")
                                    sample_images.append(converted_url)
                        elif isinstance(img_data, str) and img_data and img_data not in sample_images:
                            # URLを大きいサイズに変換を試みる
                            converted_url = img_data
                            if "-" in converted_url and "jp-" not in converted_url:
                                converted_url = converted_url.replace(f"-{content_id}-", f"{content_id}jp-")
                                converted_url = converted_url.replace(f"/{content_id}-", f"/{content_id}/{content_id}jp-")
                            if "thumb" in converted_url:
                                converted_url = converted_url.replace("thumb", "")
                            if "small" in converted_url and "sample" not in converted_url.lower():
                                converted_url = converted_url.replace("small", "")
                            sample_images.append(converted_url)
                
                # サンプル画像が見つからない場合、content_idから直接生成（大きいサイズ）
                if not sample_images and content_id:
                    # DMMのサンプル画像URLパターン（大きいサイズ）
                    # videoa と video の両方を試す
                    for floor in ["videoa", "video"]:
                        base_url = f"https://pics.dmm.co.jp/digital/{floor}/{content_id}/{content_id}jp-"
                        for i in range(1, 11):  # 1-10枚目
                            sample_images.append(f"{base_url}{i}.jpg")
                
                # 紹介文の取得（複数のフィールドから取得を試みる）
                description = ""
                if "review" in item and "text" in item["review"]:
                    description = item["review"]["text"]
                elif "comment" in item:
                    description = item["comment"]
                elif "iteminfo" in item and "comment" in item["iteminfo"]:
                    description = item["iteminfo"]["comment"]
                
                # 作品特徴（女優、ジャンル、メーカー等）を取得
                keywords = []
                genres_list = []
                
                # 女優名
                if "iteminfo" in item and "actress" in item["iteminfo"]:
                    actresses = item["iteminfo"]["actress"]
                    for actress in actresses:
                        if "name" in actress:
                            keywords.append(actress["name"])
                
                # ジャンル（別途リストとして保持）
                if "iteminfo" in item and "genre" in item["iteminfo"]:
                    genres = item["iteminfo"]["genre"]
                    for genre in genres:
                        if "name" in genre:
                            genre_name = genre["name"]
                            keywords.append(genre_name)
                            genres_list.append(genre_name)
                
                # メーカー
                if "iteminfo" in item and "maker" in item["iteminfo"]:
                    makers = item["iteminfo"]["maker"]
                    if makers and len(makers) > 0 and "name" in makers[0]:
                        keywords.append(f"メーカー: {makers[0]['name']}")
                
                # シリーズ
                if "iteminfo" in item and "series" in item["iteminfo"]:
                    series_list = item["iteminfo"]["series"]
                    if series_list and len(series_list) > 0 and "name" in series_list[0]:
                        keywords.append(f"シリーズ: {series_list[0]['name']}")
                
                # 監督
                if "iteminfo" in item and "director" in item["iteminfo"]:
                    directors = item["iteminfo"]["director"]
                    if directors and len(directors) > 0 and "name" in directors[0]:
                        keywords.append(f"監督: {directors[0]['name']}")
                
                keywords_str = "、".join(keywords) if keywords else "不明"
                
                # 発売日を取得
                release_date = item.get("date", "")
                
                return {
                    "content_id": item.get("content_id", content_id),
                    "title": item.get("title", ""),
                    "description": description,
                    "keywords": keywords_str,
                    "genres": genres_list,  # ジャンルを別途リストとして保持
                    "main_image_url": image_url_large,
                    "sample_images": sample_images,
                    "affiliate_url": item.get("affiliateURL", ""),
                    "url": item.get("URL", ""),
                    "release_date": release_date,
                }
            else:
                return None
                
    except Exception as e:
        print(f"❌ API取得エラー: {e}", file=sys.stderr)
        return None


def generate_cursor_prompt(product_info: dict, input_url: str, user_features: str = "", example_articles: list[str] = None) -> str:
    """
    Cursor用のプロンプトを生成
    
    Args:
        product_info: 作品情報の辞書
        input_url: 入力されたURL
        
    Returns:
        プロンプト文字列
    """
    title = product_info.get("title", "")
    description = product_info.get("description", "")
    content_id = product_info.get("content_id", "")
    keywords = product_info.get("keywords", "")
    genres_list = product_info.get("genres", [])  # ジャンルを直接取得
    main_image_url = product_info.get("main_image_url", "")
    sample_images = product_info.get("sample_images", [])
    affiliate_url = product_info.get("affiliate_url", "")
    
    # 作品特徴から出演者、メーカー等を抽出
    keywords_parts = keywords.split("、") if keywords else []
    actresses = [k for k in keywords_parts if k not in genres_list and not k.startswith("メーカー:") and not k.startswith("シリーズ:") and not k.startswith("監督:")]
    maker = ""
    series = ""
    director = ""
    for k in keywords_parts:
        if k.startswith("メーカー:"):
            maker = k.replace("メーカー:", "").strip()
        elif k.startswith("シリーズ:"):
            series = k.replace("シリーズ:", "").strip()
        elif k.startswith("監督:"):
            director = k.replace("監督:", "").strip()
    
    actresses_str = "、".join(actresses) if actresses else "不明"
    genres_str = "、".join(genres_list) if genres_list else "不明"
    
    # サンプル画像URLリストを整形（大きいサイズを優先、複数枚ある場合はランダムに選択）
    sample_images_list = ""
    if sample_images:
        # 大きいサイズの画像を優先的に使用（URLに "l" や "large" が含まれるものを優先）
        sorted_samples = sorted(sample_images, key=lambda x: (
            'l' in x.lower() or 'large' in x.lower(),  # 大きいサイズを優先
            'm' in x.lower() or 'medium' in x.lower(),  # 次に中サイズ
            's' in x.lower() or 'small' in x.lower()  # 最後に小サイズ
        ), reverse=True)
        
        # 複数枚ある場合はランダムに4〜6枚選択（1番目の画像は必ず含める）
        if len(sorted_samples) > 1:
            num_to_select = min(random.randint(4, 6), len(sorted_samples))
            # 1番目の画像を必ず含める
            selected_samples = [sorted_samples[0]]
            # 残りからランダムに選択
            remaining_samples = sorted_samples[1:]
            if len(remaining_samples) > 0:
                additional_samples = random.sample(remaining_samples, min(num_to_select - 1, len(remaining_samples)))
                selected_samples.extend(additional_samples)
        else:
            selected_samples = sorted_samples
        
        for i, img_url in enumerate(selected_samples, 1):
            sample_images_list += f"   {i}. {img_url}\n"
    else:
        # サンプル画像が見つからない場合、content_idから生成（大きいサイズ、ランダムに選択）
        sample_images_list = f"   （サンプル画像が見つかりませんでした。以下のパターンからランダムに使用してください）\n"
        # videoa と video の両方のパターンを試す
        for floor in ["videoa", "video"]:
            # 1-10枚目からランダムに4〜6枚選択（1番は必ず含める）
            all_indices = list(range(1, 11))
            num_to_select = random.randint(4, 6)
            # 1番を必ず含める
            selected_indices = [1] + sorted(random.sample([i for i in all_indices if i != 1], min(num_to_select - 1, 9)))
            for idx, i in enumerate(selected_indices, 1):
                sample_images_list += f"   {idx}. https://pics.dmm.co.jp/digital/{floor}/{content_id}/{content_id}jp-{i}.jpg\n"
    
    # 今日の日付を取得
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 第一印象セクションの見出しをランダムに選択（固定リストから）
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
    
    # レーティングを生成（4.0〜5.0の間でランダム）
    rating = round(random.uniform(4.0, 5.0), 1)
    
    # タグを生成（発売日から年数を取得）
    release_date = product_info.get("release_date", "")
    year = ""
    if release_date:
        try:
            # 発売日から年を抽出（YYYY-MM-DD形式またはYYYY/MM/DD形式）
            year_match = re.search(r'(\d{4})', release_date)
            if year_match:
                year = year_match.group(1)
        except:
            pass
    
    # 発売年が取得できない場合は、今日の年を使用（フォールバック）
    if not year:
        year = today.split("-")[0] if today else ""
    
    tags = []
    if year:
        tags.append(f'"{year}年"')
    # 「平成の名作」タグは削除
    if actresses_str != "不明" and actresses:
        tags.extend([f'"{actress}"' for actress in actresses[:2]])
    if genres_str != "不明":
        genre_list = [g.strip() for g in genres_str.split("、") if g.strip()]
        tags.extend([f'"{genre}"' for genre in genre_list[:2]])
    if maker:
        tags.append(f'"{maker}"')
    if len(tags) > 8:
        tags = tags[:8]
    tags_str = ", ".join(tags)
    
    # 既存記事の参考例セクション
    example_section = ""
    if example_articles:
        example_section = "\n# 参考例（既存の記事サンプル）\n"
        example_section += "以下の既存記事を参考にして、**同じスタイル・トーンで書いてください**。\n"
        example_section += "**重要：既存記事と同じ文言・表現は使わないように、必ず表現を変えて書いてください。**\n"
        example_section += "同じ内容を伝える場合でも、別の言葉や表現を使って書くこと。\n\n"
        for i, article in enumerate(example_articles[:3], 1):  # 最大3記事
            example_section += f"## 参考記事 {i}\n"
            # 記事の最初の800文字程度を表示（構成とスタイルを理解できる程度）
            preview = article[:800] + "..." if len(article) > 800 else article
            example_section += f"{preview}\n\n---\n\n"
    
    prompt = f"""# 依頼
以下の作品データ（特に「紹介文」と「作品特徴」）を元に、例の「ｗ」多めの視聴者モードでレビューを書いて。
内容は「きれいなまとめ」にせず、一人のファンとして興奮を爆発させてｗ

{example_section}

# 作品データ
- 作品名： {title}
- 紹介文： {description}
- 作品ID： {content_id}
- 作品URL： {input_url}
- 作品特徴： {keywords}
- 出演： {actresses_str}
- ジャンル： {genres_str}
- メーカー： {maker if maker else "不明"}
{f"- シリーズ： {series}" if series else ""}
{f"- 監督： {director}" if director else ""}

- メイン画像URL： {main_image_url}
- アフィリエイトリンク： {affiliate_url}
- サンプル画像URLリスト：
{sample_images_list}
{f"""
# ⚠️ 重要：ユーザーが指定した作品の特徴
以下の特徴を**必ず記事に盛り込んで、具体的なシーンとして描写してください**：
{user_features}

**これらの特徴を膨らませて、熱量100%で書いてください。**
例：
- 「中出し」→「[K1]シーンがマジでエロすぎて、もう完全に昇天したわｗ 特に最後の[K1]シーンがマジでヤバすぎて、見てるだけで抜けるわｗ」
- 「ハーフ美女」→「ハーフ美人の色白肌がマジでエロすぎて、もう完全にやられたわｗ 日本人離れした美しさがマジで最強だわｗ」
- 「ローションプレイがエロい」→「ローションまみれのシーンがマジでヤバすぎて、もう完全に昇天したわｗ パイパン×ローションって、マジで最強の組み合わせだわｗ」

各特徴について、具体的なシーンを想像して、主観100%で熱量を込めて書いてください。
""" if user_features else ""}

# Role
あなたはAVの熱狂的なファンです。
深夜に最高の一本を見つけて、興奮のままに掲示板やSNSで語り散らかしている「一人の視聴者」として書いてください。

# スタイル指針
- スペック（画角、解像度、制作年）などの説明は一切不要。そんなの誰も見てないｗ
- 丁寧語、ライター気取りのきれいな言葉は全部ゴミ箱へ。
- 「ｗ」や「マジで」「ヤバい」を多用して、リアルな興奮を表現する。
- **重要：語尾のバリエーションを豊富に使ってください。「だわｗ」「だったわｗ」を毎回使わないでください。**
  - 語尾の例：「〜だ」「〜だな」「〜だよ」「〜だろ」「〜だぜ」「〜だっけ」「〜だし」「〜だしな」
  - 語尾の例：「〜だわ」「〜だったわ」「〜だわｗ」「〜だったわｗ」（これらは時々使う程度）
  - 語尾の例：「〜だね」「〜だよね」「〜だなあ」「〜だっけ」「〜だし」
  - 語尾の例：「〜だ」「〜だよな」「〜だよ」「〜だろ」「〜だぜ」
  - 語尾の例：「〜だ」「〜だな」「〜だよ」「〜だろ」「〜だぜ」
  - 語尾を変えることで、文章にリズムと変化を持たせてください。
- **重要：毎回ハイテンションにする必要はありません。色んなパターンで記事を書いてください。**
  - 時には落ち着いた語り口で、じっくりと作品の魅力を語る
  - 時には興奮を抑えめに、冷静に分析する視点で書く
  - 時には熱量100%で、興奮を爆発させる
  - 時には懐かしさやノスタルジーを感じさせる語り口で書く
  - 参考例の記事を見て、様々なトーンやパターンを参考にしてください。

    # ユーザーが指定した作品の特徴（重要）
{f"""
**重要：以下の作品特徴を必ず記事に盛り込んでください：**
{user_features}

これらの特徴を具体的なシーン描写として膨らませて、熱量100%で書いてください。
例：「中出し」→「[K1]シーンがマジでエロすぎて、もう完全に昇天したわｗ」
例：「ローションプレイがエロい」→「ローションまみれのシーンがマジでヤバすぎて、見てるだけで抜けるわｗ」
""" if user_features else ""}

# 執筆ルール
1. **作品のあらすじ・紹介文をしっかり読んで、その内容に基づいて書く**: 
   - **最重要**: 「紹介文」に書かれている具体的なシーンやシチュエーションを必ず反映してください。
   - 紹介文に「学校の教室で」と書いてあれば、そのシーンを具体的に描写してください。
   - 紹介文に「パイパン×美尻」と書いてあれば、その特徴を具体的なシーンとして描写してください。
   - 「抜けるわｗ」「やられたわｗ」などの表現を多用しすぎず、作品の内容に合わせた具体的な描写を重視してください。
   - 作品の内容が分からない場合は、推測で書かず、紹介文から読み取れる情報のみを基に書いてください。
   {f"**特に、上記の「作品特徴」にある内容を必ずシーンとして描写してください。**" if user_features else ""}
2. **シーンの描写**: 
   - 作品に含まれるシーンを具体的に描写してください。変な比喩はいりません。
   - 「紹介文」から読み取れるシーンを中心に、そのシーンの具体的な様子を描写してください。
   - 例：「学校の教室でセーラー服を着たまま」→「教室の机の上で、セーラー服のボタンを外されながら」のように具体的に。
3. **表現のバリエーション**: 
   - 「抜けるわｗ」「やられたわｗ」「テンション上がったわｗ」などの表現を繰り返し使わないでください。
   - **語尾のバリエーション**: 「だわｗ」「だったわｗ」を毎回使わず、様々な語尾を使ってください。
     - 例：「〜だ」「〜だな」「〜だよ」「〜だろ」「〜だぜ」「〜だっけ」「〜だし」「〜だしな」
     - 例：「〜だね」「〜だよね」「〜だなあ」「〜だっけ」「〜だし」
     - 例：「〜だ」「〜だよな」「〜だよ」「〜だろ」「〜だぜ」
     - 「だわｗ」「だったわｗ」は時々使う程度にしてください。
   - 作品の内容に合わせて、様々な表現を使ってください。
   - 例：「このシーンで完全にハマった」「ここがマジでエロかった」「この瞬間にやられた」など、表現を変えてください。
4. **主観のみで語る**: 
   - 「俺はこのシーンで昇天したｗ」的な、個人的な感想を最優先。
   - ただし、作品の内容に合わせた具体的な感想を書いてください。

# 記事の構成
以下の構成で、**Frontmatterを含めた完全なMarkdownファイル**を出力してください：

## Frontmatter（必須）
```yaml
---
title: "{title} ー 名作を語る"
date: "{today}"
excerpt: "{title}の熱いレビュー。名作を再評価する。"
image: "{main_image_url}"
tags: [{tags_str}]
affiliateLink: "{affiliate_url}"
contentId: "{content_id}"
rating: {rating}
---
```

## 本文構成

### 1. 感情が漏れ出してるような一言タイトル
（「キタコレｗ」「マジでヤバい」「これ見てないやつは損してる」みたいな、興奮が溢れ出てる感じのタイトル）

### 2. 作品タイトルセクション
```markdown
## {title}

<a href="{affiliate_url}" target="_blank" rel="sponsored noopener noreferrer">
  <img src="{main_image_url}" alt="{title}" />
</a>

**出演:** {actresses_str}
**ジャンル:** {genres_str}
**メーカー:** {maker if maker else "不明"}
{f'**監督:** {director}' if director else ''}

<div className="affiliate-link-inline">
  <a href="{affiliate_url}" target="_blank" rel="noopener noreferrer">サンプル動画を見る</a>
</div>
```

### 3. サンプル動画プレーヤー（必須）
以下のコードを「サンプル動画を見る」の直後に挿入してください：
```html
<div style="width:100%; padding-top: 75%; position:relative; margin: 2rem 0;"><iframe width="100%" height="100%" max-width="1280px" style="position: absolute; top: 0; left: 0;" src="https://www.dmm.co.jp/litevideo/-/part/=/affi_id=toshichan-002/cid={content_id}/size=1280_720/" scrolling="no" frameborder="0" allowfullscreen></iframe></div>
```

### 4. 第一印象セクション
```markdown
## {selected_heading}

（作品を見始めた瞬間の第一印象を、興奮のままに書く）
（「これヤバいｗ」「マジで期待してたけど超えてきた」みたいな感じ）
（女優の見た目、雰囲気、最初のシーンの印象など、主観100%で）
```

### 5. ここがエロかったｗ（シーン別に熱量100%で）
**重要**: このセクションでは、上記の「紹介文」に書かれている具体的なシーンやシチュエーションを必ず反映してください。
- 紹介文に「学校の教室で」と書いてあれば、そのシーンを具体的に描写してください。
- 紹介文に「パイパン×美尻」と書いてあれば、その特徴を具体的なシーンとして描写してください。
- 「抜けるわｗ」「やられたわｗ」などの表現を多用しすぎず、作品の内容に合わせた具体的な描写を重視してください。
- 紹介文から読み取れる内容を中心に、そのシーンの具体的な様子を描写してください。
- 例：「学校の教室でセーラー服を着たまま」→「教室の机の上で、セーラー服のボタンを外されながら」のように具体的に。

**重要**: シーンを説明した後、必ず以下の形式でサンプル画像を4〜5枚挿入してください：
（サンプル画像URLリストから適切なものを選んで使用）

```markdown
<a href="{affiliate_url}" target="_blank" rel="sponsored noopener noreferrer">
  <img src="[サンプル画像URLリストから選択]" alt="{title}" />
</a>
```

画像は各シーンの説明の後に適切に配置してください。シーンごとに1〜2枚の画像を配置するのが理想的です。

```markdown
<div className="affiliate-link-inline">
  <a href="{affiliate_url}" target="_blank" rel="noopener noreferrer">この名作を確認する</a>
</div>
```

### 6. コスパ重視の視聴アドバイス（旧作の場合のみ）
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

### 7. 今すぐ見てこいｗ（ゴリ押しの結び）
（「マジで見てないやつは損してる」「これ見ずに語れない」みたいな、熱量100%のゴリ押し）
（「500円だろうが定価だろうが、これは持っておくべき一本だわ」と強く推す）
（匿名性や背徳感に触れる結び。「今すぐ見ろ」という確信を読者に植え付ける）

**作品情報:**
- タイトル: {title}
- 品番: {content_id}
- 出演: {actresses_str}
- ジャンル: {genres_str}
- メーカー: {maker if maker else "不明"}
{f'- 発売: {year}年' if year else ''}

# 注意事項
- **Frontmatterを含めた完全なMarkdownファイル**を出力してください。
- アフィリエイトリンクは、上記の3箇所に必ず配置してください。
- 完全タメ口で、熱量100%の文章で書いてください。
- 「ｗ」「マジで」「ヤバい」などのカジュアルな表現を多用してください。
- スペック（画角、解像度など）の説明は一切不要です。
- シーンは具体的に、ストレートに描写してください。
- 主観的な感想を最優先に書いてください。
- **最低2,000文字以上**の記事を書いてください。
- フィルター回避のため、エロワードは [K1][K2][K3] 等で伏せ字にして。
- **重要：既存記事（参考例）と同じ文言・表現は使わないように、必ず表現を変えて書いてください。** 同じ内容を伝える場合でも、別の言葉や表現を使って書くこと。

# 保存処理
記事が完成したら、以下のパスに保存してください：
`/Users/takahashitoshifumi/Desktop/Adult-affi/content/{today}-{content_id}.md`
"""
    
    return prompt


def main():
    """メイン処理"""
    print("\n" + "=" * 80)
    print("  DMM API → Cursor用プロンプト生成ツール")
    print("=" * 80 + "\n")
    
    # API認証情報の確認
    api_id = API_ID
    affiliate_id = AFFILIATE_ID
    
    if not api_id or not affiliate_id:
        print("⚠️  API認証情報が設定されていません", file=sys.stderr)
        print("", file=sys.stderr)
        print("以下のいずれかの方法で設定してください:", file=sys.stderr)
        print("  1. 環境変数を設定: export DMM_API_ID='your_id' && export DMM_AFFILIATE_ID='your_id'", file=sys.stderr)
        print("  2. スクリプト内の定数に直接記入: API_ID = 'your_id'", file=sys.stderr)
        sys.exit(1)
    
    # URL入力
    url = input("作品URLを入力してください: ").strip()
    
    if not url:
        print("❌ URLが入力されていません", file=sys.stderr)
        sys.exit(1)
    
    # URLから品番を抽出
    print("\n🔍 URLから品番を抽出中...")
    content_id = extract_content_id_from_url(url)
    
    if not content_id:
        print("\n❌ URLから品番を抽出できませんでした", file=sys.stderr)
        print("", file=sys.stderr)
        print("📌 対応しているURL形式:", file=sys.stderr)
        print("  • FANZA/DMM通常URL: https://www.dmm.co.jp/digital/videoa/-/detail/=/cid=abc123/", file=sys.stderr)
        print("  • 動画配信URL: https://video.dmm.co.jp/av/content/?id=abc123", file=sys.stderr)
        print("  • アフィリエイトリンク: https://al.dmm.co.jp/?lurl=...", file=sys.stderr)
        sys.exit(1)
    
    print(f"✅ 品番: {content_id}")
    
    # DMM APIから商品情報を取得
    print("📡 DMM APIから商品情報を取得中...")
    product_info = fetch_dmm_product_info(api_id, affiliate_id, content_id)
    
    if not product_info:
        print("❌ 商品情報の取得に失敗しました", file=sys.stderr)
        sys.exit(1)
    
    # 取得した情報を表示
    print("\n✅ 取得した情報:")
    print(f"   作品名: {product_info.get('title', '不明')}")
    print(f"   作品ID: {product_info.get('content_id', '不明')}")
    print(f"   紹介文: {product_info.get('description', '不明')[:100]}...")
    print(f"   作品特徴: {product_info.get('keywords', '不明')[:100]}...")
    print(f"   メイン画像: {product_info.get('main_image_url', '不明')[:80]}...")
    print(f"   サンプル画像: {len(product_info.get('sample_images', []))}枚")
    
    # 作品の特徴をヒアリング
    print("\n" + "=" * 80)
    print("📝 作品の特徴を入力してください（カンマ区切りまたはスペース区切り）")
    print("例: 中出し、ハーフ美女、ローションプレイがエロい")
    print("例: パイパン デカ美尻 バニーガール")
    print("（空白でスキップ可能）")
    print("=" * 80)
    user_features_input = input("\n作品の特徴: ").strip()
    
    # カンマ区切りまたはスペース区切りで分割
    user_features = ""
    if user_features_input:
        # カンマ区切りの場合
        if "," in user_features_input:
            features_list = [f.strip() for f in user_features_input.split(",") if f.strip()]
        # スペース区切りの場合
        else:
            features_list = [f.strip() for f in user_features_input.split() if f.strip()]
        
        if features_list:
            user_features = "\n".join([f"- {feature}" for feature in features_list])
            print(f"\n✅ 以下の特徴を記事に反映します:")
            for feature in features_list:
                print(f"   • {feature}")
    
    # 既存記事を読み込む
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    content_dir = project_root / "content"
    
    print("\n📚 既存記事を読み込み中...")
    example_articles = load_example_articles(content_dir, max_articles=3)
    if example_articles:
        print(f"✅ {len(example_articles)}件の既存記事を読み込みました")
    else:
        print("⚠️  既存記事が見つかりませんでした")
    
    # プロンプトを生成
    print("\n📝 プロンプトを生成中...")
    prompt = generate_cursor_prompt(product_info, url, user_features, example_articles)
    
    # クリップボードにコピー
    try:
        pyperclip.copy(prompt)
        print("\n✅ プロンプトをクリップボードにコピーしました！")
        print("\n" + "=" * 80)
        print("生成されたプロンプト:")
        print("=" * 80)
        print(prompt)
        print("=" * 80)
        print("\n💡 Cursorのチャット欄に貼り付けて使用してください。")
    except Exception as e:
        print(f"\n⚠️  クリップボードへのコピーに失敗しました: {e}", file=sys.stderr)
        print("\n生成されたプロンプト:")
        print("=" * 80)
        print(prompt)
        print("=" * 80)
        print("\n💡 上記のプロンプトを手動でコピーしてください。")


if __name__ == "__main__":
    main()

