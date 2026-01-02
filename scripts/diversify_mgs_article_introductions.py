#!/usr/bin/env python3
"""
MGS記事の導入部分を多様化するスクリプト
「静かな夜」などの重複した表現を修正
"""

import re
import json
import random
from pathlib import Path

# プロジェクトルート
script_dir = Path(__file__).parent
project_root = script_dir.parent
content_dir = project_root / "content"

# 多様化された導入文テンプレート
DIVERSIFIED_INTRODUCTIONS = [
    "この作品を手に取ったのは、偶然の出会いだった。タイトルから伝わってくる成熟した女性の魅力、そして禁断の物語の予感。単なる作品を超えた、人間の感情の深層を描き出す物語なのだろうと感じた。",
    "この作品との出会いは、予想外のものだった。タイトルから読み取れる複雑な人間関係、成熟した女性の内面が織りなす物語。これは刺激的な場面を超えて、心に響く物語を描き出している。",
    "この作品を発見したのは、ある日のことだった。タイトルから伝わってくる成熟した女性の魅力、そして禁断の物語の予感。これは単なる作品ではなく、人間の感情の深層を描き出す物語なのだろうと感じた。",
    "この作品に出会ったのは、ある時だった。タイトルから読み取れる設定が、物語の核心をなしている。成熟した女性の内面というテーマが、どのように展開していくのか。その過程で描かれる感情の機微が、この作品の最大の魅力だ。",
    "この作品を選んだのは、タイトルに惹かれたからだ。成熟した女性の魅力が画面から溢れ出てくるような予感がした。タイトルから読み取れる複雑な人間関係、禁断の物語の予感。これは単なる作品ではなく、人間の感情の深層を描き出す物語なのだろうと感じた。",
    "この作品との出会いは、偶然だった。タイトルから伝わってくる成熟した女性の魅力、そして禁断の物語の予感。これは単なる作品ではなく、人間の感情の深層を描き出す物語なのだろうと感じた。",
    "この作品を手に取ったのは、タイトルに興味を引かれたからだ。成熟した女性の魅力が画面から溢れ出てくるような予感がした。タイトルから読み取れる複雑な人間関係、禁断の物語の予感。これは単なる作品ではなく、人間の感情の深層を描き出す物語なのだろうと感じた。",
    "この作品を発見したのは、ある日のことだった。タイトルから読み取れる設定が、物語の核心をなしている。成熟した女性の内面というテーマが、どのように展開していくのか。その過程で描かれる感情の機微が、この作品の最大の魅力だ。",
    "この作品との出会いは、予想外のものだった。タイトルから伝わってくる成熟した女性の魅力、そして禁断の物語の予感。これは単なる作品ではなく、人間の感情の深層を描き出す物語なのだろうと感じた。",
    "この作品を選んだのは、タイトルに惹かれたからだ。タイトルから読み取れる設定が、物語の核心をなしている。成熟した女性の内面というテーマが、どのように展開していくのか。その過程で描かれる感情の機微が、この作品の最大の魅力だ。",
    "この作品を手に取ったのは、偶然の出会いだった。成熟した女性の魅力が画面から溢れ出てくるような予感がした。タイトルから読み取れる複雑な人間関係、禁断の物語の予感。これは単なる作品ではなく、人間の感情の深層を描き出す物語なのだろうと感じた。",
    "この作品との出会いは、ある時だった。タイトルから伝わってくる成熟した女性の魅力、そして禁断の物語の予感。これは単なる作品ではなく、人間の感情の深層を描き出す物語なのだろうと感じた。",
    "この作品を発見したのは、ある日のことだった。タイトルから読み取れる複雑な人間関係、成熟した女性の内面が織りなす物語。これは刺激的な場面を超えて、心に響く物語を描き出している。",
    "この作品を選んだのは、タイトルに興味を引かれたからだ。タイトルから読み取れる設定が、物語の核心をなしている。成熟した女性の内面というテーマが、どのように展開していくのか。その過程で描かれる感情の機微が、この作品の最大の魅力だ。",
    "この作品を手に取ったのは、偶然の出会いだった。タイトルから伝わってくる成熟した女性の魅力、そして禁断の物語の予感。これは単なる作品ではなく、人間の感情の深層を描き出す物語なのだろうと感じた。",
]

def extract_frontmatter(content: str) -> tuple[dict, str]:
    """フロントマターを抽出"""
    if not content.startswith("---"):
        return {}, content
    
    end_pos = content.find("\n---", 3)
    if end_pos == -1:
        return {}, content
    
    frontmatter_text = content[4:end_pos].strip()
    body = content[end_pos + 5:].strip()
    
    frontmatter = {}
    for line in frontmatter_text.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().strip('"')
            frontmatter[key] = value
    
    return frontmatter, body

def escape_yaml_string(s: str) -> str:
    """YAML文字列をエスケープ"""
    s = s.replace("\\", "\\\\")
    s = s.replace('"', '\\"')
    s = s.replace("\n", "\\n")
    return s

