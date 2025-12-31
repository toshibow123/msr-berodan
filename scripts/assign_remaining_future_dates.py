#!/usr/bin/env python3
"""
300件以外の残りの記事を2026-01-01から1日5件ずつ割り当てるスクリプト
"""

import os
from pathlib import Path
from datetime import datetime, timedelta
import re

def assign_remaining_future_dates(content_dir: str, skip_count: int = 300):
    """300件以外の残りの記事を2026-01-01から1日5件ずつ割り当て"""
    content_path = Path(content_dir)
    articles = sorted(content_path.glob("*.md"))
    
    total = len(articles)
    print(f"全記事数: {total}件")
    print(f"スキップ対象: {skip_count}件（昨日・今日の記事）")
    
    # 残りの記事を取得（300件以降）
    remaining_articles = articles[skip_count:]
    remaining_count = len(remaining_articles)
    
    print(f"更新対象: {remaining_count}件")
    
    # 2026-01-01から開始
    start_date = datetime(2026, 1, 1)
    current_date = start_date
    articles_per_day = 5
    
    updated_count = 0
    
    for idx, article_path in enumerate(remaining_articles):
        try:
            with open(article_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 現在の日付を取得
            current_date_str = current_date.strftime("%Y-%m-%d")
            
            # 5件ごとに日付を進める
            if idx > 0 and idx % articles_per_day == 0:
                current_date += timedelta(days=1)
                current_date_str = current_date.strftime("%Y-%m-%d")
            
            # 日付を置換
            pattern = r'^date:\s*"[^"]*"'
            replacement = f'date: "{current_date_str}"'
            
            new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
            
            # ファイル名も更新
            old_filename = article_path.name
            if re.match(r'^\d{4}-\d{2}-\d{2}-', old_filename):
                new_filename = re.sub(r'^\d{4}-\d{2}-\d{2}-', f'{current_date_str}-', old_filename)
                new_path = article_path.parent / new_filename
                
                # ファイルを書き込み
                with open(new_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                # 古いファイルを削除（ファイル名が変わった場合のみ）
                if new_path != article_path:
                    article_path.unlink()
                    print(f"✓ {old_filename} → {new_filename} ({current_date_str})")
                else:
                    print(f"✓ {old_filename} ({current_date_str})")
            else:
                # ファイル名に日付がない場合は内容のみ更新
                with open(article_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✓ {old_filename} ({current_date_str})")
            
            updated_count += 1
            
        except Exception as e:
            print(f"✗ エラー: {article_path.name} - {e}")
    
    print(f"\n更新完了:")
    print(f"  更新件数: {updated_count}件")
    print(f"  開始日: {start_date.strftime('%Y-%m-%d')}")
    print(f"  最終日: {current_date.strftime('%Y-%m-%d')}")
    print(f"  1日あたり: {articles_per_day}件")
    print(f"  日数: {(current_date - start_date).days + 1}日")

if __name__ == "__main__":
    content_dir = Path(__file__).parent.parent / "content"
    assign_remaining_future_dates(str(content_dir), skip_count=300)

