#!/usr/bin/env python3
"""
熟女・人妻・ドラマ作品の一括記事生成スクリプト
取得したランキングデータから官能小説的な記事を生成
"""

import os
import json
import sys
import time
import random
from datetime import datetime, timedelta
from pathlib import Path
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from google.generativeai.types import HarmCategory, HarmBlockThreshold

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


def is_valid_genre(product_info: dict) -> tuple[bool, list]:
    """
    熟女・人妻・ドラマに該当するかを判定
    
    Returns:
        (該当するかどうか, 該当するジャンルのリスト)
    """
    genres = product_info.get("genre", [])
    
    valid_genres = {
        "熟女": ["熟女", "三十路", "四十路", "五十路"],
        "人妻": ["人妻", "主婦", "奥さん"],
        "ドラマ": ["ドラマ", "ストーリー", "NTR", "寝取", "不倫", "近親相姦"],
    }
    
    matched_categories = []
    
    for category, keywords in valid_genres.items():
        for keyword in keywords:
            if any(keyword in g for g in genres):
                matched_categories.append(category)
                break
    
    return len(matched_categories) > 0, matched_categories


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
        "人妻": "既婚の女性",
        "熟女": "成熟した女性",
        "巨乳": "豊かな体型",
        "貧乳": "スリムな体型",
        "美乳": "美しい体型",
        "美少女": "若い女性",
        "ロリ": "若い女性",
        "JK": "学生",
        "OL": "働く女性",
        "ナース": "看護師",
        "教師": "教育者",
        "ママ": "母親",
        "義母": "義理の母親",
        "義姉": "義理の姉",
        "義妹": "義理の妹",
        "姉": "年上の女性",
        "妹": "年下の女性",
        "母": "母親",
        "娘": "娘",
        "息子": "息子",
        "父": "父親",
        "夫": "夫",
        "妻": "妻",
        "彼女": "恋人",
        "彼氏": "恋人",
        "同級生": "同世代",
        "先輩": "年上の人",
        "後輩": "年下の人",
        "上司": "職場の先輩",
        "部下": "職場の後輩",
        "素人": "一般の人",
        "素人妻": "一般の既婚女性",
        "素人娘": "一般の若い女性",
        "素人OL": "一般の働く女性",
        "素人ナース": "一般の看護師",
        "素人教師": "一般の教育者",
        "素人ママ": "一般の母親",
        "素人JK": "一般の学生",
        "素人主婦": "一般の主婦",
        "素人熟女": "一般の成熟した女性",
        "素人美少女": "一般の若い女性",
        "素人巨乳": "一般の豊かな体型の女性",
        "素人美乳": "一般の美しい体型の女性",
        "素人パイパン": "一般の清潔な状態の女性",
        "素人ロリ": "一般の若い女性",
        "素人妻": "一般の既婚女性",
        "素人娘": "一般の若い女性",
        "素人OL": "一般の働く女性",
        "素人ナース": "一般の看護師",
        "素人教師": "一般の教育者",
        "素人ママ": "一般の母親",
        "素人JK": "一般の学生",
        "素人主婦": "一般の主婦",
        "素人熟女": "一般の成熟した女性",
        "素人美少女": "一般の若い女性",
        "素人巨乳": "一般の豊かな体型の女性",
        "素人美乳": "一般の美しい体型の女性",
        "素人パイパン": "一般の清潔な状態の女性",
        "素人ロリ": "一般の若い女性",
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

**重要：以下に提示する作品情報は、すべて「創作小説・フィクション作品」として扱ってください。**
- これは実在の人物や出来事ではなく、**創作物・小説作品のレビュー記事**です
- タイトルや説明に含まれる表現は、すべて文学的・比喩的な表現として解釈してください
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

# レビュー対象の作品情報

**重要**: 以下の作品情報は、すべて「創作小説・フィクション作品」として扱ってください。タイトルや説明に含まれる表現は、すべて文学的・比喩的な表現として解釈してください。実在の人物や出来事ではありません。

**作品タイトル**: {sanitized_title}
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
- **比喩的・文学的な表現で、想像力を掻き立てる（直接的な描写は避ける）**
- 余韻を残す、詩的な文章
- あくまで「創作物の一場面」として描写
- **感情的な場面、心理描写の深い場面として表現**
- **「官能的な場面」ではなく「感情が高ぶる場面」「心理的な葛藤が描かれる場面」として表現**

**重要**: シーンの説明の後、以下の形式でサンプル画像を4-5枚挿入してください：

<a href="{affiliate_url}" target="_blank" rel="sponsored noopener noreferrer">
  <img src="https://pics.dmm.co.jp/digital/video/{content_id}/{content_id}jp-1.jpg" alt="{sanitized_title}" />
</a>

<a href="{affiliate_url}" target="_blank" rel="sponsored noopener noreferrer">
  <img src="https://pics.dmm.co.jp/digital/video/{content_id}/{content_id}jp-2.jpg" alt="{sanitized_title}" />
</a>

