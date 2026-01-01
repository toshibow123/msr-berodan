#!/usr/bin/env python3
"""
記事の日付をカスタムルールで再割り当てするスクリプト
- 2025-12-30と2025-12-31で300件
- 2026-01-01は既存5件を維持し、追加15件で合計20件
- 残りを2026-01-02から1日20件ずつ割り当て
"""

import os
from pathlib import Path
from datetime import datetime, timedelta
import re

def reassign_dates_custom(content_dir: str):
    """記事の日付をカスタムルールで再割り当て"""
    content_path = Path(content_dir)
    all_articles = sorted(content_path.glob("*.md"))
    
    total = len(all_articles)
    print(f"全記事数: {total}件")
    
    # 日付別に分類
    date_files = {}
    for file in all_articles:
        try:
            parts = file.stem.split('-')
            if len(parts) >= 3:
                date_str = '-'.join(parts[:3])
                if date_str not in date_files:
                    date_files[date_str] = []
                date_files[date_str].append(file)
        except:
            pass
    
    # 2025-12-30と2025-12-31の記事を取得
    articles_1230 = sorted(date_files.get('2025-12-30', []))
    articles_1231 = sorted(date_files.get('2025-12-31', []))
    fixed_articles = articles_1230 + articles_1231
    
    # 300件になるように、他の日付から記事を追加
    if len(fixed_articles) < 300:
        needed = 300 - len(fixed_articles)
        print(f"📝 2025-12-30と2025-12-31に{needed}件追加して300件にします...")
        
        # 他の日付の記事を取得（2025-12-30, 2025-12-31, 2026-01-01以外）
        other_articles = []
        for date_str, files_list in date_files.items():
            if date_str not in ['2025-12-30', '2025-12-31', '2026-01-01']:
                other_articles.extend(files_list)
        
        # 古い順にソートして、必要な数だけ追加
        other_articles = sorted(other_articles)
        fixed_articles.extend(other_articles[:needed])
        print(f"✅ {needed}件追加しました。")
    
    # 300件を超える場合は、古い順に300件を保持
    if len(fixed_articles) > 300:
        fixed_articles = fixed_articles[:300]
        print(f"⚠️  2025-12-30と2025-12-31の記事が300件を超えています。最初の300件を保持します。")
    
    # 2026-01-01の既存記事を取得（5件まで）
    articles_0101_existing = sorted(date_files.get('2026-01-01', []))[:5]
    
    # 固定する記事（2025-12-30, 2025-12-31の300件 + 2026-01-01の既存5件）
    fixed_content_ids = set()
    for f in fixed_articles:
        parts = f.stem.split('-')
        if len(parts) >= 4:
            content_id = '-'.join(parts[3:])
            fixed_content_ids.add(content_id)
    
    for f in articles_0101_existing:
        parts = f.stem.split('-')
        if len(parts) >= 4:
            content_id = '-'.join(parts[3:])
            fixed_content_ids.add(content_id)
    
    print(f"固定記事数: {len(fixed_articles)}件（2025-12-30, 2025-12-31）")
    print(f"2026-01-01既存記事数: {len(articles_0101_existing)}件")
    
    # 2025-12-30と2025-12-31に300件を割り当て（150件ずつ）
    print(f"\n📅 2025-12-30と2025-12-31に300件を割り当て中...")
    articles_1230_target = fixed_articles[:150]
    articles_1231_target = fixed_articles[150:300]
    
    for idx, article_path in enumerate(fixed_articles):
        try:
            with open(article_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 150件ずつに分ける
            if idx < 150:
                target_date_str = "2025-12-30"
            else:
                target_date_str = "2025-12-31"
            
            # 日付を置換（frontmatter内のdate）
            pattern = r'^date:\s*"[^"]*"'
            replacement = f'date: "{target_date_str}"'
            new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
            
            # ファイル名を更新
            old_filename = article_path.name
            parts = old_filename.split('-')
            if len(parts) >= 4:
                new_filename = f"{target_date_str}-{'-'.join(parts[3:])}"
            else:
                continue
            
            new_filepath = article_path.parent / new_filename
            
            if article_path != new_filepath:
                if new_filepath.exists():
                    # 既に存在する場合はスキップ（同じcontent_idの記事）
                    continue
                
                with open(new_filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                article_path.unlink()
            else:
                with open(article_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                    
        except Exception as e:
            print(f"❌ エラー ({article_path.name}): {e}")
            continue
    
    print(f"✅ 2025-12-30: 150件、2025-12-31: 150件に割り当て完了")
    
    # 再割り当て対象の記事を取得（固定記事以外）
    reassign_articles = []
    for file in all_articles:
        parts = file.stem.split('-')
        if len(parts) >= 4:
            content_id = '-'.join(parts[3:])
            if content_id not in fixed_content_ids:
                reassign_articles.append(file)
    
    print(f"再割り当て対象: {len(reassign_articles)}件")
    
    # 2026-01-01に追加15件を割り当て
    articles_0101_additional = reassign_articles[:15]
    reassign_articles = reassign_articles[15:]
    
    # 2026-01-02から1日20件ずつ割り当て
    start_date = datetime(2026, 1, 2)
    current_date = start_date
    articles_per_day = 20
    
    updated_count = 0
    
    # 2026-01-01に追加15件を割り当て
    print(f"\n📅 2026-01-01に追加15件を割り当て中...")
    for article_path in articles_0101_additional:
        try:
            with open(article_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            target_date_str = "2026-01-01"
            
            # 日付を置換（frontmatter内のdate）
            pattern = r'^date:\s*"[^"]*"'
            replacement = f'date: "{target_date_str}"'
            new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
            
            # ファイル名を更新
            old_filename = article_path.name
            parts = old_filename.split('-')
            if len(parts) >= 4:
                new_filename = f"{target_date_str}-{'-'.join(parts[3:])}"
            else:
                continue
            
            new_filepath = article_path.parent / new_filename
            
            if article_path != new_filepath:
                if new_filepath.exists():
                    print(f"⚠️  スキップ: {old_filename} -> {new_filename} (既に存在)")
                    continue
                
                with open(new_filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                article_path.unlink()
                updated_count += 1
            else:
                with open(article_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated_count += 1
                
        except Exception as e:
            print(f"❌ エラー ({article_path.name}): {e}")
            continue
    
    # 2026-01-02から1日20件ずつ割り当て
    print(f"\n📅 2026-01-02から1日20件ずつ割り当て中...")
    for idx, article_path in enumerate(reassign_articles):
        try:
            with open(article_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 20件ごとに日付を進める
            if idx > 0 and idx % articles_per_day == 0:
                current_date += timedelta(days=1)
            
            current_date_str = current_date.strftime("%Y-%m-%d")
            
            # 日付を置換（frontmatter内のdate）
            pattern = r'^date:\s*"[^"]*"'
            replacement = f'date: "{current_date_str}"'
            new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
            
            # ファイル名を更新
            old_filename = article_path.name
            parts = old_filename.split('-')
            if len(parts) >= 4:
                new_filename = f"{current_date_str}-{'-'.join(parts[3:])}"
            else:
                continue
            
            new_filepath = article_path.parent / new_filename
            
            if article_path != new_filepath:
                if new_filepath.exists():
                    print(f"⚠️  スキップ: {old_filename} -> {new_filename} (既に存在)")
                    continue
                
                with open(new_filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                article_path.unlink()
                updated_count += 1
            else:
                with open(article_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated_count += 1
            
            if (updated_count % 20 == 0) or (idx == len(reassign_articles) - 1):
                print(f"✅ {updated_count}件更新完了 (現在の日付: {current_date_str})")
                
        except Exception as e:
            print(f"❌ エラー ({article_path.name}): {e}")
            continue
    
    print("\n" + "=" * 80)
    print("🎉 日付再割り当て完了！")
    print("=" * 80)
    print(f"✅ 更新: {updated_count}件")
    print(f"📁 保存先: {content_dir}")
    print(f"📅 2025-12-30, 2025-12-31: 300件（固定）")
    print(f"📅 2026-01-01: 20件（既存5件 + 追加15件）")
    print(f"📅 2026-01-02以降: 1日20件ずつ")
    print(f"📅 最終日: {current_date.strftime('%Y-%m-%d')}")
    print("=" * 80)
    print()


if __name__ == "__main__":
    import sys
    
    content_dir = "content"
    if len(sys.argv) > 1:
        content_dir = sys.argv[1]
    
    reassign_dates_custom(content_dir)