def fix_introduction(body: str) -> str:
    """導入部分を修正"""
    # まず「静かな夜」が含まれているか確認
    if "静かな夜" not in body:
        return body
    
    # 「心を揺さぶる、禁断の物語」セクションの後を探す
    section_match = re.search(r'## 心を揺さぶる、禁断の物語\s*\n\s*\n', body)
    if section_match:
        # セクションの後の部分を取得
        after_section = body[section_match.end():]
        # 「静かな夜」を含む最初の段落を探す（改行まで）
        para_match = re.search(r'^([^\n]*静かな夜[^\n]*。)', after_section, re.MULTILINE)
        if para_match:
            # ランダムに新しい導入文を選択
            new_intro = random.choice(DIVERSIFIED_INTRODUCTIONS)
            start_pos = section_match.end() + para_match.start()
            end_pos = section_match.end() + para_match.end()
            body = body[:start_pos] + new_intro + body[end_pos:]
            return body
    
    # フォールバック: 単純な置換パターン
    patterns = [
        r'この作品に出会ったのは、ある静かな夜のことだった[^。]*。',
        r'この作品に出会ったのは、ある静かな夜[^。]*。',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, body)
        if match:
            # ランダムに新しい導入文を選択
            new_intro = random.choice(DIVERSIFIED_INTRODUCTIONS)
            body = body[:match.start()] + new_intro + body[match.end():]
            break
    
    return body

def main():
    """メイン処理"""
    print("=" * 80)
    print("  MGS記事の導入部分を多様化")
    print("=" * 80 + "\n")
    
    # MGS記事のみを対象
    mgs_articles = []
    for article_file in content_dir.glob("*.md"):
        try:
            with open(article_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            frontmatter, _ = extract_frontmatter(content)
            source = frontmatter.get("source", "")
            
            if source == "MGS":
                mgs_articles.append(article_file)
        except:
            continue
    
    if not mgs_articles:
        print("❌ MGS記事が見つかりません")
        return
    
    print(f"📋 {len(mgs_articles)}件のMGS記事をチェックします\n")
    
    fixed_count = 0
    skipped_count = 0
    
    for article_file in mgs_articles:
        try:
            with open(article_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 「静かな夜」が含まれているかチェック
            if "静かな夜" not in content:
                skipped_count += 1
                continue
            
            frontmatter, body = extract_frontmatter(content)
            
            if not frontmatter:
                skipped_count += 1
                continue
            
            # 導入部分を修正
            new_body = fix_introduction(body)
            
            # 変更がない場合はスキップ
            if new_body == body:
                skipped_count += 1
                continue
            
            # フロントマターを再構築
            title = frontmatter.get("title", "")
            date = frontmatter.get("date", "")
            excerpt = frontmatter.get("excerpt", "")
            image = frontmatter.get("image", "")
            tags = frontmatter.get("tags", "[]")
            affiliate_link = frontmatter.get("affiliateLink", "")
            content_id = frontmatter.get("contentId", "")
            rating = frontmatter.get("rating", "4.0")
            source = frontmatter.get("source", "")
            
            # タグを正しく処理
            if isinstance(tags, str):
                try:
                    tags = json.loads(tags)
                except:
                    tags = []
            tags_str = json.dumps(tags, ensure_ascii=False)
            
            # エスケープ
            escaped_title = escape_yaml_string(title)
            escaped_excerpt = escape_yaml_string(excerpt)
            
            frontmatter_lines = ["---"]
            frontmatter_lines.append(f'title: "{escaped_title}"')
            frontmatter_lines.append(f'date: "{date}"')
            frontmatter_lines.append(f'excerpt: "{escaped_excerpt}"')
            frontmatter_lines.append(f'image: "{image}"')
            frontmatter_lines.append(f'tags: {tags_str}')
            frontmatter_lines.append(f'affiliateLink: "{affiliate_link}"')
            frontmatter_lines.append(f'contentId: "{content_id}"')
            frontmatter_lines.append(f'rating: {rating}')
            if source:
                frontmatter_lines.append(f'source: "{source}"')
            frontmatter_lines.append("---")
            
            new_content = "\n".join(frontmatter_lines) + "\n\n" + new_body
            
            # 保存
            with open(article_file, "w", encoding="utf-8") as f:
                f.write(new_content)
            
            print(f"✅ {article_file.name} - 導入部分を修正")
            fixed_count += 1
            
            # 進捗表示（100件ごと）
            if fixed_count % 100 == 0:
                print(f"\n📊 進捗: {fixed_count}件修正完了\n")
                
        except Exception as e:
            print(f"❌ {article_file.name} - エラー: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 80)
    print(f"🎉 修正完了！")
    print(f"   修正: {fixed_count}件")
    print(f"   スキップ: {skipped_count}件")
    print("=" * 80)

if __name__ == "__main__":
    main()

