#!/usr/bin/env python3
"""
記事の日付を適切な範囲に修正するスクリプト
未来の日付を今日以降の適切な日付に修正
"""

import re
import json
from pathlib import Path
from datetime import datetime, timedelta

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

def escape_yaml_string(s: str) -> str:
    """YAML文字列をエスケープ"""
    s = s.replace("\\", "\\\\")
    s = s.replace('"', '\\"')
    s = s.replace("\n", "\\n")
    return s

def main():
    """メイン処理"""
    print("=" * 80)
    print("  記事の日付修正")
    print("=" * 80 + "\n")
    
    articles = list(content_dir.glob("*.md"))
    
    if not articles:
        print("❌ 記事が見つかりません")
        return
    
    print(f"📋 {len(articles)}件の記事をチェックします\n")
    
    # 今日の日付
    today = datetime.now()
    
    # 日付を修正する必要がある記事を探す
    fixed_count = 0
    skipped_count = 0
    
    # 日付ごとに記事をグループ化
    date_groups = {}
    for article_file in articles:
        match = re.search(r'(\d{4}-\d{2}-\d{2})', article_file.name)
        if match:
            date_str = match.group(1)
            if date_str not in date_groups:
                date_groups[date_str] = []
            date_groups[date_str].append(article_file)
    
    # 未来の日付の記事を今日以降に再配置
    future_articles = []
    for date_str, files in sorted(date_groups.items()):
        article_date = datetime.strptime(date_str, "%Y-%m-%d")
        if article_date > today:
            future_articles.extend(files)
    
    print(f"📅 未来の日付の記事: {len(future_articles)}件\n")
    
    # 今日から順に日付を割り当て
    current_date = today
    day_offset = 0
    
    for article_file in sorted(future_articles):
        try:
            with open(article_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            frontmatter, body = extract_frontmatter(content)
            
            if not frontmatter:
                skipped_count += 1
                continue
            
            # 新しい日付を決定
            new_date = (current_date + timedelta(days=day_offset)).strftime("%Y-%m-%d")
            day_offset += 1
            
            # 既に適切な日付の場合はスキップ
            old_date = frontmatter.get("date", "")
            if old_date == new_date:
                skipped_count += 1
                continue
            
            # フロントマターを再構築
            title = frontmatter.get("title", "")
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
            frontmatter_lines.append(f'date: "{new_date}"')
            frontmatter_lines.append(f'excerpt: "{escaped_excerpt}"')
            frontmatter_lines.append(f'image: "{image}"')
            frontmatter_lines.append(f'tags: {tags_str}')
            frontmatter_lines.append(f'affiliateLink: "{affiliate_link}"')
            frontmatter_lines.append(f'contentId: "{content_id}"')
            frontmatter_lines.append(f'rating: {rating}')
            if source:
                frontmatter_lines.append(f'source: "{source}"')
            frontmatter_lines.append("---")
            
            new_content = "\n".join(frontmatter_lines) + "\n\n" + body
            
            # 新しいファイル名を作成
            new_filename = f"{new_date}-{content_id}.md"
            new_filepath = content_dir / new_filename
            
            # 既に同じファイル名が存在する場合はスキップ
            if new_filepath.exists() and new_filepath != article_file:
                print(f"⏭️  {article_file.name} - 既に存在: {new_filename}")
                skipped_count += 1
                continue
            
            # 保存
            with open(new_filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            
            # 古いファイルを削除（ファイル名が変わった場合）
            if article_file != new_filepath:
                article_file.unlink()
            
            print(f"✅ {article_file.name} -> {new_filename} - 日付修正完了")
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

