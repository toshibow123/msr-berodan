#!/usr/bin/env python3
"""
記事の日付を1日20件ずつ再割り当てするスクリプト
"""

import os
from pathlib import Path
from datetime import datetime, timedelta
import re

def reassign_dates_20_per_day(content_dir: str, start_date_str: str = "2025-12-30", articles_per_day: int = 20):
    """記事の日付を1日20件ずつ再割り当て"""
    content_path = Path(content_dir)
    articles = sorted(content_path.glob("*.md"))
    
    total = len(articles)
    print(f"全記事数: {total}件")
    print(f"1日あたりの記事数: {articles_per_day}件")
    print(f"開始日: {start_date_str}")
    
    # 開始日を設定
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    current_date = start_date
    
    updated_count = 0
    
    for idx, article_path in enumerate(articles):
        try:
            with open(article_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 20件ごとに日付を進める
            if idx > 0 and idx % articles_per_day == 0:
                current_date += timedelta(days=1)
            
            # 現在の日付を取得
            current_date_str = current_date.strftime("%Y-%m-%d")
            
            # ファイル名を更新
            old_filename = article_path.name
            parts = old_filename.split('-')
            if len(parts) >= 4:
                # 日付部分（最初の3つ）を置き換え
                new_filename = f"{current_date_str}-{'-'.join(parts[3:])}"
            else:
                # ファイル名の形式が想定外の場合はスキップ
                print(f"⚠️  スキップ: {old_filename} (形式が想定外)")
                continue
            
            # 日付を置換（frontmatter内のdate）
            pattern = r'^date:\s*"[^"]*"'
            replacement = f'date: "{current_date_str}"'
            new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
            
            # ファイル名を変更
            new_filepath = article_path.parent / new_filename
            
            # ファイル名が変更される場合のみ移動
            if article_path != new_filepath:
                # 既に同じ名前のファイルが存在する場合はスキップ
                if new_filepath.exists():
                    print(f"⚠️  スキップ: {old_filename} -> {new_filename} (既に存在)")
                    continue
                
                # 内容を新しいファイルに書き込み
                with open(new_filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                # 古いファイルを削除
                article_path.unlink()
                
                updated_count += 1
                if (updated_count % 20 == 0) or (idx == len(articles) - 1):
                    print(f"✅ {updated_count}/{total}件更新完了 (現在の日付: {current_date_str})")
            else:
                # ファイル名は同じだが、内容を更新
                with open(article_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated_count += 1
                
        except Exception as e:
            print(f"❌ エラー ({article_path.name}): {e}")
            continue
    
    print("\n" + "=" * 80)
    print("🎉 日付再割り当て完了！")
    print("=" * 80)
    print(f"✅ 更新: {updated_count}件")
    print(f"📁 保存先: {content_dir}")
    print(f"📅 開始日: {start_date_str}")
    print(f"📅 最終日: {current_date.strftime('%Y-%m-%d')}")
    print(f"📊 1日あたり: {articles_per_day}件")
    print("=" * 80)
    print()


if __name__ == "__main__":
    import sys
    
    # デフォルト設定
    content_dir = "content"
    start_date = "2025-12-30"
    articles_per_day = 20
    
    # コマンドライン引数の処理
    if len(sys.argv) > 1:
        start_date = sys.argv[1]
    if len(sys.argv) > 2:
        articles_per_day = int(sys.argv[2])
    
    reassign_dates_20_per_day(content_dir, start_date, articles_per_day)

