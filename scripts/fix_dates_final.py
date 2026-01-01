#!/usr/bin/env python3
"""
日付を最終調整するスクリプト
- 2025-12-30と2025-12-31で300件
- 2026-01-01で20件
"""

import os
from pathlib import Path
from datetime import datetime
import re

def fix_dates_final(content_dir: str):
    """日付を最終調整"""
    content_path = Path(content_dir)
    all_files = sorted(content_path.glob("*.md"))
    
    # 日付別に分類
    date_files = {}
    for file in all_files:
        try:
            parts = file.stem.split('-')
            if len(parts) >= 3:
                date_str = '-'.join(parts[:3])
                if date_str not in date_files:
                    date_files[date_str] = []
                date_files[date_str].append(file)
        except:
            pass
    
    # 2025-12-30と2025-12-31の記事
    articles_1230 = sorted(date_files.get('2025-12-30', []))
    articles_1231 = sorted(date_files.get('2025-12-31', []))
    total_1230_1231 = len(articles_1230) + len(articles_1231)
    
    # 2026-01-01の記事
    articles_0101 = sorted(date_files.get('2026-01-01', []))
    
    print(f"現在の状況:")
    print(f"  2025-12-30: {len(articles_1230)}件")
    print(f"  2025-12-31: {len(articles_1231)}件")
    print(f"  合計: {total_1230_1231}件 (目標: 300件)")
    print(f"  2026-01-01: {len(articles_0101)}件 (目標: 20件)")
    
    # 2026-01-01が20件を超えている場合、超過分を2025-12-30に移動
    if len(articles_0101) > 20:
        excess = len(articles_0101) - 20
        print(f"\n📝 2026-01-01から{excess}件を2025-12-30に移動します...")
        
        for i in range(excess):
            article_path = articles_0101[20 + i]
            try:
                with open(article_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 日付を2025-12-30に変更
                pattern = r'^date:\s*"[^"]*"'
                replacement = 'date: "2025-12-30"'
                new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
                
                # ファイル名を変更
                old_filename = article_path.name
                parts = old_filename.split('-')
                if len(parts) >= 4:
                    new_filename = f"2025-12-30-{'-'.join(parts[3:])}"
                    new_filepath = article_path.parent / new_filename
                    
                    if not new_filepath.exists():
                        with open(new_filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        article_path.unlink()
                        print(f"  ✅ {old_filename} -> {new_filename}")
                    else:
                        print(f"  ⚠️  スキップ: {old_filename} (既に存在)")
            except Exception as e:
                print(f"  ❌ エラー ({article_path.name}): {e}")
    
    # 2025-12-30と2025-12-31で300件になるように調整
    # 再度日付別に分類
    date_files = {}
    for file in sorted(content_path.glob("*.md")):
        try:
            parts = file.stem.split('-')
            if len(parts) >= 3:
                date_str = '-'.join(parts[:3])
                if date_str not in date_files:
                    date_files[date_str] = []
                date_files[date_str].append(file)
        except:
            pass
    
    articles_1230 = sorted(date_files.get('2025-12-30', []))
    articles_1231 = sorted(date_files.get('2025-12-31', []))
    total_1230_1231 = len(articles_1230) + len(articles_1231)
    
    if total_1230_1231 < 300:
        needed = 300 - total_1230_1231
        print(f"\n📝 2025-12-30と2025-12-31に{needed}件追加して300件にします...")
        
        # 他の日付から記事を取得（2025-12-30, 2025-12-31, 2026-01-01以外）
        other_articles = []
        for date_str, files_list in date_files.items():
            if date_str not in ['2025-12-30', '2025-12-31', '2026-01-01']:
                other_articles.extend(files_list)
        
        other_articles = sorted(other_articles)
        
        for i in range(needed):
            if i >= len(other_articles):
                break
            article_path = other_articles[i]
            try:
                with open(article_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 150件ずつに分ける
                target_date = "2025-12-30" if len(articles_1230) < 150 else "2025-12-31"
                
                pattern = r'^date:\s*"[^"]*"'
                replacement = f'date: "{target_date}"'
                new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
                
                old_filename = article_path.name
                parts = old_filename.split('-')
                if len(parts) >= 4:
                    new_filename = f"{target_date}-{'-'.join(parts[3:])}"
                    new_filepath = article_path.parent / new_filename
                    
                    if not new_filepath.exists():
                        with open(new_filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        article_path.unlink()
                        if target_date == "2025-12-30":
                            articles_1230.append(new_filepath)
                        else:
                            articles_1231.append(new_filepath)
                        print(f"  ✅ {old_filename} -> {new_filename}")
            except Exception as e:
                print(f"  ❌ エラー ({article_path.name}): {e}")
    
    # 最終確認
    date_files = {}
    for file in sorted(content_path.glob("*.md")):
        try:
            parts = file.stem.split('-')
            if len(parts) >= 3:
                date_str = '-'.join(parts[:3])
                if date_str not in date_files:
                    date_files[date_str] = []
                date_files[date_str].append(file)
        except:
            pass
    
    articles_1230 = sorted(date_files.get('2025-12-30', []))
    articles_1231 = sorted(date_files.get('2025-12-31', []))
    articles_0101 = sorted(date_files.get('2026-01-01', []))
    
    print("\n" + "=" * 80)
    print("🎉 日付調整完了！")
    print("=" * 80)
    print(f"✅ 2025-12-30: {len(articles_1230)}件")
    print(f"✅ 2025-12-31: {len(articles_1231)}件")
    print(f"✅ 合計: {len(articles_1230) + len(articles_1231)}件 (目標: 300件)")
    print(f"✅ 2026-01-01: {len(articles_0101)}件 (目標: 20件)")
    print("=" * 80)
    print()


if __name__ == "__main__":
    import sys
    
    content_dir = "content"
    if len(sys.argv) > 1:
        content_dir = sys.argv[1]
    
    fix_dates_final(content_dir)

