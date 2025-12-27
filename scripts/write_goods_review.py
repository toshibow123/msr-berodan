#!/usr/bin/env python3
"""
アラフォーOL「マリ」によるアダルトグッズレビュー記事生成スクリプト
手動で商品情報を入力し、Gemini APIで記事を生成する
"""

import os
import json
import sys
import time
from datetime import datetime
from pathlib import Path
import google.generativeai as genai


def initialize_gemini(api_key: str):
    """
    Gemini APIを初期化
    
    Args:
        api_key: Gemini APIキー
    """
    genai.configure(api_key=api_key)


def create_prompt(product_info: dict) -> str:
    """
    マリのペルソナでグッズレビュー記事を生成するプロンプトを作成
    
    Args:
        product_info: 商品情報の辞書
            - name: 商品名
            - price: 価格（任意）
            - features: 特徴（任意）
            - affiliate_url: アフィリエイトリンク（任意）
            - image_url: 商品画像URL（任意）
    
    Returns:
        プロンプト文字列
    """
    product_name = product_info.get("name", "")
    price = product_info.get("price", "")
    features = product_info.get("features", "")
    affiliate_url = product_info.get("affiliate_url", "")
    image_url = product_info.get("image_url", "")
    
    prompt = f"""あなたは「都内のメーカーに勤務する38歳の独身OL、マリ」です。
以下のルールに従って、指定された「大人のグッズ」の紹介ブログを書いてください。

**【キャラクター設定】**
- 38歳、独身。仕事は真面目だが、最近は中間管理職としてのストレスが溜まっている。
- 家ではズボラ。缶チューハイやハイボールを飲みながらリラックスするのが好き。
- 口調は「〜だわ」「〜のよ」という強いオネエ言葉ではなく、自然な大人の女性の話し言葉（例：「〜なんだよね」「〜しちゃった」）。
- アダルトグッズは「いやらしいもの」ではなく「明日も仕事を頑張るためのセルフケア用品」として捉えている。

**【記事のトーン＆マナー】**
- 読者に語りかけるような、日記形式のエッセイ風にする。
- 専門用語（クリトリス、オナニー等）はなるべく避け、「あそこ」「セルフプレジャー」「ひとり時間」など、マイルドな表現に言い換える。
- 冒頭は必ず「お疲れ様。マリだよ。」や「今日も会議で詰められてヘトヘト...」といった、日常の哀愁漂う挨拶から始める。

**【紹介する商品】**
商品名: {product_name}
{f'価格: {price}' if price else ''}
{f'特徴: {features}' if features else ''}

**【記事の構成】**

## お疲れ様、マリだよ
（仕事の愚痴や、最近の疲れについての雑談。2-3文程度。「今日も残業で疲れちゃった」など）

## 最近買っちゃったもの
（なぜこの商品を買ったのか。ネット広告で見つけた、友達に勧められた、など。商品名を自然に紹介）
{f'![{product_name}]({image_url})' if image_url else ''}

## 届いて開けてみたら...
（パッケージや見た目の第一印象。「思ったより小さい」「ピンク色が可愛い」など）

## 実際に使ってみて
（使用感を具体的に。露骨すぎず、でも「気持ちよさ」や「癒やし」が伝わる表現で。
例：「じんわり温かくて、疲れた体に染みる感じ」「思った以上に静かで、アパートでも安心」など）

## こんな人におすすめかも
（どんな人に向いているか。「私みたいに疲れてる人」「ひとり時間を充実させたい人」など）

## まとめ：明日も頑張ろう
（前向きな締めくくり。「これがあれば明日も頑張れそう」「たまには自分を甘やかすのも大事だよね」など）

{f'''<div className="affiliate-link">
  <a href="{affiliate_url}" target="_blank" rel="noopener noreferrer">気になった人はこちらで見てみてね</a>
</div>''' if affiliate_url else ''}

**【注意事項】**
- Frontmatter（---で囲まれたメタデータ）は含めず、Markdown本文のみを出力してください。
- アフィリエイトリンクは、上記の形式で必ず記事の最後に配置してください。
- 自然な口調で、読者に語りかけるように書いてください。
- 露骨な性的表現は避け、マイルドで品のある表現を心がけてください。
"""
    
    return prompt


def generate_article(model: genai.GenerativeModel, product_info: dict) -> str | None:
    """
    Gemini APIを使って記事本文を生成
    
    Args:
        model: Geminiモデル
        product_info: 商品情報
        
    Returns:
        生成された記事本文（Markdown形式）
    """
    prompt = create_prompt(product_info)
    
    try:
        response = model.generate_content(prompt)
        
        # コンテンツがブロックされた場合のエラーハンドリング
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


