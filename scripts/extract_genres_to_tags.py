#!/usr/bin/env python3
"""
既存記事の「**ジャンル:**」セクションからジャンル情報を抽出して、
frontmatterのtagsに追加するスクリプト
"""

import re
import sys
from pathlib import Path
from collections import Counter

def parse_markdown_file(file_path: Path) -> dict:
    """Markdownファイルからfrontmatterを解析"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # frontmatterを抽出
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            return {}
        
        frontmatter_text = match.group(1)
        frontmatter = {}
        
        # 各行をパース
        for line in frontmatter_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                
                # 配列の処理
                if value.startswith('[') and value.endswith(']'):
                    array_content = value[1:-1]
                    array_values = []
                    for item in array_content.split(','):
                        item = item.strip().strip('"').strip("'")
                        if item:
                            array_values.append(item)
                    frontmatter[key] = array_values
                else:
                    frontmatter[key] = value
        
        return frontmatter, content
        
    except Exception as e:
        print(f"⚠️  ファイル読み込みエラー ({file_path}): {e}", file=sys.stderr)
        return {}, ""


def extract_genres_from_content(content: str) -> list:
    """記事本文から「**ジャンル:**」の行を抽出してジャンルリストを返す"""
    # 「**ジャンル:**」の行を探す
    pattern = r'\*\*ジャンル:\*\*\s*(.+?)(?:\n|$)'
    match = re.search(pattern, content)
    
    if not match:
        return []
    
    genres_text = match.group(1).strip()
    
    # カンマ区切りでジャンルを分割
    genres = [g.strip() for g in genres_text.split('、') if g.strip()]
    
    return genres


def update_article_tags(file_path: Path, genres_from_content: list) -> bool:
    """記事ファイルのタグを更新"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # frontmatterを抽出
        match = re.match(r'^(---\n.*?\n---)', content, re.DOTALL)
        if not match:
            return False
        
        frontmatter_text = match.group(1)
        rest_content = content[len(frontmatter_text):]
        
        # 既存のfrontmatterを解析
        existing_frontmatter, _ = parse_markdown_file(file_path)
        existing_tags = existing_frontmatter.get('tags', [])
        
        # 既存のタグを文字列のセットに変換（重複チェック用）
        existing_tags_set = {str(tag).strip().strip('"').strip("'") for tag in existing_tags}
        
        # 新しいタグリストを作成
        new_tags = []
        
        # 1. 既存のタグを保持
        for tag in existing_tags:
            tag_str = str(tag).strip().strip('"').strip("'")
            if tag_str:
                new_tags.append(f'"{tag_str}"')
        
        # 2. 本文から抽出したジャンルを追加（重複を避ける）
        for genre in genres_from_content:
            if genre and genre not in existing_tags_set:
                new_tags.append(f'"{genre}"')
                existing_tags_set.add(genre)
        
        # タグ数を15個までに制限
        new_tags = new_tags[:15]
        tags_str = ", ".join(new_tags)
        
        # frontmatterを更新
        tags_pattern = r'tags:\s*\[.*?\]'
        if re.search(tags_pattern, frontmatter_text):
            new_frontmatter = re.sub(tags_pattern, f'tags: [{tags_str}]', frontmatter_text)
        else:
            # tags行がない場合は追加
            new_frontmatter = frontmatter_text.rstrip() + f'\ntags: [{tags_str}]\n---'
        
        # ファイルを書き込み
        new_content = new_frontmatter + rest_content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
        
    except Exception as e:
        print(f"⚠️  タグ更新エラー ({file_path}): {e}", file=sys.stderr)
        return False


def main():
    """メイン処理"""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    content_dir = project_root / "content"
    
    if not content_dir.exists():
        print(f"❌ contentディレクトリが見つかりません: {content_dir}")
        sys.exit(1)
    
    # すべてのMarkdownファイルを取得
    md_files = sorted(content_dir.glob("*.md"))
    
    print(f"📁 記事ファイル数: {len(md_files)}件")
    print("=" * 80)
    
    updated_count = 0
    skipped_count = 0
    error_count = 0
    all_genres = Counter()
    
    for idx, md_file in enumerate(md_files, 1):
        print(f"\n[{idx}/{len(md_files)}] {md_file.name} を処理中...")
        
        try:
            # ファイルを読み込み
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 「**ジャンル:**」からジャンルを抽出
            genres = extract_genres_from_content(content)
            
            if not genres:
                print(f"   ⚠️  「**ジャンル:**」が見つかりません")
                skipped_count += 1
                continue
            
            # ジャンルをカウント
            for genre in genres:
                all_genres[genre] += 1
            
            # タグを更新
            if update_article_tags(md_file, genres):
                print(f"   ✅ タグを更新しました（ジャンル: {len(genres)}件）")
                print(f"      {', '.join(genres[:5])}{'...' if len(genres) > 5 else ''}")
                updated_count += 1
            else:
                print(f"   ⚠️  タグの更新に失敗しました")
                error_count += 1
                
        except Exception as e:
            print(f"   ❌ エラー: {e}", file=sys.stderr)
            error_count += 1
    
    # 結果を表示
    print("\n" + "=" * 80)
    print("📊 更新結果")
    print("=" * 80)
    print(f"✅ 更新完了: {updated_count}件")
    print(f"⚠️  スキップ: {skipped_count}件")
    print(f"❌ エラー: {error_count}件")
    
    # ジャンル統計を表示
    print("\n📈 ジャンル統計（上位20件）:")
    for genre, count in all_genres.most_common(20):
        print(f"   {genre}: {count}件")
    
    print("=" * 80)


if __name__ == "__main__":
    main()

