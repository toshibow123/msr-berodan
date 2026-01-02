#!/usr/bin/env python3
"""
MGStageデータから記事を生成するスクリプト
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
        "ネトラレ": "関係の変化",
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


def load_mgs_data(json_path: Path) -> list:
    """MGStageのJSONデータを読み込む"""
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if isinstance(data, dict) and "ranking" in data:
            return data["ranking"]
        elif isinstance(data, list):
            return data
        else:
            print(f"❌ 予期しないデータ形式です", file=sys.stderr)
            return []
    except FileNotFoundError:
        print(f"❌ ファイルが見つかりません: {json_path}", file=sys.stderr)
        return []
    except json.JSONDecodeError as e:
        print(f"❌ JSONの解析に失敗しました: {e}", file=sys.stderr)
        return []


def create_article_prompt(product_info: dict) -> str:
    """記事生成用のプロンプトを作成"""
    title = product_info.get("title", "")
    content_id = product_info.get("content_id", "")
    image_url = product_info.get("image_url", "")
    affiliate_url = product_info.get("affiliate_url", "")
    actress_list = product_info.get("actress", [])
    genre_list = product_info.get("genre", [])
    maker = product_info.get("maker", "")
    director = product_info.get("director", "")
    release_date = product_info.get("release_date", "")
    search_keyword = product_info.get("search_keyword", "")
    
    # タイトルをサニタイズ
    sanitized_title = sanitize_title(title)
    
    # 出演者情報
    actresses = "、".join(actress_list) if actress_list else "不明"
    
    # ジャンル情報
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
- **タメ口スタイルは一切使用禁止**：「だわ」「すぎる」「マジで」「ヤバい」「抜ける」など
- **「ｗ」は絶対に使用しない**
- **以下の見出しは絶対に使用しない**：
  - 「タイトル見た瞬間、これヤバいって確信したわｗ」
  - 「ここがエロかったｗ」
  - 「見始めた瞬間に完全にやられたわｗ」
  - 「冒頭からマジで期待値ブチ上げだったわｗ」
  - 「最初の数秒で完全にハマったわｗ」
  - 「画面に映った瞬間、もう完全にやられたわｗ」
  - 「始まった瞬間の「キタコレｗ」感」
  - 「今すぐ見てこいｗ」
  - その他、タメ口や「ｗ」を含む見出し
- **必ず「作品との出会い」「物語の魅力」「ストーリーの深み」「心に残るシーン」「読者への語りかけ」などの洗練された見出しを使用すること**
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
**制作会社**: {maker if maker else "不明"}
**監督**: {director if director else "不明"}
{f'**公開年**: {year}年' if year else ''}
{f'**検索キーワード**: {search_keyword}' if search_keyword else ''}

---

# 記事の構成

以下の構成で、**Frontmatterを含めず、Markdown本文のみ**を出力してください：

## 成熟した女性の魅力が織りなす、禁断の物語

## {sanitized_title}

<a href="{affiliate_url}" target="_blank" rel="sponsored noopener noreferrer">
  <img src="{image_url}" alt="{sanitized_title}" />
</a>

**出演:** {actresses}
**ジャンル:** {genres}
**メーカー:** {maker if maker else "不明"}
{f'**監督:** {director}' if director else ''}

<div className="affiliate-link-inline">
  <a href="{affiliate_url}" target="_blank" rel="noopener noreferrer">作品の詳細を見る</a>
</div>

## 心を揺さぶる、禁断の物語

この作品に出会ったのは、ある静かな夜のことだった。{actresses}という名前を見た瞬間、成熟した女性の魅力が画面から溢れ出てくるような予感がした。タイトルから読み取れる複雑な人間関係、禁断の物語の予感。これは単なる作品ではなく、人間の感情の深層を描き出す物語なのだろうと感じた。

画面に映し出された{actresses}の佇まいは、まさに期待を裏切らないものだった。成熟した女性特有の落ち着きと、それでいて内に秘めた情熱が、彼女の表情から滲み出ている。最初のシーンから、この作品が語ろうとしている物語の重さを感じ取ることができた。

## 物語の魅力

この作品は、タイトルから読み取れる設定が、物語の核心をなしている。家庭を持つ女性の内面というテーマが、どのように展開していくのか。その過程で描かれる感情の機微が、この作品の最大の魅力だ。

タイトルに込められた設定は、単なる刺激的な場面を超えて、人間の関係性の複雑さを描き出している。{actresses}が演じる登場人物の内面、その葛藤や情熱が、丁寧に描かれていく。ストーリーの構成は、時間の流れに沿って丁寧に描かれている。日常的な場面から始まり、その後の展開へと自然に移行していく。{f'監督の{director}による' if director else '監督による'}演出は、各シーンの意味を丁寧に積み重ねていく手法で、物語の深みを増していく。

<a href="{affiliate_url}" target="_blank" rel="sponsored noopener noreferrer">
  <img src="{image_url}" alt="{sanitized_title}" />
</a>

## 演技と演出の妙

{actresses}の演技は、この作品の質を決定づける重要な要素だ。彼女の表情の変化、仕草の一つ一つが、登場人物の内面を丁寧に表現している。特に印象的だったのは、複雑な感情を抱えながらも、それを言葉にしない場面での演技だ。視線の動き、呼吸のリズム、それらすべてが物語を語っている。

{f'監督の{director}による' if director else '監督による'}演出も、この作品の質を高めている。各シーンの構図、光の使い方、カメラワークの選択。すべてが物語のテーマを支えるために機能している。特に、感情の機微を表現する場面での演出は、見る者の心に深く響く。

作品がもたらす余韻は、観終わった後も長く心に残る。単なる刺激的な場面を超えて、人間の感情の複雑さ、関係性の難しさを描き出している。この作品は、成熟した作品を愛する視聴者にとって、心に響く一本となるだろう。

<a href="{affiliate_url}" target="_blank" rel="sponsored noopener noreferrer">
  <img src="{image_url}" alt="{sanitized_title}" />
</a>

<a href="{affiliate_url}" target="_blank" rel="sponsored noopener noreferrer">
  <img src="{image_url}" alt="{sanitized_title}" />
</a>

<a href="{affiliate_url}" target="_blank" rel="sponsored noopener noreferrer">
  <img src="{image_url}" alt="{sanitized_title}" />
</a>

<div className="affiliate-link-inline">
  <a href="{affiliate_url}" target="_blank" rel="noopener noreferrer">この名作を確認する</a>
</div>

## 読者への語りかけ

この作品は、成熟した作品を愛する方にぜひ観ていただきたい一本だ。単なる刺激を求めるのではなく、物語の深み、演技の妙、演出の美しさを味わいたい方にとって、この作品は心に響く体験を提供してくれる。

{actresses}の演技が描き出す、複雑な感情の機微。{f'監督の{director}による' if director else '監督による'}丁寧な演出。それらが織りなす物語は、観る者の心に静かに、しかし深く響いていく。この作品がもたらす余韻は、観終わった後も長く心に残り続けるだろう。

成熟した作品の魅力を、洗練された言葉で語る。この作品は、まさにそのような作品の一つだ。ぜひ、この作品を手に取って、その魅力を堪能していただきたい。

---

## 画像・リンク

- すべての画像はアフィリエイトリンクでラップする
- 外部リンクは `target="_blank" rel="noopener noreferrer sponsored"` を付与する

## 文字数

- 最低2,500文字以上
- 各セクションを丁寧に展開
- 具体的な描写と分析を含める

---

注意: Frontmatter（---で囲まれたメタデータ）は含めず、Markdown本文のみを出力してください。
"""
    
    return prompt


