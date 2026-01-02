#!/usr/bin/env python3
"""
YAMLフロントマターのエスケープ問題を修正するスクリプト
タイトルや抜粋内の特殊文字を適切にエスケープ
"""

import re
from pathlib import Path

# プロジェクトルート
script_dir = Path(__file__).parent
project_root = script_dir.parent
content_dir = project_root / "content"

def escape_yaml_string(s: str) -> str:
    """YAML文字列をエスケープ"""
    # バックスラッシュをエスケープ（最初に処理）
    s = s.replace("\\", "\\\\")
    # ダブルクォートをエスケープ
    s = s.replace('"', '\\"')
    # 改行をエスケープ
    s = s.replace("\n", "\\n")
    return s

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

def fix_article(filepath: Path) -> bool:
    """記事のYAMLエスケープを修正"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        frontmatter, body = extract_frontmatter(content)
        
        if not frontmatter:
            return False
        
        # タイトルと抜粋をエスケープ
        title = frontmatter.get("title", "")
        excerpt = frontmatter.get("excerpt", "")
        
        # バックスラッシュが含まれているかチェック
        needs_fix = False
        
        # バックスラッシュが含まれている場合（エスケープされていない可能性）
        # ただし、既に \\\\ のようにエスケープされている場合はスキップ
        if "\\" in title:
            # 単独の \ が含まれている場合（エスケープされていない）
            # \\ が含まれていても、それが \\\\ でない場合は修正が必要
            if title.count("\\") % 2 != 0 or (title.count("\\") > 0 and "\\\\" not in title.replace("\\\\", "")):
                needs_fix = True
        if "\\" in excerpt:
            if excerpt.count("\\") % 2 != 0 or (excerpt.count("\\") > 0 and "\\\\" not in excerpt.replace("\\\\", "")):
                needs_fix = True
        
        # ダブルクォートが含まれている場合も修正
        if '"' in title and '\\"' not in title:
            needs_fix = True
        if '"' in excerpt and '\\"' not in excerpt:
            needs_fix = True
        
        if not needs_fix:
            return False
        
        # エスケープ
        escaped_title = escape_yaml_string(title)
        escaped_excerpt = escape_yaml_string(excerpt)
        
        # フロントマターを再構築
        frontmatter_lines = ["---"]
        frontmatter_lines.append(f'title: "{escaped_title}"')
        frontmatter_lines.append(f'date: "{frontmatter.get("date", "")}"')
        frontmatter_lines.append(f'excerpt: "{escaped_excerpt}"')
        frontmatter_lines.append(f'image: "{frontmatter.get("image", "")}"')
        frontmatter_lines.append(f'tags: {frontmatter.get("tags", "[]")}')
        frontmatter_lines.append(f'affiliateLink: "{frontmatter.get("affiliateLink", "")}"')
        frontmatter_lines.append(f'contentId: "{frontmatter.get("contentId", "")}"')
        frontmatter_lines.append(f'rating: {frontmatter.get("rating", "4.0")}')
        if "source" in frontmatter:
            frontmatter_lines.append(f'source: "{frontmatter.get("source", "")}"')
        frontmatter_lines.append("---")
        
        new_content = "\n".join(frontmatter_lines) + "\n\n" + body
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        
        return True
        
    except Exception as e:
        print(f"❌ {filepath.name} - エラー: {e}")
        return False

def main():
    """メイン処理"""
    print("=" * 80)
    print("  YAMLエスケープ修正")
    print("=" * 80 + "\n")
    
    articles = list(content_dir.glob("*.md"))
    
    if not articles:
        print("❌ 記事が見つかりません")
        return
    
    print(f"📋 {len(articles)}件の記事をチェックします\n")
    
    fixed_count = 0
    checked_count = 0
    
    for article_file in articles:
        checked_count += 1
        if fix_article(article_file):
            print(f"✅ {article_file.name} - 修正完了")
            fixed_count += 1
        
        # 進捗表示（100件ごと）
        if checked_count % 100 == 0:
            print(f"📊 進捗: {checked_count}件チェック完了（修正: {fixed_count}件）\n")
    
    print("\n" + "=" * 80)
    print(f"🎉 修正完了！")
    print(f"   チェック: {checked_count}件")
    print(f"   修正: {fixed_count}件")
    print("=" * 80)

if __name__ == "__main__":
    main()

