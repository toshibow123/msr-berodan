#!/usr/bin/env python3
"""
MGS記事のYAMLフロントマターを修正するスクリプト
tagsを正しいYAML配列形式に修正
"""

import re
import json
from pathlib import Path

# プロジェクトルート
script_dir = Path(__file__).parent
project_root = script_dir.parent
content_dir = project_root / "content"

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

def main():
    """メイン処理"""
    print("=" * 80)
    print("  MGS記事のYAMLフロントマター修正")
    print("=" * 80 + "\n")
    
    mgs_articles = list(content_dir.glob("2026-01-02-*.md"))
    
    if not mgs_articles:
        print("❌ 修正対象の記事が見つかりません")
        return
    
    print(f"📋 {len(mgs_articles)}件の記事を修正します\n")
    
    fixed_count = 0
    skipped_count = 0
    
    for article_file in mgs_articles:
        try:
            with open(article_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            frontmatter, body = extract_frontmatter(content)
            
            if not frontmatter:
                print(f"⏭️  {article_file.name} - フロントマターが見つかりません")
                skipped_count += 1
                continue
            
            source = frontmatter.get("source", "")
            if source != "MGS":
                print(f"⏭️  {article_file.name} - MGS記事ではありません")
                skipped_count += 1
                continue
            
            # tagsを正しい形式に修正
            tags_str = frontmatter.get("tags", "[]")
            if isinstance(tags_str, str):
                # 文字列として保存されている場合
                if tags_str.startswith('"') and tags_str.endswith('"'):
                    # 二重引用符で囲まれている場合
                    tags_str = tags_str[1:-1]
                try:
                    tags = json.loads(tags_str)
                except:
                    # JSONとして解釈できない場合は空配列
                    tags = []
            else:
                tags = tags_str if isinstance(tags_str, list) else []
            
            # "MGS"タグを追加（まだない場合）
            if "MGS" not in tags:
                tags.append("MGS")
            
            # フロントマターを再構築（正しいYAML形式で）
            frontmatter_lines = ["---"]
            frontmatter_lines.append(f'title: "{frontmatter.get("title", "").replace('"', '\\"')}"')
            frontmatter_lines.append(f'date: "{frontmatter.get("date", "")}"')
            frontmatter_lines.append(f'excerpt: "{frontmatter.get("excerpt", "").replace('"', '\\"')}"')
            frontmatter_lines.append(f'image: "{frontmatter.get("image", "")}"')
            # tagsはYAML配列形式で出力（引用符で囲まない）
            frontmatter_lines.append(f'tags: {json.dumps(tags, ensure_ascii=False)}')
            frontmatter_lines.append(f'affiliateLink: "{frontmatter.get("affiliateLink", "")}"')
            frontmatter_lines.append(f'contentId: "{frontmatter.get("contentId", "")}"')
            frontmatter_lines.append(f'rating: {frontmatter.get("rating", "4.0")}')
            frontmatter_lines.append(f'source: "MGS"')
            frontmatter_lines.append("---")
            
            new_content = "\n".join(frontmatter_lines) + "\n\n" + body
            
            with open(article_file, "w", encoding="utf-8") as f:
                f.write(new_content)
            
            print(f"✅ {article_file.name} - 修正完了")
            fixed_count += 1
                
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

