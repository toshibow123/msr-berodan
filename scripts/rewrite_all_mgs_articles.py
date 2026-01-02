#!/usr/bin/env python3
"""
全てのMGS記事をDMM記事と同じ構成・スタイルに書き直すスクリプト
MGS記事であることを識別できるようにタグを追加
"""

import re
from pathlib import Path
from datetime import datetime

# プロジェクトルート
script_dir = Path(__file__).parent
project_root = script_dir.parent
content_dir = project_root / "content"

def extract_frontmatter(content: str) -> tuple[dict, str]:
    """フロントマターを抽出"""
    if not content.startswith("---"):
        return {}, content
    
    # フロントマターの終了位置を探す
    end_pos = content.find("\n---", 3)
    if end_pos == -1:
        return {}, content
    
    frontmatter_text = content[4:end_pos].strip()
    body = content[end_pos + 5:].strip()
    
    # フロントマターをパース
    frontmatter = {}
    for line in frontmatter_text.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().strip('"')
            frontmatter[key] = value
    
    return frontmatter, body

def rewrite_article_content(frontmatter: dict, body: str) -> str:
    """記事本文をDMM記事と同じ構成・スタイルに書き直す"""
    title = frontmatter.get("title", "")
    image_url = frontmatter.get("image", "")
    affiliate_url = frontmatter.get("affiliateLink", "").replace("https://.mgstage.com", "https://www.mgstage.com")
    actresses = frontmatter.get("出演", "不明")
    genres = frontmatter.get("ジャンル", "不明")
    maker = frontmatter.get("メーカー", "不明")
    director = frontmatter.get("監督", "")
    
    # タグから出演者とジャンルを抽出
    tags_str = frontmatter.get("tags", "[]")
    if isinstance(tags_str, str):
        # JSON配列をパース
        import json
        try:
            tags = json.loads(tags_str)
        except:
            tags = []
    else:
        tags = tags_str
    
    # 出演者を抽出（タグから）
    exclude_tags = ["ネトラレ", "NTR", "2026年", "2025年", "2024年", "MGS", "人妻", "熟女", "ドラマ"]
    actress_list = [tag for tag in tags if tag not in exclude_tags]
    actresses = "、".join(actress_list[:2]) if actress_list else "不明"
    
    # ジャンルを抽出
    genre_list = [tag for tag in tags if tag in ["ネトラレ", "NTR", "人妻", "熟女", "ドラマ"]]
    genres = "、".join(genre_list) if genre_list else "ネトラレ"
    
    # 新しい記事本文を生成
    new_body = f"""## 成熟した女性の魅力が織りなす、禁断の物語

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

この作品に出会ったのは、ある静かな夜のことだった。タイトルから読み取れる複雑な人間関係、禁断の物語の予感。これは単なる作品ではなく、人間の感情の深層を描き出す物語なのだろうと感じた。

画面に映し出された{actresses}の佇まいは、まさに期待を裏切らないものだった。成熟した女性特有の落ち着きと、それでいて内に秘めた情熱が、彼女の表情から滲み出ている。最初のシーンから、この作品が語ろうとしている物語の重さを感じ取ることができた。

## 物語の魅力

この作品は、タイトルから読み取れる設定が、物語の核心をなしている。成熟した女性の内面というテーマが、どのように展開していくのか。その過程で描かれる感情の機微が、この作品の最大の魅力だ。

タイトルに込められた設定は、単なる刺激的な場面を超えて、人間の関係性の複雑さを描き出している。{actresses}が演じる登場人物の内面、その葛藤や情熱が、丁寧に描かれていく。ストーリーの構成は、時間の流れに沿って丁寧に描かれている。日常的な場面から始まり、その後の展開へと自然に移行していく。{f'監督の{director}による' if director else '監督による'}演出は、各シーンの意味を丁寧に積み重ねていく手法で、物語の深みを増していく。

物語は、成熟した女性が最初は抵抗を示しながらも、次第に内なる欲望に抗えなくなる過程を描いている。その心理的な変化が、丁寧に、そして繊細に描かれている。最初の抵抗から、徐々に理性が崩壊していく様子が、観る者の心に深く響いてくる。この作品が描き出す、人間の内面の複雑さと、欲望と理性の葛藤は、単なる刺激を超えた、深い物語性を持っている。

<a href="{affiliate_url}" target="_blank" rel="sponsored noopener noreferrer">
  <img src="{image_url}" alt="{title}" />
</a>

## 演技と演出の妙

{actresses}の演技は、この作品の質を決定づける重要な要素だ。彼女の表情の変化、仕草の一つ一つが、登場人物の内面を丁寧に表現している。特に印象的だったのは、複雑な感情を抱えながらも、それを言葉にしない場面での演技だ。視線の動き、呼吸のリズム、それらすべてが物語を語っている。

最初の抵抗から、次第に理性が崩壊していく過程での表情の変化は、見事なものだった。最初は気丈に振る舞っていた彼女が、次第に視線を泳がせ始める様子。口では抵抗の言葉を発しながらも、その声の震えが本心を物語っている。その微妙な心理の変化が、丁寧に、そして繊細に描かれている。

{f'監督の{director}による' if director else '監督による'}演出も、この作品の質を高めている。各シーンの構図、光の使い方、カメラワークの選択。すべてが物語のテーマを支えるために機能している。特に、感情の機微を表現する場面での演出は、見る者の心に深く響く。重苦しい空気が漂う場面での演出は、逆に作品の魅力を際立たせている。

作品がもたらす余韻は、観終わった後も長く心に残る。単なる刺激的な場面を超えて、人間の感情の複雑さ、関係性の難しさを描き出している。この作品は、成熟した作品を愛する視聴者にとって、心に響く一本となるだろう。

## 心に残るシーン

この作品には、特に印象的だったシーンがいくつかある。最初の抵抗から、次第に理性が崩壊していく過程での表情の変化は、見事なものだった。最初は気丈に振る舞っていた彼女が、次第に視線を泳がせ始める様子。口では抵抗の言葉を発しながらも、その声の震えが本心を物語っている。

特に印象的だったのは、最初の接触の場面だ。最初は反発して、目線を合わせようとしない彼女が、次第に視線を泳がせ始める瞬間。その微妙な心理の変化が、丁寧に、そして繊細に描かれている。口では「やめて…」と抵抗の言葉を発しながらも、その声の震えが、本心はすでに快楽の淵に片足を突っ込んでいることを物語っている。

さらに印象的だったのは、理性が完全に崩壊していく過程での描写だ。最初は絶望と怒りに満ちていた表情が、次第に羞恥心と同時に抗えない快感に、体が反応し始める様子。肉体が自分の意志とは裏腹に、求めるままに動き出す。この理性の崩壊が、丁寧に、そして繊細に描かれている。

感情的な場面での表現は、特に印象的だった。心理描写の深い場面では、登場人物の内面が最も表れた瞬間が描かれている。比喩的・文学的な表現で、想像力を掻き立てる。余韻を残す、詩的な文章で、あくまで「創作物の一場面」として描写されている。

<a href="{affiliate_url}" target="_blank" rel="sponsored noopener noreferrer">
  <img src="{image_url}" alt="{title}" />
</a>

<a href="{affiliate_url}" target="_blank" rel="sponsored noopener noreferrer">
  <img src="{image_url}" alt="{title}" />
</a>

<a href="{affiliate_url}" target="_blank" rel="sponsored noopener noreferrer">
  <img src="{image_url}" alt="{title}" />
</a>

<div className="affiliate-link-inline">
  <a href="{affiliate_url}" target="_blank" rel="noopener noreferrer">この名作を確認する</a>
</div>

## 読者への語りかけ

この作品は、成熟した作品を愛する方にぜひ観ていただきたい一本だ。単なる刺激を求めるのではなく、物語の深み、演技の妙、演出の美しさを味わいたい方にとって、この作品は心に響く体験を提供してくれる。

{actresses}の演技が描き出す、複雑な感情の機微。{f'監督の{director}による' if director else '監督による'}丁寧な演出。それらが織りなす物語は、観る者の心に静かに、しかし深く響いていく。この作品がもたらす余韻は、観終わった後も長く心に残り続けるだろう。

成熟した作品の魅力を、洗練された言葉で語る。この作品は、まさにそのような作品の一つだ。ぜひ、この作品を手に取って、その魅力を堪能していただきたい。
"""
    
    return new_body

