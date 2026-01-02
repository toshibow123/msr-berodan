#!/usr/bin/env python3
"""
MGSスクレイピングデータから、既存記事を参考にして記事を生成するスクリプト
APIを使わず、テンプレートベースで記事を生成
"""

import json
import random
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List

# プロジェクトルート
script_dir = Path(__file__).parent
project_root = script_dir.parent
data_dir = project_root / "data"
content_dir = project_root / "content"

# 既存記事のテンプレート文章（バリエーション）
TEMPLATE_INTRODUCTIONS = [
    "この作品に出会ったのは、ある静かな夜のことだった。タイトルから読み取れる複雑な人間関係、禁断の物語の予感。これは単なる作品ではなく、人間の感情の深層を描き出す物語なのだろうと感じた。",
    "この作品に出会ったのは、ある静かな夜のことだった。成熟した女性の魅力が画面から溢れ出てくるような予感がした。タイトルから読み取れる複雑な人間関係、禁断の物語の予感。これは単なる作品ではなく、人間の感情の深層を描き出す物語なのだろうと感じた。",
    "この作品に出会ったのは、ある静かな夜のことだった。タイトルから読み取れる設定が、物語の核心をなしている。成熟した女性の内面というテーマが、どのように展開していくのか。その過程で描かれる感情の機微が、この作品の最大の魅力だ。",
]

TEMPLATE_FIRST_IMPRESSIONS = [
    "画面に映し出された{actress}の佇まいは、まさに期待を裏切らないものだった。成熟した女性特有の落ち着きと、それでいて内に秘めた情熱が、彼女の表情から滲み出ている。最初のシーンから、この作品が語ろうとしている物語の重さを感じ取ることができた。",
    "画面に映し出された{actress}の佇まいは、まさに期待を裏切らないものだった。成熟した女性特有の落ち着きと、それでいて内に秘めた情熱が、彼女の表情から滲み出ている。最初のシーンから、この作品が語ろうとしている物語の重さを感じ取ることができた。",
    "画面に映し出された{actress}の佇まいは、まさに期待を裏切らないものだった。成熟した女性特有の落ち着きと、それでいて内に秘めた情熱が、彼女の表情から滲み出ている。最初のシーンから、この作品が語ろうとしている物語の重さを感じ取ることができた。",
]

TEMPLATE_STORY_CHARM = [
    "この作品は、タイトルから読み取れる設定が、物語の核心をなしている。成熟した女性の内面というテーマが、どのように展開していくのか。その過程で描かれる感情の機微が、この作品の最大の魅力だ。",
    "タイトルに込められた設定は、単なる刺激的な場面を超えて、人間の関係性の複雑さを描き出している。{actress}が演じる登場人物の内面、その葛藤や情熱が、丁寧に描かれていく。ストーリーの構成は、時間の流れに沿って丁寧に描かれている。日常的な場面から始まり、その後の展開へと自然に移行していく。監督による演出は、各シーンの意味を丁寧に積み重ねていく手法で、物語の深みを増していく。",
    "物語は、成熟した女性が最初は抵抗を示しながらも、次第に内なる欲望に抗えなくなる過程を描いている。その心理的な変化が、丁寧に、そして繊細に描かれている。最初の抵抗から、徐々に理性が崩壊していく様子が、観る者の心に深く響いてくる。この作品が描き出す、人間の内面の複雑さと、欲望と理性の葛藤は、単なる刺激を超えた、深い物語性を持っている。",
]

