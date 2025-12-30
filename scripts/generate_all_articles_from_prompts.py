#!/usr/bin/env python3
"""
プロンプトファイルから全記事を生成するスクリプト
各プロンプトファイルを読み込んで、記事を生成
"""

import re
from pathlib import Path
from datetime import datetime
import random

def parse_prompt_file(prompt_file: Path) -> dict:
    """プロンプトファイルから情報を抽出"""
    with open(prompt_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    info = {}
    
    # 作品データを抽出
    title_match = re.search(r'- 作品名：\s*(.+?)\n', content)
    if title_match:
        info['title'] = title_match.group(1).strip()
    
    content_id_match = re.search(r'- 作品ID：\s*(.+?)\n', content)
    if content_id_match:
        info['content_id'] = content_id_match.group(1).strip()
    
    affiliate_match = re.search(r'- アフィリエイトリンク：\s*(.+?)\n', content)
    if affiliate_match:
        info['affiliate_url'] = affiliate_match.group(1).strip()
    
    image_match = re.search(r'- メイン画像URL：\s*(.+?)\n', content)
    if image_match:
        info['image_url'] = image_match.group(1).strip()
    
    actress_match = re.search(r'- 出演：\s*(.+?)\n', content)
    if actress_match:
        info['actress'] = actress_match.group(1).strip()
    
    genre_match = re.search(r'- ジャンル：\s*(.+?)\n', content)
    if genre_match:
        info['genre'] = genre_match.group(1).strip()
    
    maker_match = re.search(r'- メーカー：\s*(.+?)\n', content)
    if maker_match:
        info['maker'] = maker_match.group(1).strip()
    
    director_match = re.search(r'- 監督：\s*(.+?)\n', content)
    if director_match:
        info['director'] = director_match.group(1).strip()
    
    # サンプル画像URLリストを抽出
    sample_images = []
    sample_section = re.search(r'- サンプル画像URLリスト：\s*\n((?:\s+\d+\.\s*.+?\n)+)', content)
    if sample_section:
        for line in sample_section.group(1).strip().split('\n'):
            url_match = re.search(r'\d+\.\s*(https?://.+?)(?:\s|$)', line)
            if url_match:
                sample_images.append(url_match.group(1).strip())
    info['sample_images'] = sample_images[:5]  # 最大5枚
    
    # Frontmatterから情報を抽出
    title_fm_match = re.search(r'title:\s*"(.+?)"', content)
    if title_fm_match:
        info['title_full'] = title_fm_match.group(1).strip()
    
    rating_match = re.search(r'rating:\s*([\d.]+)', content)
    if rating_match:
        info['rating'] = rating_match.group(1).strip()
    else:
        info['rating'] = str(round(random.uniform(4.0, 5.0), 1))
    
    tags_match = re.search(r'tags:\s*\[(.+?)\]', content)
    if tags_match:
        tags_str = tags_match.group(1).strip()
        # タグをパース
        tags = [t.strip().strip('"') for t in tags_str.split(',')]
        info['tags'] = tags
    
    # 保存パスを抽出（最後の`で囲まれたパスを取得）
    save_path_match = re.search(r'`([^`]+\.md)`', content)
    if save_path_match:
        info['save_path'] = save_path_match.group(1).strip()
    
    return info


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
    
    # サンプル画像を選択（最大4枚）
    selected_images = info.get('sample_images', [])[:4]
    
    # タイトルから具体的な設定を抽出
    title = info.get('title', '')
    title_keywords = []
    if '息子' in title or '友人' in title:
        title_keywords.append('家族関係の複雑さ')
    if '5年間' in title or '長期間' in title:
        title_keywords.append('長い時間をかけて育まれた関係')
    if 'セフレ' in title or '不倫' in title:
        title_keywords.append('禁断の関係')
    if '年下' in title:
        title_keywords.append('年齢差のある関係')
    if '人妻' in title or '主婦' in title:
        title_keywords.append('家庭を持つ女性の内面')
    if '母親' in title or '妹' in title:
        title_keywords.append('家族という関係性の重さ')
    
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

<a href="{info.get('affiliate_url', '')}" target="_blank" rel="sponsored noopener noreferrer">
  <img src="{selected_images[0] if selected_images else info.get('image_url', '')}" alt="{title}" />
</a>

## 演技と演出の妙

{info.get('actress', '彼女')}の演技は、この作品の質を決定づける重要な要素だ。彼女の表情の変化、仕草の一つ一つが、登場人物の内面を丁寧に表現している。特に印象的だったのは、複雑な感情を抱えながらも、それを言葉にしない場面での演技だ。視線の動き、呼吸のリズム、それらすべてが物語を語っている。

{f"監督の{info.get('director', '')}による" if info.get('director') else ''}演出も、この作品の質を高めている。各シーンの構図、光の使い方、カメラワークの選択。すべてが物語のテーマを支えるために機能している。特に、感情の機微を表現する場面での演出は、見る者の心に深く響く。

作品がもたらす余韻は、観終わった後も長く心に残る。単なる刺激的な場面を超えて、人間の感情の複雑さ、関係性の難しさを描き出している。この作品は、成熟した作品を愛する視聴者にとって、心に響く一本となるだろう。

"""
    
    # サンプル画像を追加
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
    today = datetime.now().strftime("%Y-%m-%d")
    
    title = info.get('title_full', f"{info.get('title', '')} ー 名作を語る")
    excerpt = f"{info.get('title', '')}の熱いレビュー。名作を再評価する。"
    tags = info.get('tags', ['2025年'])
    tags_str = ", ".join([f'"{tag}"' for tag in tags])
    
    frontmatter = f"""---
title: "{title}"
date: "{today}"
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
    print("\n" + "=" * 80)
    print("  プロンプトファイルから全記事生成")
    print("=" * 80 + "\n")
    
    # ディレクトリ設定
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    prompts_dir = project_root / "prompts"
    content_dir = project_root / "content"
    
    content_dir.mkdir(exist_ok=True)
    
    # プロンプトファイルのリスト
    prompt_files = [
        prompts_dir / "2025-12-30-jur00145-prompt.txt",
        prompts_dir / "2025-12-30-jur00408-prompt.txt",
        prompts_dir / "2025-12-30-venx00334-prompt.txt",
        prompts_dir / "2025-12-30-juq00871-prompt.txt",
        prompts_dir / "2025-12-30-1dandy00919e-prompt.txt",
        prompts_dir / "2025-12-30-juq00516-prompt.txt",
        prompts_dir / "2025-12-30-roe00233-prompt.txt",
        prompts_dir / "2025-12-30-hntrz00016-prompt.txt",
        prompts_dir / "2025-12-30-juq00799-prompt.txt",
        prompts_dir / "2025-12-30-mbyd00381-prompt.txt",
        prompts_dir / "2025-12-30-gma00081-prompt.txt",
        prompts_dir / "2025-12-30-nsfs00365-prompt.txt",
        prompts_dir / "2025-12-30-vec00655-prompt.txt",
        prompts_dir / "2025-12-30-juvr00209-prompt.txt",
        prompts_dir / "2025-12-30-jjda00052-prompt.txt",
        prompts_dir / "2025-12-30-juq00965-prompt.txt",
        prompts_dir / "2025-12-30-gma00054-prompt.txt",
        prompts_dir / "2025-12-30-h_086hone00286-prompt.txt",
        prompts_dir / "2025-12-30-jur00120-prompt.txt",
    ]
    
    # 存在するプロンプトファイルのみを処理
    existing_prompts = [f for f in prompt_files if f.exists()]
    
    print(f"📖 {len(existing_prompts)}件のプロンプトファイルを読み込みました\n")
    
    # 記事生成
    success_count = 0
    skip_count = 0
    
    for idx, prompt_file in enumerate(existing_prompts, 1):
        print(f"[{idx}/{len(existing_prompts)}] 📝 {prompt_file.name}")
        
        # プロンプトファイルから情報を抽出
        info = parse_prompt_file(prompt_file)
        title = info.get('title', '不明')[:50]
        print(f"   作品名: {title}...")
        
        # ファイルパスを決定
        today = datetime.now().strftime("%Y-%m-%d")
        if 'save_path' in info and info['save_path']:
            # 保存パスからファイル名を抽出
            save_path = info['save_path']
            if '/' in save_path:
                filename = save_path.split('/')[-1]
            else:
                filename = save_path
            existing_file = content_dir / filename
        else:
            existing_file = content_dir / f"{today}-{info.get('content_id', 'unknown')}.md"
        
        # 既存記事があっても上書きする（プロンプトファイルに基づいて再生成）
        if existing_file.exists():
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
    main()

