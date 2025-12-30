#!/usr/bin/env python3
"""
failed_articles.jsonから記事を生成するスクリプト
"""

import json
import re
from pathlib import Path
from datetime import datetime
import random

def convert_work_to_info(work: dict, publish_date: str) -> dict:
    """workオブジェクトから記事生成用のinfo辞書に変換"""
    content_id = work.get("content_id", "")
    title = work.get("title", "")
    actress_list = work.get("actress", [])
    genre_list = work.get("genre", [])
    maker = work.get("maker", "")
    director = work.get("director", "")
    image_url = work.get("image_url", "")
    affiliate_url = work.get("affiliate_url", "")
    release_date = work.get("release_date", "")
    
    # 出演者を文字列に変換
    actress_str = "、".join(actress_list) if actress_list else "不明"
    
    # ジャンルを文字列に変換
    genre_str = "、".join(genre_list) if genre_list else "不明"
    
    # サンプル画像URLを生成（content_idから）
    sample_images = []
    for floor in ["videoa", "video"]:
        for i in range(1, 11):  # 1-10枚目
            sample_images.append(f"https://pics.dmm.co.jp/digital/{floor}/{content_id}/{content_id}jp-{i}.jpg")
    
    # 発売年を抽出
    year = ""
    if release_date:
        year_match = re.search(r'(\d{4})', release_date)
        if year_match:
            year = year_match.group(1)
    
    # タグを生成
    tags = []
    if year:
        tags.append(f"{year}年")
    if actress_list:
        tags.extend([actress for actress in actress_list[:2]])
    if genre_list:
        tags.extend([genre for genre in genre_list[:2] if genre not in tags])
    if maker:
        tags.append(maker)
    if len(tags) > 8:
        tags = tags[:8]
    
    return {
        "content_id": content_id,
        "title": title,
        "actress": actress_str,
        "genre": genre_str,
        "maker": maker,
        "director": director,
        "image_url": image_url,
        "affiliate_url": affiliate_url,
        "sample_images": sample_images,
        "tags": tags,
        "rating": round(random.uniform(4.0, 5.0), 1),
        "publish_date": publish_date,
        "year": year
    }