TEMPLATE_ACTING = [
    "{actress}の演技は、この作品の質を決定づける重要な要素だ。彼女の表情の変化、仕草の一つ一つが、登場人物の内面を丁寧に表現している。特に印象的だったのは、複雑な感情を抱えながらも、それを言葉にしない場面での演技だ。視線の動き、呼吸のリズム、それらすべてが物語を語っている。",
    "最初の抵抗から、次第に理性が崩壊していく過程での表情の変化は、見事なものだった。最初は気丈に振る舞っていた彼女が、次第に視線を泳がせ始める様子。口では抵抗の言葉を発しながらも、その声の震えが本心を物語っている。その微妙な心理の変化が、丁寧に、そして繊細に描かれている。",
    "監督による演出も、この作品の質を高めている。各シーンの構図、光の使い方、カメラワークの選択。すべてが物語のテーマを支えるために機能している。特に、感情の機微を表現する場面での演出は、見る者の心に深く響く。重苦しい空気が漂う場面での演出は、逆に作品の魅力を際立たせている。",
    "作品がもたらす余韻は、観終わった後も長く心に残る。単なる刺激的な場面を超えて、人間の感情の複雑さ、関係性の難しさを描き出している。この作品は、成熟した作品を愛する視聴者にとって、心に響く一本となるだろう。",
]

TEMPLATE_MEMORABLE_SCENES = [
    "この作品には、特に印象的だったシーンがいくつかある。最初の抵抗から、次第に理性が崩壊していく過程での表情の変化は、見事なものだった。最初は気丈に振る舞っていた彼女が、次第に視線を泳がせ始める様子。口では抵抗の言葉を発しながらも、その声の震えが本心を物語っている。",
    "特に印象的だったのは、最初の接触の場面だ。最初は反発して、目線を合わせようとしない彼女が、次第に視線を泳がせ始める瞬間。その微妙な心理の変化が、丁寧に、そして繊細に描かれている。口では「やめて…」と抵抗の言葉を発しながらも、その声の震えが、本心はすでに快楽の淵に片足を突っ込んでいることを物語っている。",
    "さらに印象的だったのは、理性が完全に崩壊していく過程での描写だ。最初は絶望と怒りに満ちていた表情が、次第に羞恥心と同時に抗えない快感に、体が反応し始める様子。肉体が自分の意志とは裏腹に、求めるままに動き出す。この理性の崩壊が、丁寧に、そして繊細に描かれている。",
    "感情的な場面での表現は、特に印象的だった。心理描写の深い場面では、登場人物の内面が最も表れた瞬間が描かれている。比喩的・文学的な表現で、想像力を掻き立てる。余韻を残す、詩的な文章で、あくまで「創作物の一場面」として描写されている。",
]

TEMPLATE_READER_MESSAGE = [
    "この作品は、成熟した作品を愛する方にぜひ観ていただきたい一本だ。単なる刺激を求めるのではなく、物語の深み、演技の妙、演出の美しさを味わいたい方にとって、この作品は心に響く体験を提供してくれる。",
    "{actress}の演技が描き出す、複雑な感情の機微。監督による丁寧な演出。それらが織りなす物語は、観る者の心に静かに、しかし深く響いていく。この作品がもたらす余韻は、観終わった後も長く心に残り続けるだろう。",
    "成熟した作品の魅力を、洗練された言葉で語る。この作品は、まさにそのような作品の一つだ。ぜひ、この作品を手に取って、その魅力を堪能していただきたい。",
]

def load_mgs_data(json_path: Path) -> List[Dict]:
    """MGSスクレイピングデータを読み込む"""
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("ranking", [])
    except Exception as e:
        print(f"❌ データの読み込みエラー: {e}")
        return []

def generate_sample_image_urls(image_url: str, content_id: str, count: int = 3) -> List[str]:
    """サンプル画像URLを生成"""
    if not image_url or "image.mgstage.com" not in image_url:
        return []
    
    match = re.search(r'https://image\.mgstage\.com/images/(.+?)/(.+?)/(.+?)/', image_url)
    if not match:
        return []
    
    maker = match.group(1)
    series = match.group(2)
    id_part = match.group(3)
    content_id_lower = content_id.lower()
    
    sample_urls = []
    for i in range(1, count + 1):
        sample_url = f"https://image.mgstage.com/images/{maker}/{series}/{id_part}/cap_e_{i}_{content_id_lower}.jpg"
        sample_urls.append(sample_url)
    
    return sample_urls