def save_article(content: str, product_info: dict, publish_date: str, output_dir: str) -> str | None:
    """
    記事をMarkdownファイルとして保存
    
    Args:
        content: 記事本文
        product_info: 商品情報
        publish_date: 公開日（YYYY-MM-DD形式）
        output_dir: 出力ディレクトリ
        
    Returns:
        保存したファイルパス
    """
    product_name = product_info.get("name", "unknown")
    image_url = product_info.get("image_url", "")
    affiliate_url = product_info.get("affiliate_url", "")
    category = product_info.get("category", "グッズレビュー")
    
    # タグの作成
    tags = ['"セルフケア"', '"アラフォーOL"', '"マリのレビュー"']
    if category:
        tags.insert(0, f'"{category}"')
    tags_str = ", ".join(tags)
    
    # タイトルを記事本文から抽出（最初の見出し）、または自動生成
    title_match = content.split('\n')[0] if content else ""
    if title_match.startswith('##'):
        title = title_match.replace('##', '').strip()
    else:
        title = f"【マリのレビュー】{product_name}"
    
    # 抜粋を生成（本文の最初の段落から）
    excerpt_lines = [line for line in content.split('\n') if line.strip() and not line.startswith('#')]
    excerpt = excerpt_lines[0][:100] + "..." if excerpt_lines else f"{product_name}を実際に使ってみたマリの正直レビュー。"
    
    # Frontmatterを作成
    frontmatter = f"""---
title: "{title}"
date: "{publish_date}"
excerpt: "{excerpt}"
{f'image: "{image_url}"' if image_url else ''}
tags: [{tags_str}]
{f'affiliateLink: "{affiliate_url}"' if affiliate_url else ''}
---

"""
    
    # ファイル名を作成（日付-商品名のスラッグ）
    slug = product_name.lower().replace(' ', '-').replace('　', '-')
    # 日本語を含む場合はそのまま使用（Markdownファイル名として問題ない）
    filename = f"{publish_date}-{slug}.md"
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


def input_product_info() -> dict:
    """
    対話形式で商品情報を入力
    
    Returns:
        商品情報の辞書
    """
    print("\n" + "=" * 80)
    print("📝 商品情報を入力してください")
    print("=" * 80 + "\n")
    
    product_info = {}
    
    product_info["name"] = input("商品名（必須）: ").strip()
    if not product_info["name"]:
        print("❌ 商品名は必須です。")
        sys.exit(1)
    
    product_info["price"] = input("価格（任意、例: 3,980円）: ").strip()
    product_info["features"] = input("特徴（任意、例: 静音設計、防水、USB充電式）: ").strip()
    product_info["category"] = input("カテゴリ（任意、例: バイブ、ローション、美容家電）: ").strip()
    product_info["image_url"] = input("商品画像URL（任意）: ").strip()
    product_info["affiliate_url"] = input("アフィリエイトリンク（任意）: ").strip()
    
    return product_info


def load_products_from_json(json_path: str) -> list[dict]:
    """
    JSONファイルから商品リストを読み込む
    
    Args:
        json_path: JSONファイルのパス
        
    Returns:
        商品情報のリスト
    """
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # JSONが配列の場合はそのまま、オブジェクトの場合はproductsキーを探す
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and "products" in data:
                return data["products"]
            else:
                print("❌ JSONファイルの形式が正しくありません。", file=sys.stderr)
                sys.exit(1)
    except FileNotFoundError:
        print(f"❌ ファイルが見つかりません: {json_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ JSONのパースに失敗: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """メイン処理"""
    print("\n" + "🌸" * 40)
    print("  マリのアダルトグッズレビュー記事生成ツール")
    print("🌸" * 40 + "\n")
    
    # 環境変数からAPIキーを取得
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ 環境変数 GEMINI_API_KEY が設定されていません", file=sys.stderr)
        sys.exit(1)
    
    # プロジェクトルートのパスを取得
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # 出力ディレクトリを作成
    content_dir = project_root / "content"
    content_dir.mkdir(exist_ok=True)
    
    # 入力モードの選択
    print("入力モードを選択してください:")
    print("  1. 対話形式で1つの商品を入力")
    print("  2. JSONファイルから複数の商品を読み込み")
    
    mode = input("\n選択（1 または 2）: ").strip()
    
    products = []
    
    if mode == "1":
        # 対話形式
        product_info = input_product_info()
        products.append(product_info)
    elif mode == "2":
        # JSONファイル
        json_path = input("JSONファイルのパス: ").strip()
        if not json_path:
            json_path = str(project_root / "products.json")
            print(f"デフォルトパスを使用: {json_path}")
        products = load_products_from_json(json_path)
        print(f"✅ {len(products)}件の商品を読み込みました。\n")
    else:
        print("❌ 無効な選択です。")
        sys.exit(1)
    
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
    model = genai.GenerativeModel("gemini-flash-latest")
    
    # 各商品について記事を生成
    print("\n✍️  記事生成を開始します...\n")
    
    success_count = 0
    for idx, product in enumerate(products):
        product_name = product.get("name", f"商品{idx+1}")
        
        print(f"[{idx + 1}/{len(products)}] {product_name}")
        print(f"  🔄 記事生成中...")
        
        # Gemini APIで記事を生成
        article_content = generate_article(model, product)
        
        if article_content:
            # 記事を保存
            filepath = save_article(article_content, product, publish_date, str(content_dir))
            
            if filepath:
                print(f"  ✅ 保存完了: {filepath}")
                success_count += 1
            else:
                print(f"  ❌ 保存失敗")
        else:
            print(f"  ❌ 生成失敗")
        
        # レート制限対策：複数商品の場合は4秒待機
        if len(products) > 1 and idx < len(products) - 1:
            print(f"  ⏳ レート制限対策で4秒待機中...\n")
            time.sleep(4)
        else:
            print()
    
    # 完了メッセージ
    print("=" * 80)
    print(f"🎉 記事生成完了！")
    print(f"   成功: {success_count}/{len(products)}件")
    print(f"   保存先: {content_dir}")
    print("=" * 80)


if __name__ == "__main__":
    main()