def generate_article_content(info: dict) -> str:
    """プロンプト情報から記事本文を生成"""
    
    # 詩的なタイトルの候補
    poetic_titles = [
        "成熟した女性の魅力が織りなす、禁断の物語",
        "心を揺さぶる、大人の色気",
        "静かに、しかし深く心に響く",
        "成熟した魅力に触れる瞬間",
        "物語の始まりに感じたもの",
        "彼女の佇まいに心奪われた",
        "この作品が語りかけるもの",
        "大人の色気が香り立つ一本"
    ]
    
    # 第一印象の見出し候補
    first_impression_headings = [
        "作品との出会い",
        "心を揺さぶる、禁断の物語",
        "大人の色気が香り立つ一本",
        "成熟した魅力に触れる瞬間",
        "静かに、しかし深く心に響く",
        "物語の始まりに感じたもの",
        "彼女の佇まいに心奪われた",
        "この作品が語りかけるもの"
    ]
    
    poetic_title = random.choice(poetic_titles)
    first_heading = random.choice(first_impression_headings)
    
    # サンプル画像を選択（最大5枚、ランダムに選択）
    all_images = info.get('sample_images', [])
    if all_images:
        # ランダムに4-5枚選択
        num_images = random.randint(4, 5)
        selected_images = random.sample(all_images, min(num_images, len(all_images)))
    else:
        selected_images = []
    
    # タイトルから具体的な設定を抽出
    title = info.get('title', '')
    title_keywords = []
    if '息子' in title or '友人' in title or '義' in title:
        title_keywords.append('家族関係の複雑さ')
    if '5年間' in title or '長期間' in title or '年' in title:
        title_keywords.append('長い時間をかけて育まれた関係')
    if 'セフレ' in title or '不倫' in title or '寝取' in title:
        title_keywords.append('禁断の関係')
    if '年下' in title:
        title_keywords.append('年齢差のある関係')
    if '人妻' in title or '主婦' in title or '妻' in title:
        title_keywords.append('家庭を持つ女性の内面')
    if '母親' in title or '妹' in title or '姉' in title:
        title_keywords.append('家族という関係性の重さ')
    if '教師' in title or '先生' in title:
        title_keywords.append('教育現場という特別な空間')
    if 'マッサージ' in title:
        title_keywords.append('施術という名の親密な時間')
    if 'バイト' in title or '職場' in title or '同僚' in title:
        title_keywords.append('日常の場面から始まる関係')
    
    # 記事本文を生成
    content = f"""## {poetic_title}

## {title}

<a href="{info.get('affiliate_url', '')}" target="_blank" rel="sponsored noopener noreferrer">
  <img src="{info.get('image_url', '')}" alt="{title}" />
</a>

**出演:** {info.get('actress', '不明')}
**ジャンル:** {info.get('genre', '')}
**メーカー:** {info.get('maker', '不明')}
{f"**監督:** {info.get('director', '')}" if info.get('director') else ''}

<div className="affiliate-link-inline">
  <a href="{info.get('affiliate_url', '')}" target="_blank" rel="noopener noreferrer">サンプル動画を見る</a>
</div>

<div style="width:100%; padding-top: 75%; position:relative; margin: 2rem 0;"><iframe width="100%" height="100%" max-width="1280px" style="position: absolute; top: 0; left: 0;" src="https://www.dmm.co.jp/litevideo/-/part/=/affi_id=toshichan-002/cid={info.get('content_id', '')}/size=1280_720/" scrolling="no" frameborder="0" allowfullscreen></iframe></div>

## {first_heading}

この作品に出会ったのは、ある静かな夜のことだった。{info.get('actress', '彼女')}という名前を見た瞬間、成熟した女性の魅力が画面から溢れ出てくるような予感がした。タイトルから読み取れる複雑な人間関係、禁断の物語の予感。これは単なる作品ではなく、人間の感情の深層を描き出す物語なのだろうと感じた。

画面に映し出された{info.get('actress', '彼女')}の佇まいは、まさに期待を裏切らないものだった。成熟した女性特有の落ち着きと、それでいて内に秘めた情熱が、彼女の表情から滲み出ている。最初のシーンから、この作品が語ろうとしている物語の重さを感じ取ることができた。

## 物語の魅力

この作品は、タイトルから読み取れる設定が、物語の核心をなしている。{', '.join(title_keywords) if title_keywords else '成熟した女性の内面'}というテーマが、どのように展開していくのか。その過程で描かれる感情の機微が、この作品の最大の魅力だ。

タイトルに込められた設定は、単なる刺激的な場面を超えて、人間の関係性の複雑さを描き出している。{info.get('actress', '彼女')}が演じる登場人物の内面、その葛藤や情熱が、丁寧に描かれていく。ストーリーの構成は、時間の流れに沿って丁寧に描かれている。日常的な場面から始まり、その後の展開へと自然に移行していく。{f"監督の{info.get('director', '')}による" if info.get('director') else ''}演出は、各シーンの意味を丁寧に積み重ねていく手法で、物語の深みを増していく。

"""
    
    # サンプル画像を追加（最初の1枚）
    if selected_images:
        content += f"""<a href="{info.get('affiliate_url', '')}" target="_blank" rel="sponsored noopener noreferrer">
  <img src="{selected_images[0]}" alt="{title}" />
</a>

"""
    
    content += f"""## 演技と演出の妙

{info.get('actress', '彼女')}の演技は、この作品の質を決定づける重要な要素だ。彼女の表情の変化、仕草の一つ一つが、登場人物の内面を丁寧に表現している。特に印象的だったのは、複雑な感情を抱えながらも、それを言葉にしない場面での演技だ。視線の動き、呼吸のリズム、それらすべてが物語を語っている。

{f"監督の{info.get('director', '')}による" if info.get('director') else ''}演出も、この作品の質を高めている。各シーンの構図、光の使い方、カメラワークの選択。すべてが物語のテーマを支えるために機能している。特に、感情の機微を表現する場面での演出は、見る者の心に深く響く。

作品がもたらす余韻は、観終わった後も長く心に残る。単なる刺激的な場面を超えて、人間の感情の複雑さ、関係性の難しさを描き出している。この作品は、成熟した作品を愛する視聴者にとって、心に響く一本となるだろう。

"""
    
    # 残りのサンプル画像を追加
    for img_url in selected_images[1:]:
        content += f"""<a href="{info.get('affiliate_url', '')}" target="_blank" rel="sponsored noopener noreferrer">
  <img src="{img_url}" alt="{title}" />
</a>

"""
    
    content += f"""<div className="affiliate-link-inline">
  <a href="{info.get('affiliate_url', '')}" target="_blank" rel="noopener noreferrer">この名作を確認する</a>
</div>

## 読者への語りかけ

この作品は、成熟した作品を愛する方にぜひ観ていただきたい一本だ。単なる刺激を求めるのではなく、物語の深み、演技の妙、演出の美しさを味わいたい方にとって、この作品は心に響く体験を提供してくれる。

{info.get('actress', '彼女')}の演技が描き出す、複雑な感情の機微。{f"監督の{info.get('director', '')}による" if info.get('director') else ''}丁寧な演出。それらが織りなす物語は、観る者の心に静かに、しかし深く響いていく。この作品がもたらす余韻は、観終わった後も長く心に残り続けるだろう。

成熟した作品の魅力を、洗練された言葉で語る。この作品は、まさにそのような作品の一つだ。ぜひ、この作品を手に取って、その魅力を堪能していただきたい。
"""
    
    return content