def generate_article_content(product_info: Dict) -> str:
    """記事本文を生成"""
    title = product_info.get("title", "")
    image_url = product_info.get("image_url", "")
    affiliate_url = product_info.get("affiliate_url", "")
    content_id = product_info.get("content_id", "")
    actress_list = product_info.get("actress", [])
    genre_list = product_info.get("genre", [])
    maker = product_info.get("maker", "")
    director = product_info.get("director", "")
    
    actresses = "、".join(actress_list[:2]) if actress_list else "不明"
    genres = "、".join(genre_list) if genre_list else "不明"
    
    # サンプル画像URLを生成
    sample_urls = generate_sample_image_urls(image_url, content_id, count=3)
    if not sample_urls:
        sample_urls = [image_url] * 3
    
    # テンプレートからランダムに選択
    introduction = random.choice(TEMPLATE_INTRODUCTIONS)
    first_impression = random.choice(TEMPLATE_FIRST_IMPRESSIONS).format(actress=actresses)
    story_charm = random.choice(TEMPLATE_STORY_CHARM).format(actress=actresses)
    acting = random.choice(TEMPLATE_ACTING).format(actress=actresses)
    memorable_scenes = random.choice(TEMPLATE_MEMORABLE_SCENES)
    reader_message = random.choice(TEMPLATE_READER_MESSAGE).format(actress=actresses)
    
    # 記事本文を構築
    content = f"""## 成熟した女性の魅力が織りなす、禁断の物語

## {title}

<a href="{affiliate_url}" target="_blank" rel="sponsored noopener noreferrer">
  <img src="{image_url}" alt="{title}" />
</a>

**出演:** {actresses}
**ジャンル:** {genres}
**メーカー:** {maker if maker else "不明"}
{f'**監督:** {director}' if director else ''}

<div className="affiliate-link-inline">
  <a href="{affiliate_url}" target="_blank" rel="noopener noreferrer">作品の詳細を見る</a>
</div>

## 心を揺さぶる、禁断の物語

{introduction}

{first_impression}

## 物語の魅力

{story_charm}

<a href="{affiliate_url}" target="_blank" rel="sponsored noopener noreferrer">
  <img src="{sample_urls[0]}" alt="{title}" />
</a>

## 演技と演出の妙

{acting}

## 心に残るシーン

{memorable_scenes}

<div className="affiliate-link-inline">
  <a href="{affiliate_url}" target="_blank" rel="noopener noreferrer">この名作を確認する</a>
</div>

<a href="{affiliate_url}" target="_blank" rel="sponsored noopener noreferrer">
  <img src="{sample_urls[1]}" alt="{title}" />
</a>

<a href="{affiliate_url}" target="_blank" rel="sponsored noopener noreferrer">
  <img src="{sample_urls[2]}" alt="{title}" />
</a>

<a href="{affiliate_url}" target="_blank" rel="sponsored noopener noreferrer">
  <img src="{sample_urls[0]}" alt="{title}" />
</a>


## 読者への語りかけ

{reader_message}
"""
    
    return content

def create_tags(product_info: Dict) -> List[str]:
    """タグを作成"""
    tags = []
    
    # 検索キーワード
    search_keyword = product_info.get("search_keyword", "")
    if search_keyword:
        tags.append(search_keyword)
    
    # 発売年
    release_date = product_info.get("release_date", "")
    if release_date:
        try:
            year = release_date.split("-")[0]
            tags.append(f"{year}年")
        except:
            pass
    
    # ジャンル
    genre_list = product_info.get("genre", [])
    tags.extend(genre_list)
    
    # タイトルからジャンルを推測
    title = product_info.get("title", "")
    if "NTR" in title or "ネトラレ" in title or "寝取" in title:
        if "NTR" not in tags and "ネトラレ" not in tags:
            tags.append("ネトラレ")
    if "人妻" in title:
        if "人妻" not in tags:
            tags.append("人妻")
    if "熟女" in title:
        if "熟女" not in tags:
            tags.append("熟女")
    if "ドラマ" in title:
        if "ドラマ" not in tags:
            tags.append("ドラマ")
    
    # MGSタグ
    tags.append("MGS")
    
    # タグ数制限（最大15個まで）
    return tags[:15]