def generate_article(model: genai.GenerativeModel, product_info: dict, max_retries: int = 2) -> str | None:
    """Gemini APIを使って記事本文を生成（リトライ機能付き）"""
    prompt = create_article_prompt(product_info)
    
    # セーフティ設定
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }
    
    generation_config = {
        "temperature": 0.9,
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
                    print(f"   ❌ ブロックされました: {response.prompt_feedback.block_reason}", file=sys.stderr)
                    if attempt < max_retries - 1:
                        print(f"   ⚠️  より婉曲的な表現でリトライします... (試行 {attempt + 1}/{max_retries})")
                        time.sleep(3)
                        continue
                    return None
                else:
                    print(f"   ❌ レスポンス候補がありません", file=sys.stderr)
                return None
            
            return response.text
            
        except Exception as e:
            error_str = str(e)
            
            if "429" in error_str or "quota" in error_str.lower() or "Quota exceeded" in error_str:
                print(f"   ❌ クォータ制限に達しました", file=sys.stderr)
                return None
            elif "block" in error_str.lower() or "safety" in error_str.lower():
                print(f"   ❌ コンテンツがブロックされました", file=sys.stderr)
                return None
            else:
                print(f"   ❌ 記事生成失敗: {e}", file=sys.stderr)
                if attempt < max_retries - 1:
                    wait_time = 5 * (attempt + 1)
                    print(f"   ⏳ {wait_time}秒待機してリトライします... (試行 {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                import traceback
                traceback.print_exc()
                return None
    
    return None


def save_article(content: str, product_info: dict, publish_date: str, output_dir: Path, content_id: str) -> str | None:
    """記事をMarkdownファイルとして保存"""
    title = product_info.get("title", "")
    image_url = product_info.get("image_url", "")
    affiliate_url = product_info.get("affiliate_url", "")
    actress_list = product_info.get("actress", [])
    genre_list = product_info.get("genre", [])
    release_date = product_info.get("release_date", "")
    maker = product_info.get("maker", "")
    director = product_info.get("director", "")
    search_keyword = product_info.get("search_keyword", "")
    
    # 発売年を抽出
    year = ""
    if release_date:
        try:
            year = release_date.split("-")[0]
        except:
            pass
    
    # タグの作成
    tags = []
    
    # 1. 検索キーワードを追加
    if search_keyword:
        tags.append(f'"{search_keyword}"')
    
    # 2. 発売年を追加
    if year:
        tags.append(f'"{year}年"')
    
    # 3. ジャンルを追加
    important_genres = ['中出し', '中出', 'ベロチュー', 'ガチイキ', '3P', '4P', '不倫', 'NTR', 'ネトラレ', '寝取られ', '人妻', '熟女', 'ドラマ']
    for genre in genre_list:
        genre_quoted = f'"{genre}"'
        if genre_quoted not in tags:
            tags.append(genre_quoted)
    
    # 4. タイトルからジャンルを推測（NTR、人妻、熟女など）
    title_lower = title.lower()
    if "ntr" in title_lower or "ネトラレ" in title_lower or "寝取" in title_lower:
        if '"NTR"' not in tags and '"ネトラレ"' not in tags:
            tags.append('"NTR"')
    if "人妻" in title:
        if '"人妻"' not in tags:
            tags.append('"人妻"')
    if "熟女" in title:
        if '"熟女"' not in tags:
            tags.append('"熟女"')
    if "ドラマ" in title:
        if '"ドラマ"' not in tags:
            tags.append('"ドラマ"')
    
    # 5. 女優タグ（最大2人まで）
    if actress_list:
        tags.extend([f'"{actress}"' for actress in actress_list[:2]])
    
    # 6. メーカータグ
    if maker:
        tags.append(f'"{maker}"')
    
    # タグ数制限（最大15個まで）
    tags_str = ", ".join(tags[:15])
    
    # 抜粋を生成
    excerpt = f"{title}のレビュー。成熟した女性の魅力が織りなす、禁断の物語。"
    
    # 評価を生成
    rating = round(random.uniform(4.0, 5.0), 1)
    
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
        print(f"   ❌ ファイルの保存に失敗: {e}", file=sys.stderr)
        return None


def main():
    """メイン処理"""
    print("\n" + "=" * 80)
    print("  MGStageデータから記事生成")
    print("=" * 80 + "\n")
    
    # 環境変数からAPIキーを取得
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ 環境変数 GEMINI_API_KEY が設定されていません", file=sys.stderr)
        sys.exit(1)
    
    # プロジェクトルートのパスを取得
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # データファイルのパス
    data_file = project_root / "data" / "mgs_scraped_data.json"
    
    if not data_file.exists():
        print(f"❌ データファイルが見つかりません: {data_file}", file=sys.stderr)
        sys.exit(1)
    
    # 出力ディレクトリ
    content_dir = project_root / "content"
    content_dir.mkdir(exist_ok=True)
    
    # MGStageデータを読み込む
    print(f"📋 {data_file} を読み込み中...")
    products = load_mgs_data(data_file)
    
    if not products:
        print("❌ 商品データが空です", file=sys.stderr)
        sys.exit(1)
    
    print(f"✅ {len(products)}件の商品を読み込みました\n")
    
    # Gemini APIを初期化
    print("🤖 Gemini APIを初期化中...")
    initialize_gemini(api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    print("✅ 初期化完了\n")
    
    # 公開日の設定
    publish_date_input = input("公開日（YYYY-MM-DD、空白で今日）: ").strip()
    if publish_date_input:
        publish_date = publish_date_input
    else:
        publish_date = datetime.now().strftime("%Y-%m-%d")
    
    print(f"\n📅 公開日: {publish_date}\n")
    
    # 生成する記事数を選択
    print(f"生成する記事数を選択してください（1-{len(products)}）:")
    try:
        num_articles = int(input("記事数: ").strip())
        if num_articles < 1 or num_articles > len(products):
            num_articles = len(products)
    except ValueError:
        num_articles = len(products)
    
    print(f"\n✍️  {num_articles}件の記事を生成します...\n")
    
    success_count = 0
    skip_count = 0
    fail_count = 0
    
    for idx, product in enumerate(products[:num_articles], 1):
        content_id = product.get("content_id", "")
        title = product.get("title", "")
        
        print(f"[{idx}/{num_articles}] 処理中...")
        print(f"   作品ID: {content_id}")
        print(f"   タイトル: {title[:60]}...")
        
        if not content_id:
            print(f"   ❌ 作品IDがありません")
            fail_count += 1
            print()
            continue
        
        # 既存記事のチェック
        existing_file = content_dir / f"{publish_date}-{content_id}.md"
        if existing_file.exists():
            print(f"   ⏭️  既存記事があるためスキップ: {existing_file.name}")
            skip_count += 1
            print()
            continue
        
        # 記事を生成
        print(f"   ✍️  記事生成中...")
        article_content = generate_article(model, product)
        
        if article_content:
            # 記事を保存
            filepath = save_article(article_content, product, publish_date, content_dir, content_id)
            
            if filepath:
                print(f"   ✅ 記事を保存しました: {filepath}")
                success_count += 1
            else:
                print(f"   ❌ 保存失敗")
                fail_count += 1
        else:
            print(f"   ❌ 生成失敗")
            fail_count += 1
        
        print()
        
        # レート制限対策（3秒待機）
        if idx < num_articles:
            time.sleep(3)
    
    # 結果を表示
    print("=" * 80)
    print("🎉 記事生成完了！")
    print(f"   成功: {success_count}件")
    print(f"   スキップ: {skip_count}件")
    print(f"   失敗: {fail_count}件")
    print("=" * 80)


if __name__ == "__main__":
    main()

