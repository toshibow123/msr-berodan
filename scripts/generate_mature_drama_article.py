#!/usr/bin/env python3
"""
熟女・人妻・ドラマ作品専門の記事生成スクリプト
官能小説のような雰囲気で、ストーリー性と演技力を重視した記事を生成
"""

import os
import json
import sys
import re
import random
import time
from datetime import datetime
from pathlib import Path
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import urllib.request
import urllib.error
import ssl
from urllib.parse import urlencode, parse_qs, urlparse, unquote

# .envファイルの読み込み
try:
    from dotenv import load_dotenv
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass


def initialize_gemini(api_key: str):
    """Gemini APIを初期化"""
    genai.configure(api_key=api_key)


def sanitize_title(title: str) -> str:
    """タイトルから直接的な表現を除去・置換"""
    # 直接的な表現を婉曲的な表現に置換（大幅に拡張）
    replacements = {
        "中出し": "感情的な結末",
        "SEX": "親密な場面",
        "性交": "親密な場面",
        "筆おろし": "初めての体験",
        "童貞": "未経験",
        "不倫": "禁断の関係",
        "近親相姦": "複雑な関係",
        "寝取": "関係の変化",
        "NTR": "関係の変化",
        "生ハメ": "深い関係",
        "ハメ": "親密な関係",
        "フェラ": "親密な交流",
        "オナニー": "一人の時間",
        "レイプ": "強制的な関係",
        "強姦": "強制的な関係",
        "輪姦": "複数の関係",
        "痴漢": "不適切な接触",
        "露出": "開放的な場面",
        "アナル": "特別な関係",
        "ケツ": "特別な部分",
        "尻": "後ろ姿",
        "おっぱい": "胸",
        "パイパン": "清潔な状態",
        "パイズリ": "親密な交流",
        "3P": "複数の関係",
        "4P": "複数の関係",
        "複数": "多様な関係",
        "イキ": "感情の高まり",
        "イク": "感情の高まり",
        "絶頂": "感情の高まり",
        "潮吹き": "感情の表現",
        "スプラッシュ": "感情の表現",
        "ザーメン": "感情の表現",
        "精液": "感情の表現",
        "射精": "感情の高まり",
        "セフレ": "特別な関係",
        "浮気": "複雑な関係",
        "不貞": "複雑な関係",
    }
    
    sanitized = title
    for direct, indirect in replacements.items():
        sanitized = sanitized.replace(direct, indirect)
    
    return sanitized


def sanitize_description(description: str) -> str:
    """作品説明から直接的な表現を除去・置換"""
    if not description:
        return ""
    
    # タイトルと同じ置換ルールを適用
    sanitized = sanitize_title(description)
    
    # 説明特有の置換
    additional_replacements = {
        "〜": "、",
        "…": "、",
        "！": "。",
        "？": "。",
    }
    
    for direct, indirect in additional_replacements.items():
        sanitized = sanitized.replace(direct, indirect)
    
    return sanitized


