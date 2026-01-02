#!/usr/bin/env python3
"""
未来の日付の記事を全て今日の日付に変更するスクリプト
"""

import re
import json
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
    print("  未来の日付を今日の日付に変更")
    print("=" * 80 + "\n")
    
    articles = list(content_dir.glob("*.md"))
    
    if not articles:
        print("❌ 記事が見つかりません")
        return
    
    # 今日の日付
    today = datetime.now().strftime("%Y-%m-%d")
    
    print(f"📅 今日の日付: {today}\n")
    print(f"📋 {len(articles)}件の記事をチェックします\n")
    
    fixed_count = 0
    skipped_count = 0
    
    for article_file in articles:
        try:
            with open(article_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            frontmatter, body = extract_frontmatter(content)
            
            if not frontmatter:
                skipped_count += 1
                continue
            
            article_date = frontmatter.get("date", "")
            if not article_date:
                skipped_count += 1
                continue
            
            # 未来の日付かチェック
            try:
                article_date_obj = datetime.strptime(article_date, "%Y-%m-%d")
                today_obj = datetime.strptime(today, "%Y-%m-%d")
                
                if article_date_obj <= today_obj:
                    skipped_count += 1
                    continue
            except:
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
            frontmatter_lines.append(f'date: "{today}"')
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
            new_filename = f"{today}-{content_id}.md"
            new_filepath = content_dir / new_filename
            
            # 既に同じファイル名が存在する場合は、連番を付ける
            counter = 1
            while new_filepath.exists() and new_filepath != article_file:
                new_filename = f"{today}-{content_id}-{counter}.md"
                new_filepath = content_dir / new_filename
                counter += 1
            
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