def generate_frontmatter(info: dict) -> str:
    """Frontmatterを生成"""
    publish_date = info.get('publish_date', datetime.now().strftime("%Y-%m-%d"))
    
    title = f"{info.get('title', '')} ー 名作を語る"
    excerpt = f"{info.get('title', '')}の熱いレビュー。名作を再評価する。"
    tags = info.get('tags', ['2025年'])
    tags_str = ", ".join([f'"{tag}"' for tag in tags])
    
    frontmatter = f"""---
title: "{title}"
date: "{publish_date}"
excerpt: "{excerpt}"
image: "{info.get('image_url', '')}"
tags: [{tags_str}]
affiliateLink: "{info.get('affiliate_url', '')}"
contentId: "{info.get('content_id', '')}"
rating: {info.get('rating', '4.0')}
---

"""
    return frontmatter


def main():
    """メイン処理"""
    import argparse
    
    parser = argparse.ArgumentParser(description="失敗記事から記事生成")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="既存記事を上書きする"
    )
    args = parser.parse_args()
    
    print("\n" + "=" * 80)
    print("  失敗記事から記事生成")
    print("=" * 80 + "\n")
    
    # ディレクトリ設定
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    data_dir = project_root / "data"
    content_dir = project_root / "content"
    
    content_dir.mkdir(exist_ok=True)
    
    # failed_articles.jsonを読み込む
    failed_file = data_dir / "failed_articles.json"
    if not failed_file.exists():
        print(f"❌ 失敗記事ファイルが見つかりません: {failed_file}", file=sys.stderr)
        sys.exit(1)
    
    with open(failed_file, "r", encoding="utf-8") as f:
        failed_articles = json.load(f)
    
    print(f"📖 {len(failed_articles)}件の失敗記事を読み込みました")
    if args.overwrite:
        print("⚠️  既存記事を上書きモードで実行します\n")
    else:
        print()
    
    # 記事生成
    success_count = 0
    skip_count = 0
    
    for idx, failed_item in enumerate(failed_articles, 1):
        content_id = failed_item.get("content_id", "")
        publish_date = failed_item.get("publish_date", datetime.now().strftime("%Y-%m-%d"))
        work = failed_item.get("work", {})
        
        print(f"[{idx}/{len(failed_articles)}] 📝 {content_id}")
        print(f"   作品名: {work.get('title', '不明')[:50]}...")
        
        # workオブジェクトからinfo辞書に変換
        info = convert_work_to_info(work, publish_date)
        
        # 既存記事のチェック
        filename = f"{publish_date}-{content_id}.md"
        existing_file = content_dir / filename
        
        if existing_file.exists() and not args.overwrite:
            print(f"   ⏭️  既存記事があるためスキップ")
            skip_count += 1
            continue
        elif existing_file.exists() and args.overwrite:
            print(f"   ⚠️  既存記事を上書きします")
        
        # 記事生成
        print(f"   ✍️  生成中...")
        frontmatter = generate_frontmatter(info)
        article_content = generate_article_content(info)
        full_content = frontmatter + article_content
        
        # 保存
        filepath = existing_file
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(full_content)
            print(f"   ✅ 保存完了: {filepath.name}")
            success_count += 1
        except Exception as e:
            print(f"   ❌ 保存失敗: {e}")
        
        print()
    
    # 完了メッセージ
    print("=" * 80)
    print("🎉 記事生成完了！")
    print("=" * 80)
    print(f"✅ 成功: {success_count}本")
    print(f"⏭️  スキップ: {skip_count}本")
    print(f"📁 保存先: {content_dir}")
    print("=" * 80)
    print()


if __name__ == "__main__":
    import sys
    main()