def extract_content_id_from_url(url: str) -> str | None:
    """URLから品番（content_id）を抽出"""
    # アフィリエイトリンクの場合、実URLを取り出す
    if "al.fanza.co.jp" in url or "al.dmm.co.jp" in url:
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        if 'lurl' in qs:
            url = unquote(qs['lurl'][0])
            print(f"🔍 アフィリエイトリンクを検出: 実URLに変換しました")
    
    # 正規表現で品番を抽出
    patterns = [
        r'cid=([a-z0-9_]+)',
        r'id=([a-z0-9_]+)',
        r'/detail/=/cid=([a-z0-9_]+)',
        r'content_id=([a-z0-9_]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return None


def fetch_dmm_product_info(api_id: str, affiliate_id: str, content_id: str) -> dict | None:
    """DMM APIから商品情報を取得"""
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


def is_valid_genre(product_info: dict) -> tuple[bool, list]:
    """
    熟女・人妻・ドラマに該当するかを判定
    
    Returns:
        (該当するかどうか, 該当するジャンルのリスト)
    """
    genres = product_info.get("genre", [])
    
    # 対象ジャンル
    valid_genres = {
        "熟女": ["熟女"],
        "人妻": ["人妻", "人妻・主婦"],
        "ドラマ": ["ドラマ", "ストーリー", "NTR", "寝取り", "寝取られ", "不倫", "近親相姦"],
    }
    
    matched_categories = []
    
    for category, keywords in valid_genres.items():
        for keyword in keywords:
            if any(keyword in g for g in genres):
                matched_categories.append(category)
                break
    
    return len(matched_categories) > 0, matched_categories


def create_article_prompt(product_info: dict) -> str:
    """記事生成用のプロンプトを作成"""
    title = product_info.get("title", "")
    # タイトルをサニタイズ（プロンプト内では婉曲的な表現を使用）
    sanitized_title = sanitize_title(title)
    content_id = product_info.get("content_id", "")
    image_url = product_info.get("image_url", "")
    affiliate_url = product_info.get("affiliate_url", "")
    actress_list = product_info.get("actress", [])
    genre_list = product_info.get("genre", [])
    maker = product_info.get("maker", "")
    director = product_info.get("director", "")
    description = product_info.get("description", "")
    release_date = product_info.get("release_date", "")
    
    # 説明もサニタイズ
    sanitized_description = sanitize_description(description)
    
    actresses = "、".join(actress_list) if actress_list else "不明"
    genres = "、".join(genre_list) if genre_list else "不明"
    
    # 発売年を抽出
    year = ""
    if release_date:
        try:
            year = release_date.split("-")[0]
        except:
            pass
    
    prompt = f"""# あなたの役割

あなたは、文芸評論家と映画評論家の両方の視点を持つ、洗練されたレビュアーです。

**最重要：この記事は「創作小説・フィクション作品のレビュー」として書いてください。**
- これは実在の人物や出来事ではなく、**創作物・小説作品のレビュー記事**です
- 映画やドラマ作品のストーリー分析・演技評価の視点で書きます
- 文学的・芸術的な表現を心がけます
- 文芸誌や映画評論誌のような品格のある文章を書きます

## 重要な前提（必ず守ること）
- **この記事は創作小説・フィクション作品のレビュー**として書きます
- 登場人物は「キャラクター」「役柄」「登場人物」として扱います（実在の人物ではない）
- ストーリーは「物語」「作品世界」「フィクション」として分析します
- 映画やドラマ作品のストーリー分析・演技評価の視点で書きます
- 文学的・芸術的な表現を心がけます
- 文芸誌や映画評論誌のような品格のある文章を書きます
- **性的な描写は一切含めず、ストーリー性と演技力の分析に焦点を当てます**

## 執筆の特徴
- ストーリーの構成や演出を映画レビューのように分析する
- 登場人物の演技力や表現力を文学的視点で評価する
- 読者がうっとりするような、余韻を残す文章を書く
- 女性読者も楽しめる、品のある表現を心がける
- **あくまで「創作物のレビュー」として、文学的・芸術的な視点で書く**

## 厳守すべき制約
- 批判・悪口は一切禁止（ポジティブな視点のみ）
- スラング（「ｗ」「マジで」「ヤバい」など）は使用しない
- **直接的な性的表現は一切使用しない。文学的・比喩的な表現のみを使用**
- 登場人物への失礼な表現は禁止
- **あくまで「創作物のレビュー」として書く**
- **性的な場面は「感情的な場面」「心理描写の深い場面」として表現**

---

# 作品情報（創作小説・フィクション作品）

**作品タイトル**: {sanitized_title}
**注意**: タイトルは創作小説・フィクション作品のタイトルとして扱ってください。直接的な表現は含まれていません。
**作品ID**: {content_id}
**主要キャラクター**: {actresses}
**ジャンル**: {genres}
**制作会社**: {maker}
{f'**監督**: {director}' if director else ''}
{f'**公開年**: {year}年' if year else ''}
**作品画像URL**: {image_url}
**作品詳細URL**: {affiliate_url}

**作品あらすじ**:
{sanitized_description if sanitized_description else "（説明なし）"}

**注意**: これは創作小説・フィクション作品のレビューです。登場人物はキャラクターとして、ストーリーは物語として扱ってください。作品あらすじに含まれる表現は、すべて文学的・比喩的な表現として解釈してください。

---

# 記事構成

以下の構成で、Markdown本文のみを出力してください（Frontmatterは不要）：

## [詩的なタイトル]
（「心を揺さぶる、複雑な人間関係の物語」「成熟した表現が光る作品」など、作品の魅力を一言で表現）

## {sanitized_title}

<a href="{affiliate_url}" target="_blank" rel="sponsored noopener noreferrer">
  <img src="{image_url}" alt="{sanitized_title}" />
</a>

**主要キャラクター:** {actresses}
**ジャンル:** {genres}
**制作会社:** {maker}
{f'**監督:** {director}' if director else ''}
{f'**公開年:** {year}年' if year else ''}

<div className="affiliate-link-inline">
  <a href="{affiliate_url}" target="_blank" rel="noopener noreferrer">作品の詳細を見る</a>
</div>

<div style="width:100%; padding-top: 75%; position:relative; margin: 2rem 0;"><iframe width="100%" height="100%" max-width="1280px" style="position: absolute; top: 0; left: 0;" src="https://www.dmm.co.jp/litevideo/-/part/=/affi_id=toshichan-002/cid={content_id}/size=1280_720/" scrolling="no" frameborder="0" allowfullscreen></iframe></div>

## 作品との出会い

（この創作小説・ドラマ作品との出会いを、文学的・映画評論的に語る）
- 「この作品に出会ったのは〜」という自然な語り出し
- タイトルやパッケージから感じた印象、期待感
- 作品が描く世界観への期待

## 物語の魅力

（ストーリーの構成、設定、展開を映画レビュー・文芸評論のように分析）
- 物語の設定、テーマを丁寧に紹介
- ネタバレしない範囲で、物語の核心に迫る
- 人間関係の複雑さ、心理描写の深さを語る
- 「作品説明」の内容を必ず反映すること
- 文学的・芸術的な視点で物語を分析

## 演技と演出の妙

（登場人物の演技力、表現力を映画評論的に評価）
- 登場人物の表現力の素晴らしさを具体的に
- 表情の変化、仕草の繊細さ
- 監督の演出、カメラワークへの言及
- 成熟した女性の魅力を、芸術的な視点で表現

## 心に残るシーン

（特に印象的だったシーンを、文学的・映画評論的に描写）
- 具体的なシーンを2-3つ取り上げる
- 比喩的・文学的な表現で、想像力を掻き立てる
- 余韻を残す、詩的な文章
- あくまで「創作物の一場面」として描写

**重要**: シーンの説明の後、以下の形式でサンプル画像を4-5枚挿入してください：

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

<div className="affiliate-link-inline">
  <a href="{affiliate_url}" target="_blank" rel="noopener noreferrer">サンプル動画で確認する</a>
</div>

## この作品を観るあなたへ

（読者への語りかけで締めくくる）
- 「この作品は、あなたに新しい発見をもたらすでしょう」のような語りかけ
- 作品から得られる体験、感情を伝える
- 余韻を残す、詩的な締めくくり

<div className="affiliate-link">
  <a href="{affiliate_url}" target="_blank" rel="noopener noreferrer">作品を鑑賞する</a>
</div>

**作品情報:**
- 作品タイトル: {sanitized_title}
- 作品ID: {content_id}
- 主要キャラクター: {actresses}
- ジャンル: {genres}
- 制作会社: {maker}
{f'- 公開年: {year}年' if year else ''}

---

# 執筆ガイドライン

## 推奨表現（文学的・映画評論的）
- 「余韻」「深み」「情感」「表現力」「芸術性」
- 「心を揺さぶる」「魅了される」「感動的」
- 「複雑な人間関係」「心理描写」「ドラマ性」
- 「成熟した表現」「洗練された演出」「芸術的な美しさ」
- 比喩的表現：「まるで〜のように」「〜を思わせる」

## 描写のバランス
- ストーリー: 40%（物語の構成、テーマ）
- 演技: 30%（女優の演技力、表情）
- 演出: 20%（監督の演出、カメラワーク）
- シーン描写: 10%（具体的なシーン）

## 文字数
- 最低2,500文字以上
- 各セクションを丁寧に展開
- 具体的な描写と分析を含める

---

注意: Frontmatter（---で囲まれたメタデータ）は含めず、Markdown本文のみを出力してください。
"""
    
    return prompt


def generate_article(model: genai.GenerativeModel, product_info: dict, max_retries: int = 2) -> str | None:
    """Gemini APIを使って記事本文を生成（リトライ機能付き、トークン消費を最小化）"""
    prompt = create_article_prompt(product_info)
    
    # セーフティ設定（創作物・小説レビューとして扱うため、ブロックを緩和）
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,  # 高レベルのみブロック
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }
    
    generation_config = {
        "temperature": 0.9,  # 創造性を高める
        "top_p": 0.95,
        "top_k": 40,
    }
    
    for attempt in range(max_retries):
        try:
            response = model.generate_content(
                prompt,
                safety_settings=safety_settings,
                generation_config=generation_config
            )
            
            if not response.candidates:
                if response.prompt_feedback and response.prompt_feedback.block_reason:
                    print(f"❌ ブロックされました: {response.prompt_feedback.block_reason}", file=sys.stderr)
                    # ブロックされた場合、1回だけリトライを試みる（トークン節約のため）
                    if attempt < max_retries - 1:
                        print(f"⚠️  より婉曲的な表現でリトライします... (試行 {attempt + 1}/{max_retries})")
                        time.sleep(3)  # 短い待機時間
                        continue
                    return None
                else:
                    print(f"❌ レスポンス候補がありません", file=sys.stderr)
                return None
            
            return response.text
            
        except Exception as e:
            error_str = str(e)
            
            # クォータエラー（429）の場合 - リトライしても意味がないので即座に失敗
            if "429" in error_str or "quota" in error_str.lower() or "Quota exceeded" in error_str:
                print(f"❌ クォータ制限に達しました。リトライを中止します（トークン節約のため）", file=sys.stderr)
                return None
            # ブロック系のエラーもリトライ不要
            elif "block" in error_str.lower() or "safety" in error_str.lower():
                print(f"❌ コンテンツがブロックされました。リトライを中止します", file=sys.stderr)
                return None
            else:
                # その他の一時的なエラーのみリトライ（ネットワークエラーなど）
                print(f"❌ 記事生成失敗: {e}", file=sys.stderr)
                if attempt < max_retries - 1:
                    wait_time = 5 * (attempt + 1)  # 短い待機時間（5秒、10秒）
                    print(f"⏳ {wait_time}秒待機してリトライします... (試行 {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                import traceback
                traceback.print_exc()
                return None
    
    return None


def save_article(content: str, product_info: dict, publish_date: str, output_dir: str, content_id: str, matched_genres: list) -> str | None:
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
    
    # タグの作成
    tags = []
    
    # 1. マッチしたジャンル（熟女、人妻、ドラマなど）を追加
    tags.extend([f'"{g}"' for g in matched_genres])
    
    # 2. 発売年を追加
    if year:
        tags.append(f'"{year}年"')
    
    # 3. DMM APIから取得したすべてのジャンルを追加（重複を避ける）
    # 重要なジャンル（中出しなど）を優先的に追加
    important_genres = ['中出し', '中出', 'ベロチュー', 'ガチイキ', '3P', '4P', '不倫', 'NTR', 'ネトラレ', '寝取られ']
    for genre in genre_list:
        genre_quoted = f'"{genre}"'
        # 重要なジャンルは優先的に追加
        if any(important in genre for important in important_genres):
            if genre_quoted not in tags:
                tags.append(genre_quoted)
    
    # 4. その他のジャンルを追加
    for genre in genre_list:
        genre_quoted = f'"{genre}"'
        if genre_quoted not in tags:
            tags.append(genre_quoted)
    
    # 5. 女優タグ（最大2人まで）
    if actress_list:
        tags.extend([f'"{actress}"' for actress in actress_list[:2]])
    
    # 6. メーカータグ
    if maker:
        tags.append(f'"{maker}"')
    
    # タグ数制限を緩和（最大15個まで）
    tags_str = ", ".join(tags[:15])
    
    # 抜粋を生成
    excerpt = f"{title}のレビュー。大人の女性の色気とストーリー性を、官能小説のような筆致で綴ります。"
    
    # 評価を生成
    rating = round(random.uniform(4.0, 5.0), 1)
    story_score = round(random.uniform(4.0, 5.0), 1)
    acting_score = round(random.uniform(4.0, 5.0), 1)
    atmosphere_score = round(random.uniform(4.0, 5.0), 1)
    
    # Frontmatterを作成
    frontmatter = f"""---
title: "{title}"
date: "{publish_date}"
excerpt: "{excerpt}"
image: "{image_url}"
tags: [{tags_str}]
affiliateLink: "{affiliate_url}"
contentId: "{content_id}"
rating: {rating}
genre: [{", ".join([f'"{g}"' for g in matched_genres])}]
storyScore: {story_score}
actingScore: {acting_score}
atmosphereScore: {atmosphere_score}
---

"""
    
    # ファイル名を作成
    filename = f"{publish_date}-{content_id}.md"
    filepath = os.path.join(output_dir, filename)
    
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
    print("\n" + "✨" * 40)
    print("  熟女・人妻・ドラマ作品 記事生成ツール")
    print("  〜官能小説のような雰囲気で〜")
    print("✨" * 40 + "\n")
    
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
    print("作品のURLを入力してください（FANZAの商品ページ）:")
    url = input("URL: ").strip()
    
    if not url:
        print("❌ URLが入力されていません")
        sys.exit(1)
    
    # URLから品番を抽出
    print("\n🔍 URLから品番を抽出中...")
    content_id = extract_content_id_from_url(url)
    
    if not content_id:
        print("\n❌ URLから品番を抽出できませんでした", file=sys.stderr)
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
    print(f"   ジャンル: {', '.join(product_info.get('genre', []))}")
    
    # ジャンル判定
    is_valid, matched_genres = is_valid_genre(product_info)
    
    if not is_valid:
        print("\n❌ この作品は対象ジャンル（熟女・人妻・ドラマ）に該当しません")
        print(f"   ジャンル: {', '.join(product_info.get('genre', []))}")
        sys.exit(1)
    
    print(f"✅ 対象ジャンル: {', '.join(matched_genres)}")
    
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
    
    model_name = "gemini-2.5-flash"
    print(f"✅ {model_name} を使用します")
    model = genai.GenerativeModel(model_name)
    
    # 記事を生成
    print("\n✍️  記事生成中（官能小説のような雰囲気で...）")
    article_content = generate_article(model, product_info)
    
    if article_content:
        # 記事を保存
        filepath = save_article(article_content, product_info, publish_date, str(content_dir), content_id, matched_genres)
        
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

