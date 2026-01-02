#!/usr/bin/env python3
"""
MGS記事のフロントマターを正しく修正するスクリプト
"""

import re
from pathlib import Path

# プロジェクトルート
script_dir = Path(__file__).parent
project_root = script_dir.parent
content_dir = project_root / "content"

def fix_frontmatter(content: str) -> str:
    """フロントマターを正しく修正"""
    # URLを修正
    content = re.sub(r"https://\.mgstage\.com", "https://www.mgstage.com", content)
    
    # フロントマターが壊れている場合（`---\n---\n\ntitle:`の形式）
    if content.startswith("---\n---\n\n") or content.startswith("---\n---\n"):
        # 最初の2つの`---`を削除
        content = re.sub(r"^---\s*\n---\s*\n\s*", "", content)
    
    # `title:`で始まっている場合（最初の`---`が欠けている）
    if content.startswith("title:"):
        content = "---\n" + content
    
    # フロントマターが1行になっている場合
    if "--- title:" in content or (content.startswith("---") and "\n---\n" not in content[:500]):
        # フロントマターの開始と終了を検出
        # パターン: `--- title: ... ---` または `title: ... ---`
        match = re.search(r"(?:^---\s*)?(title:.*?)\s*---\s*", content, re.DOTALL)
        if match:
            frontmatter_raw = match.group(1)
            body_start = match.end()
            body = content[body_start:].strip()
        else:
            # 別のパターンを試す
            match = re.search(r"title:\s*\"([^\"]+)\".*?rating:\s*([\d.]+)\s*---", content, re.DOTALL)
            if match:
                # フロントマター部分を抽出
                frontmatter_end = content.find("---", content.find("rating:"))
                if frontmatter_end != -1:
                    frontmatter_raw = content[:frontmatter_end].replace("---", "").strip()
                    body = content[frontmatter_end + 3:].strip()
                else:
                    return content
            else:
                return content
    else:
        # 既に正しい形式の場合はそのまま返す
        if content.startswith("---\n") and "\n---\n" in content[:500]:
            return content
        return content
    
    # フロントマターをパースして整形
    frontmatter_lines = []
    frontmatter_lines.append("---")
    
    # キーと値を抽出
    patterns = [
        (r'title:\s*"([^"]+)"', 'title: "{}"'),
        (r'date:\s*"([^"]+)"', 'date: "{}"'),
        (r'excerpt:\s*"([^"]+)"', 'excerpt: "{}"'),
        (r'image:\s*"([^"]+)"', 'image: "{}"'),
        (r'tags:\s*(\[[^\]]+\])', 'tags: {}'),
        (r'affiliateLink:\s*"([^"]+)"', 'affiliateLink: "{}"'),
        (r'contentId:\s*"([^"]+)"', 'contentId: "{}"'),
        (r'rating:\s*([\d.]+)', 'rating: {}'),
    ]
    
    for pattern, format_str in patterns:
        match = re.search(pattern, frontmatter_raw)
        if match:
            value = match.group(1)
            frontmatter_lines.append(format_str.format(value))
    
    frontmatter_lines.append("---")
    frontmatter = "\n".join(frontmatter_lines)
    
    # 本文の改行を復元
    body = re.sub(r"<a\s+", "\n<a ", body)
    body = re.sub(r"</a>", "</a>\n", body)
    body = re.sub(r"<img\s+", "\n<img ", body)
    body = re.sub(r"/>\s*", "/>\n", body)
    body = re.sub(r"##\s+", "\n## ", body)
    body = re.sub(r"###\s+", "\n### ", body)
    
    # 余分な空白行を整理
    body = re.sub(r"\n\s*\n\s*\n+", "\n\n", body)
    body = body.strip()
    
    return frontmatter + "\n\n" + body

def main():
    """メイン処理"""
    print("=" * 80)
    print("  MGS記事のフロントマター修正")
    print("=" * 80 + "\n")
    
    # 2026-01-02の記事を取得
    mgs_articles = list(content_dir.glob("2026-01-02-*.md"))
    
    if not mgs_articles:
        print("❌ 修正対象の記事が見つかりません")
        return
    
    print(f"📋 {len(mgs_articles)}件の記事を確認します\n")
    
    fixed_count = 0
    skipped_count = 0
    
    for article_file in mgs_articles:
        try:
            with open(article_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 壊れているかチェック
            is_broken = (
                content.startswith("---\n---\n") or
                "--- title:" in content or
                "https://.mgstage.com" in content or
                (content.startswith("---") and content.count("\n---\n") == 0 and "title:" in content)
            )
            
            if not is_broken:
                # 正しい形式か確認
                if content.startswith("---\n") and "\n---\n" in content[:500]:
                    lines = content.split("\n")
                    if len(lines) > 2 and lines[0] == "---" and "---" in lines[1:10]:
                        print(f"⏭️  {article_file.name} - 修正不要")
                        skipped_count += 1
                        continue
            
            # 修正
            fixed_content = fix_frontmatter(content)
            
            # 保存
            with open(article_file, "w", encoding="utf-8") as f:
                f.write(fixed_content)
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