def main():
    """メイン処理"""
    print("=" * 80)
    print("  全MGS記事の書き直し")
    print("=" * 80 + "\n")
    
    # 2026-01-02の記事を取得
    mgs_articles = list(content_dir.glob("2026-01-02-*.md"))
    
    if not mgs_articles:
        print("❌ 修正対象の記事が見つかりません")
        return
    
    print(f"📋 {len(mgs_articles)}件の記事を書き直します\n")
    
    rewritten_count = 0
    skipped_count = 0
    
    for article_file in mgs_articles:
        try:
            with open(article_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # フロントマターを抽出
            frontmatter, body = extract_frontmatter(content)
            
            if not frontmatter:
                print(f"⏭️  {article_file.name} - フロントマターが見つかりません")
                skipped_count += 1
                continue
            
            # MGS記事であることを識別できるようにタグを追加
            tags_str = frontmatter.get("tags", "[]")
            import json
            try:
                tags = json.loads(tags_str) if isinstance(tags_str, str) else tags_str
            except:
                tags = []
            
            # "MGS"タグを追加（まだない場合）
            if "MGS" not in tags:
                tags.append("MGS")
            
            # フロントマターにMGS識別用のフィールドを追加
            frontmatter["source"] = "MGS"
            
            # 記事本文を書き直す
            new_body = rewrite_article_content(frontmatter, body)
            
            # URLを修正
            affiliate_url = frontmatter.get("affiliateLink", "").replace("https://.mgstage.com", "https://www.mgstage.com")
            frontmatter["affiliateLink"] = affiliate_url
            
            # フロントマターを再構築
            frontmatter_lines = ["---"]
            frontmatter_lines.append(f'title: "{frontmatter.get("title", "")}"')
            frontmatter_lines.append(f'date: "{frontmatter.get("date", "")}"')
            frontmatter_lines.append(f'excerpt: "{frontmatter.get("excerpt", "")}"')
            frontmatter_lines.append(f'image: "{frontmatter.get("image", "")}"')
            frontmatter_lines.append(f'tags: {json.dumps(tags, ensure_ascii=False)}')
            frontmatter_lines.append(f'affiliateLink: "{affiliate_url}"')
            frontmatter_lines.append(f'contentId: "{frontmatter.get("contentId", "")}"')
            frontmatter_lines.append(f'rating: {frontmatter.get("rating", "4.0")}')
            frontmatter_lines.append(f'source: "MGS"')
            frontmatter_lines.append("---")
            
            new_content = "\n".join(frontmatter_lines) + "\n\n" + new_body
            
            # 保存
            with open(article_file, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"✅ {article_file.name} - 書き直し完了")
            rewritten_count += 1
                
        except Exception as e:
            print(f"❌ {article_file.name} - エラー: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 80)
    print(f"🎉 書き直し完了！")
    print(f"   書き直し: {rewritten_count}件")
    print(f"   スキップ: {skipped_count}件")
    print("=" * 80)

if __name__ == "__main__":
    main()

