#!/usr/bin/env python3
"""
壊れたMGS記事を修正するスクリプト
フロントマターの改行を復元し、URLを修正
"""

import re
from pathlib import Path

# プロジェクトルート
script_dir = Path(__file__).parent
project_root = script_dir.parent
content_dir = project_root / "content"

def fix_broken_article(content: str) -> str:
    """壊れた記事を修正"""
    # URLを修正（https://.mgstage.com → https://www.mgstage.com）
    content = re.sub(r"https://\.mgstage\.com", "https://www.mgstage.com", content)
    
    # フロントマターの開始を検出
    if not content.startswith("---"):
        # 最初の`---`を探す
        match = re.search(r"^---\s*", content)
        if match:
            content = content[match.end():]
    
    # フロントマターの終了を検出
    frontmatter_end = content.find("---")
    if frontmatter_end == -1:
        # フロントマターが見つからない場合は、最初の`---`を探す
        frontmatter_end = content.find("\n---")
        if frontmatter_end != -1:
            frontmatter_end += 1
    
    if frontmatter_end == -1:
        # フロントマターが見つからない場合は、そのまま返す
        return content
    
    # フロントマター部分を抽出
    frontmatter_raw = content[:frontmatter_end].strip()
    body = content[frontmatter_end + 3:].strip()
    
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
    
    # 本文の改行を復元（`<a`や`<img`の前後に改行を追加）
    body = re.sub(r"<a\s+", "\n<a ", body)
    body = re.sub(r"</a>", "</a>\n", body)
    body = re.sub(r"<img\s+", "\n<img ", body)
    body = re.sub(r"/>", "/>\n", body)
    body = re.sub(r"##\s+", "\n## ", body)
    body = re.sub(r"###\s+", "\n### ", body)
    
    # 余分な空白行を整理
    body = re.sub(r"\n\s*\n\s*\n+", "\n\n", body)
    body = body.strip()
    
    return frontmatter + "\n\n" + body

def main():
    """メイン処理"""
    print("=" * 80)
    print("  壊れたMGS記事の修正")
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
            
            # 壊れているかチェック（フロントマターが1行になっている、またはURLが壊れている）
            is_broken = (
                "--- title:" in content or
                "https://.mgstage.com" in content or
                (content.count("---") < 2 and "title:" in content)
            )
            
            if not is_broken:
                print(f"⏭️  {article_file.name} - 修正不要")
                skipped_count += 1
                continue
            
            # 修正
            fixed_content = fix_broken_article(content)
            
            # 保存
            with open(article_file, "w", encoding="utf-8") as f:
                f.write(fixed_content)
            print(f"✅ {article_file.name} - 修正完了")
            fixed_count += 1
                
        except Exception as e:
            print(f"❌ {article_file.name} - エラー: {e}")
    
    print("\n" + "=" * 80)
    print(f"🎉 修正完了！")
    print(f"   修正: {fixed_count}件")
    print(f"   スキップ: {skipped_count}件")
    print("=" * 80)

if __name__ == "__main__":
    main()