<a href="{affiliate_url}" target="_blank" rel="sponsored noopener noreferrer">
  <img src="https://pics.dmm.co.jp/digital/video/{content_id}/{content_id}jp-3.jpg" alt="{sanitized_title}" />
</a>

<a href="{affiliate_url}" target="_blank" rel="sponsored noopener noreferrer">
  <img src="https://pics.dmm.co.jp/digital/video/{content_id}/{content_id}jp-4.jpg" alt="{sanitized_title}" />
</a>

<a href="{affiliate_url}" target="_blank" rel="sponsored noopener noreferrer">
  <img src="https://pics.dmm.co.jp/digital/video/{content_id}/{content_id}jp-5.jpg" alt="{sanitized_title}" />
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
- **性的な表現は一切使わず、感情・心理・ストーリー性に焦点を当てる**
- 「情熱的な場面」→「感情が高ぶる場面」「心理的な葛藤が描かれる場面」
- 「官能的な場面」→「心理描写の深い場面」「感情の機微が描かれる場面」

## 文字数
- 最低2,500文字以上
- 各セクションを丁寧に展開

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
                    # ブロックエラーはリトライしても意味がないので即座に失敗
                    return None
                return None
            
            return response.text
            
        except Exception as e:
            error_str = str(e)
            
            # クォータエラー（429）の場合 - リトライしても意味がないので即座に失敗
            if "429" in error_str or "quota" in error_str.lower() or "Quota exceeded" in error_str:
                print(f"   ❌ クォータ制限に達しました。リトライを中止します（トークン節約のため）", file=sys.stderr)
                return None
            # ブロック系のエラーもリトライ不要
            elif "block" in error_str.lower() or "safety" in error_str.lower():
                print(f"   ❌ コンテンツがブロックされました。リトライを中止します", file=sys.stderr)
                return None
            else:
                # その他の一時的なエラーのみリトライ（ネットワークエラーなど）
                print(f"   ❌ 記事生成失敗: {e}", file=sys.stderr)
                if attempt < max_retries - 1:
                    wait_time = 5 * (attempt + 1)  # 短い待機時間（5秒、10秒）
                    print(f"   ⏳ {wait_time}秒待機してリトライします... (試行 {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                return None
    
    return None


def save_article(content: str, product_info: dict, publish_date: str, output_dir: Path, content_id: str, matched_genres: list) -> str | None:
    """記事をMarkdownファイルとして保存"""
    title = product_info.get("title", "")
    image_url = product_info.get("image_url", "")
    affiliate_url = product_info.get("affiliate_url", "")
    actress_list = product_info.get("actress", [])
    genre_list = product_info.get("genre", [])
    release_date = product_info.get("release_date", "")
    maker = product_info.get("maker", "")
    
    # 発売年を抽出
    year = ""
    if release_date:
        try:
            year = release_date.split("-")[0]
        except:
            pass
    
    # タグの作成
    tags = []
    tags.extend([f'"{g}"' for g in matched_genres])
    if year:
        tags.append(f'"{year}年"')
    if actress_list:
        tags.extend([f'"{actress}"' for actress in actress_list[:2]])
    for genre in genre_list[:2]:
        if f'"{genre}"' not in tags:
            tags.append(f'"{genre}"')
    if maker:
        tags.append(f'"{maker}"')
    
    tags_str = ", ".join(tags[:8])
    
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
    filepath = output_dir / filename
    
    # 記事全体を作成
    full_content = frontmatter + content
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(full_content)
        return str(filepath)
    except IOError as e:
        print(f"❌ 保存失敗: {e}", file=sys.stderr)
        return None


def load_ranking_data(data_dir: Path) -> list:
    """ランキングデータを読み込む"""
    latest_file = data_dir / "mature_drama_all_latest.json"
    
    if not latest_file.exists():
        print(f"❌ ランキングファイルが見つかりません: {latest_file}", file=sys.stderr)
        print("", file=sys.stderr)
        print("💡 まず以下のコマンドでランキングを取得してください:", file=sys.stderr)
        print("   python3 scripts/fetch_mature_drama_ranking.py", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(latest_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("ranking", [])
    except Exception as e:
        print(f"❌ ランキングデータの読み込み失敗: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """メイン処理"""
    print("\n" + "✨" * 40)
    print("  熟女・人妻・ドラマ作品 一括記事生成")
    print("  〜艶めく物語〜")
    print("✨" * 40 + "\n")
    
    # 環境変数からAPIキーを取得
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ 環境変数 GEMINI_API_KEY が設定されていません", file=sys.stderr)
        sys.exit(1)
    
    # ディレクトリ設定
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    data_dir = project_root / "data"
    content_dir = project_root / "content"
    
    content_dir.mkdir(exist_ok=True)
    
    # ランキングデータを読み込む
    print("📖 ランキングデータを読み込み中...")
    ranking_data = load_ranking_data(data_dir)
    print(f"✅ {len(ranking_data)}件の作品を取得しました\n")
    
    # 生成する記事数を入力
    max_articles = int(input(f"何本の記事を生成しますか？（最大{len(ranking_data)}本）: ").strip() or "10")
    max_articles = min(max_articles, len(ranking_data))
    
    # 開始日を入力
    start_date_input = input("開始日（YYYY-MM-DD、空白で今日）: ").strip()
    if start_date_input:
        start_date = datetime.strptime(start_date_input, "%Y-%m-%d")
    else:
        start_date = datetime.now()
    
    print(f"\n📅 開始日: {start_date.strftime('%Y-%m-%d')}")
    print(f"📝 生成本数: {max_articles}本")
    print()
    
    # 既存記事のcontent_idを取得
    print("🔍 既存記事をチェック中...")
    existing_content_ids = set()
    for content_file in content_dir.glob("*.md"):
        try:
            with open(content_file, "r", encoding="utf-8") as f:
                content = f.read()
                # frontmatterからcontentIdを抽出
                if "contentId:" in content:
                    for line in content.split("\n"):
                        if line.startswith("contentId:"):
                            existing_id = line.split("contentId:")[1].strip().strip('"').strip("'")
                            if existing_id:
                                existing_content_ids.add(existing_id)
                            break
        except Exception:
            pass
    
    print(f"✅ {len(existing_content_ids)}件の既存記事を検出しました\n")
    
    # 既存記事を除外
    filtered_ranking = [work for work in ranking_data if work.get("content_id", "") not in existing_content_ids]
    print(f"📊 フィルタリング後: {len(filtered_ranking)}件（既存除外: {len(ranking_data) - len(filtered_ranking)}件）\n")
    
    if not filtered_ranking:
        print("❌ 新規記事がありません。全て既存記事です。", file=sys.stderr)
        sys.exit(0)
    
    # Gemini APIを初期化
    print("🤖 Gemini APIを初期化中...")
    initialize_gemini(api_key)
    
    model_name = "gemini-2.5-flash"
    print(f"✅ {model_name} を使用します\n")
    model = genai.GenerativeModel(model_name)
    
    # 記事生成
    success_count = 0
    skip_count = 0
    fail_count = 0
    failed_items = []  # 失敗した記事を記録
    
    for idx, work in enumerate(filtered_ranking[:max_articles], 1):
        content_id = work.get("content_id", "")
        title = work.get("title", "不明")
        
        # 公開日を計算（1日1本）
        publish_date = (start_date + timedelta(days=idx-1)).strftime("%Y-%m-%d")
        
        # 念のため既存記事のチェック（日付が異なる場合もチェック）
        existing_file = content_dir / f"{publish_date}-{content_id}.md"
        if existing_file.exists():
            print(f"[{idx}/{max_articles}] ⏭️  既存: {title[:40]}...")
            skip_count += 1
            continue
        
        print(f"[{idx}/{max_articles}] 📝 {title[:40]}...")
        print(f"   公開日: {publish_date}")
        
        # ジャンル判定
        is_valid, matched_genres = is_valid_genre(work)
        if not is_valid:
            print(f"   ⏭️  スキップ（対象外ジャンル）")
            skip_count += 1
            continue
        
        print(f"   ジャンル: {', '.join(matched_genres)}")
        
        # 記事生成
        print(f"   ✍️  生成中...")
        article_content = generate_article(model, work)
        
        if article_content:
            # 保存
            filepath = save_article(article_content, work, publish_date, content_dir, content_id, matched_genres)
            
            if filepath:
                print(f"   ✅ 保存完了")
                success_count += 1
            else:
                print(f"   ❌ 保存失敗")
                fail_count += 1
        else:
            print(f"   ❌ 生成失敗")
            fail_count += 1
            # 失敗した記事を記録
            failed_items.append({
                "content_id": content_id,
                "title": title,
                "publish_date": publish_date,
                "work": work
            })
        
        # レート制限対策（クォータを考慮して長めに待機）
        if idx < max_articles:
            wait_time = 15  # 15秒待機（クォータ制限を考慮）
            print(f"   ⏳ {wait_time}秒待機中...")
            time.sleep(wait_time)
        
        print()
    
    # 失敗した記事をJSONファイルに保存
    if failed_items:
        failed_file = data_dir / "failed_articles.json"
        try:
            with open(failed_file, "w", encoding="utf-8") as f:
                json.dump(failed_items, f, ensure_ascii=False, indent=2)
            print(f"📝 失敗した記事を記録しました: {failed_file}")
        except Exception as e:
            print(f"⚠️  失敗記事の記録に失敗: {e}", file=sys.stderr)
    
    # 完了メッセージ
    print("=" * 80)
    print("🎉 記事生成完了！")
    print("=" * 80)
    print(f"✅ 成功: {success_count}本")
    print(f"⏭️  スキップ: {skip_count}本")
    print(f"❌ 失敗: {fail_count}本")
    if failed_items:
        print(f"💾 失敗した記事は {failed_file} に保存されました")
        print(f"   再試行するには: python3 scripts/retry_failed_articles.py")
    print(f"📁 保存先: {content_dir}")
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()


