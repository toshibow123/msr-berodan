#!/usr/bin/env python3
"""
品番（contentId）で重複している記事を削除
同じcontentIdを持つ記事が複数ある場合、古い日付の記事を削除
"""

import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

def extract_frontmatter(content: str):
    """フロントマターを抽出"""
    match = re.match(r'---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None, content
    
    frontmatter_str = match.group(1)
    body = content[match.end():]
    
    # 簡単なYAMLパース（contentIdとdateを取得）
    frontmatter = {}
    for line in frontmatter_str.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            frontmatter[key] = value
    
    return frontmatter, body

def main():
    print("=" * 80)
    print("  品番（contentId）で重複している記事を削除")
    print("=" * 80 + "\n")
    
    content_dir = Path("/Users/takahashitoshifumi/Desktop/Mrs-Adult/content")
    
    if not content_dir.exists():
        print(f"❌ ディレクトリが見つかりません: {content_dir}")
        return
    
    # contentIdごとに記事をグループ化
    articles_by_content_id = defaultdict(list)
    
    print("📋 記事をスキャン中...")
    for article_file in content_dir.glob("*.md"):
        try:
            content = article_file.read_text(encoding="utf-8")
            frontmatter, _ = extract_frontmatter(content)
            
            if not frontmatter:
                continue
            
            content_id = frontmatter.get("contentId", "").strip()
            date_str = frontmatter.get("date", "").strip().strip('"').strip("'")
            
            if not content_id:
                continue
            
            # 日付をパース
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            except:
                # 日付がパースできない場合は、ファイル名から取得
                match = re.search(r'(\d{4}-\d{2}-\d{2})', article_file.name)
                if match:
                    date_obj = datetime.strptime(match.group(1), "%Y-%m-%d")
                else:
                    date_obj = datetime.min
            
            articles_by_content_id[content_id].append({
                "file": article_file,
                "date": date_obj,
                "date_str": date_str
            })
            
        except Exception as e:
            print(f"⚠️  {article_file.name} の処理中にエラー: {e}")
    
    print(f"✅ {len(articles_by_content_id)}個のユニークな品番を発見\n")
    
    # 重複をチェック
    duplicates = {cid: articles for cid, articles in articles_by_content_id.items() if len(articles) > 1}
    
    if not duplicates:
        print("✅ 重複している記事はありませんでした。")
        return
    
    print(f"🔍 {len(duplicates)}個の品番で重複を発見\n")
    
    deleted_count = 0
    kept_count = 0
    
    for content_id, articles in duplicates.items():
        # 日付でソート（新しい順）
        articles.sort(key=lambda x: x["date"], reverse=True)
        
        # 最新の記事を残し、残りを削除
        kept_article = articles[0]
        to_delete = articles[1:]
        
        print(f"📦 {content_id}:")
        print(f"   ✅ 保持: {kept_article['file'].name} (日付: {kept_article['date_str']})")
        
        for article in to_delete:
            try:
                article["file"].unlink()
                print(f"   🗑️  削除: {article['file'].name} (日付: {article['date_str']})")
                deleted_count += 1
            except Exception as e:
                print(f"   ❌ 削除失敗: {article['file'].name} - {e}")
        
        kept_count += 1
        print()
    
    print("=" * 80)
    print(f"🎉 重複削除完了！")
    print(f"   保持: {kept_count}個の品番")
    print(f"   削除: {deleted_count}個の記事")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()