def escape_yaml_string(s: str) -> str:
    """YAML文字列をエスケープ"""
    # バックスラッシュをエスケープ
    s = s.replace("\\", "\\\\")
    # ダブルクォートをエスケープ
    s = s.replace('"', '\\"')
    # 改行をエスケープ
    s = s.replace("\n", "\\n")
    return s

def generate_article(product_info: Dict, publish_date: str) -> str:
    """記事全体を生成"""
    title = product_info.get("title", "")
    image_url = product_info.get("image_url", "")
    affiliate_url = product_info.get("affiliate_url", "")
    content_id = product_info.get("content_id", "")
    
    # タイトルと抜粋をエスケープ
    escaped_title = escape_yaml_string(title)
    
    # タグを作成
    tags = create_tags(product_info)
    tags_str = json.dumps(tags, ensure_ascii=False)
    
    # 抜粋を生成
    excerpt = f"{title}のレビュー。成熟した女性の魅力が織りなす、禁断の物語。"
    escaped_excerpt = escape_yaml_string(excerpt)
    
    # 評価を生成
    rating = round(random.uniform(4.0, 5.0), 1)
    
    # フロントマターを作成
    frontmatter = f"""---
title: "{escaped_title}"
date: "{publish_date}"
excerpt: "{escaped_excerpt}"
image: "{image_url}"
tags: {tags_str}
affiliateLink: "{affiliate_url}"
contentId: "{content_id}"
rating: {rating}
source: "MGS"
---

"""
    
    # 記事本文を生成
    content = generate_article_content(product_info)
    
    return frontmatter + content

def main():
    """メイン処理"""
    print("=" * 80)
    print("  MGS記事生成（テンプレートベース）")
    print("=" * 80 + "\n")
    
    # データファイルを読み込む
    data_file = data_dir / "mgs_scraped_data.json"
    if not data_file.exists():
        print(f"❌ データファイルが見つかりません: {data_file}")
        return
    
    products = load_mgs_data(data_file)
    if not products:
        print("❌ データが空です")
        return
    
    print(f"📋 {len(products)}件のデータを読み込みました\n")
    
    # 既存記事のcontent_idを取得（重複チェック用）
    existing_articles = set()
    for article_file in content_dir.glob("*.md"):
        match = re.search(r'(\d{4}-\d{2}-\d{2})-(.+)\.md', article_file.name)
        if match:
            existing_articles.add(match.group(2))
    
    print(f"📝 既存記事: {len(existing_articles)}件\n")
    
    # 記事を生成
    generated_count = 0
    skipped_count = 0
    
    # 今日から順に日付を割り当て
    base_date = datetime.now()
    
    for idx, product in enumerate(products):
        content_id = product.get("content_id", "")
        
        if not content_id:
            skipped_count += 1
            continue
        
        # 既存記事をスキップ
        if content_id in existing_articles:
            skipped_count += 1
            continue
        
        # 日付を決定（既存記事の日付を避ける）
        publish_date = (base_date + timedelta(days=idx)).strftime("%Y-%m-%d")
        
        try:
            # 記事を生成
            article_content = generate_article(product, publish_date)
            
            # ファイル名を作成
            filename = f"{publish_date}-{content_id}.md"
            filepath = content_dir / filename
            
            # 保存
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(article_content)
            
            print(f"✅ {filename} - 生成完了")
            generated_count += 1
            
            # 進捗表示（100件ごと）
            if generated_count % 100 == 0:
                print(f"\n📊 進捗: {generated_count}件生成完了\n")
                
        except Exception as e:
            print(f"❌ {content_id} - エラー: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 80)
    print(f"🎉 記事生成完了！")
    print(f"   生成: {generated_count}件")
    print(f"   スキップ: {skipped_count}件")
    print("=" * 80)

if __name__ == "__main__":
    main()

