#!/usr/bin/env python3
"""
記事の日付を昨日と今日に更新するスクリプト
300件の記事を2日間に分散
"""

import os
from pathlib import Path
from datetime import datetime, timedelta
import re

def update_article_dates(content_dir: str):
    """記事の日付を更新"""
    content_path = Path(content_dir)
    articles = sorted(content_path.glob("*.md"))
    
    total = len(articles)
    print(f"記事数: {total}件")
    
    # 昨日と今日の日付
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    
    today_str = today.strftime("%Y-%m-%d")
    yesterday_str = yesterday.strftime("%Y-%m-%d")
    
    print(f"今日: {today_str}")
    print(f"昨日: {yesterday_str}")
    
    # 半分ずつに分ける
    half = total // 2
    
    updated_today = 0
    updated_yesterday = 0
    
    for idx, article_path in enumerate(articles):
        try:
            with open(article_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 日付を決定（前半は昨日、後半は今日）
            if idx < half:
                new_date = yesterday_str
                updated_yesterday += 1
            else:
                new_date = today_str
                updated_today += 1
            
            # 日付を置換
            # date: "YYYY-MM-DD" のパターンを置換
            pattern = r'^date:\s*"[^"]*"'
            replacement = f'date: "{new_date}"'
            
            new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
            
            # ファイル名も更新（オプション）
            # ファイル名の日付部分を更新
            old_filename = article_path.name
            if re.match(r'^\d{4}-\d{2}-\d{2}-', old_filename):
                # 日付部分を抽出して置換
                new_filename = re.sub(r'^\d{4}-\d{2}-\d{2}-', f'{new_date}-', old_filename)
                new_path = article_path.parent / new_filename
                
                # ファイルを書き込み
                with open(new_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                # 古いファイルを削除（ファイル名が変わった場合のみ）
                if new_path != article_path:
                    article_path.unlink()
                    print(f"✓ {old_filename} → {new_filename} ({new_date})")
                else:
                    print(f"✓ {old_filename} ({new_date})")
            else:
                # ファイル名に日付がない場合は内容のみ更新
                with open(article_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✓ {old_filename} ({new_date})")
                
        except Exception as e:
            print(f"✗ エラー: {article_path.name} - {e}")
    
    print(f"\n更新完了:")
    print(f"  昨日 ({yesterday_str}): {updated_yesterday}件")
    print(f"  今日 ({today_str}): {updated_today}件")
    print(f"  合計: {updated_yesterday + updated_today}件")

if __name__ == "__main__":
    content_dir = Path(__file__).parent.parent / "content"
    update_article_dates(str(content_dir))

