#!/usr/bin/env python3
"""
batch*_static_params.tsファイル内の\nを実際の改行に置き換える
"""

import re
from pathlib import Path

def fix_batch_file(filepath: Path):
    """batchファイルを修正"""
    print(f"📝 {filepath.name} を修正中...")
    
    content = filepath.read_text(encoding="utf-8")
    
    # 5行目にconst slugs = [が含まれているか確認
    if 'const slugs = [' not in content:
        print(f"⚠️  {filepath.name} に 'const slugs = [' が見つかりませんでした")
        return False
    
    # const slugs = [ から ] までの部分を抽出
    match = re.search(r'const slugs = \[(.*?)\]', content, re.DOTALL)
    if not match:
        print(f"⚠️  {filepath.name} でパターンが見つかりませんでした")
        return False
    
    slugs_content = match.group(1)
    
    # \nを実際の改行に置き換え
    slugs_content = slugs_content.replace('\\n', '\n')
    
    # 正規表現で各 "..." を抽出
    slugs = re.findall(r'"([^"]+)"', slugs_content)
    
    if not slugs:
        print(f"⚠️  {filepath.name} でslugが見つかりませんでした")
        return False
    
    # 新しい配列を作成（各slugを個別の行に）
    new_slugs_array = '    ' + ',\n    '.join([f'"{slug}"' for slug in slugs]) + '\n'
    
    # 元の部分を置き換え
    new_content = re.sub(
        r'const slugs = \[.*?\]',
        f'const slugs = [\n{new_slugs_array}  ]',
        content,
        flags=re.DOTALL
    )
    
    # ファイルに書き込み
    filepath.write_text(new_content, encoding="utf-8")
    print(f"✅ {filepath.name} を修正しました ({len(slugs)}個のslug)")
    return True

def main():
    scripts_dir = Path(__file__).parent
    batch_files = list(scripts_dir.glob("batch*_static_params.ts"))
    
    if not batch_files:
        print("❌ batch*_static_params.ts ファイルが見つかりませんでした")
        return
    
    print("=" * 80)
    print("  batch*_static_params.ts ファイルの修正")
    print("=" * 80 + "\n")
    
    fixed_count = 0
    for batch_file in batch_files:
        if fix_batch_file(batch_file):
            fixed_count += 1
    
    print("\n" + "=" * 80)
    print(f"🎉 修正完了！")
    print(f"   修正: {fixed_count}件")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
