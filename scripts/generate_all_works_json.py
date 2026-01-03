#!/usr/bin/env python3
"""
content/ディレクトリ内のすべてのMarkdownファイルを解析して、
data/all_works.jsonにまとめるスクリプト
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Optional

def parse_frontmatter(content: str) -> Dict[str, any]:
    """フロントマターをパース"""
    frontmatter = {}
    
    # フロントマターの開始と終了を検出
    if not content.startswith("---"):
        return frontmatter
    
    # 最初の`---`から次の`---`までを抽出
    end_index = content.find("---", 3)
    if end_index == -1:
        return frontmatter
    
    frontmatter_text = content[3:end_index].strip()
    
    # 各フィールドを抽出
    patterns = {
        'title': r'title:\s*"([^"]+)"',
        'date': r'date:\s*"([^"]+)"',
        'image': r'image:\s*"([^"]+)"',
        'affiliateLink': r'affiliateLink:\s*"([^"]+)"',
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, frontmatter_text)
        if match:
            frontmatter[key] = match.group(1)
    
    return frontmatter

def extract_video_url(content: str) -> Optional[str]:
    """本文からvideoUrl（iframeのsrc）を抽出"""
    # iframeのsrc属性を抽出
    pattern = r'<iframe[^>]*src="([^"]+)"[^>]*>'
    match = re.search(pattern, content)
    if match:
        return match.group(1)
    return None

def extract_actress(content: str) -> Optional[str]:
    """本文からactress（出演情報）を抽出"""
    # 「**出演:**」または「**主要キャラクター:**」の行を抽出
    patterns = [
        r'\*\*出演:\*\*\s*(.+?)(?:\n|$)',
        r'\*\*主要キャラクター:\*\*\s*(.+?)(?:\n|$)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            actress = match.group(1).strip()
            # 「不明」の場合はNoneを返す
            if actress and actress != "不明":
                return actress
    
    return None

def parse_markdown_file(file_path: Path) -> Optional[Dict[str, any]]:
    """Markdownファイルを解析して必要な情報を抽出"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # フロントマターをパース
        frontmatter = parse_frontmatter(content)
        
        # 必要な項目が揃っているか確認
        if not all(key in frontmatter for key in ['title', 'date', 'image', 'affiliateLink']):
            print(f"⚠️  警告: {file_path.name} に必要なフロントマターが不足しています")
            return None
        
        # 本文からvideoUrlとactressを抽出
        video_url = extract_video_url(content)
        actress = extract_actress(content)
        
        # データを構築
        work_data = {
            'title': frontmatter['title'],
            'image': frontmatter['image'],
            'videoUrl': video_url,
            'actress': actress,
            'date': frontmatter['date'],
            'affiliateLink': frontmatter['affiliateLink'],
        }
        
        return work_data
    
    except Exception as e:
        print(f"❌ エラー: {file_path.name} の解析に失敗しました: {e}")
        return None

def main():
    """メイン処理"""
    # パスを設定
    content_dir = Path(__file__).parent.parent / 'content'
    output_file = Path(__file__).parent.parent / 'data' / 'all_works.json'
    
    # contentディレクトリが存在するか確認
    if not content_dir.exists():
        print(f"❌ エラー: {content_dir} が存在しません")
        return
    
    # dataディレクトリを作成
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # すべてのMarkdownファイルを取得
    md_files = list(content_dir.glob('*.md'))
    print(f"📁 {len(md_files)}個のMarkdownファイルを発見しました")
    
    # 各ファイルを解析
    all_works = []
    success_count = 0
    error_count = 0
    
    for md_file in md_files:
        work_data = parse_markdown_file(md_file)
        if work_data:
            all_works.append(work_data)
            success_count += 1
        else:
            error_count += 1
    
    # 日付順にソート（新しい順）
    all_works.sort(key=lambda x: x['date'], reverse=True)
    
    # JSONファイルに保存
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_works, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 完了!")
    print(f"   - 成功: {success_count}件")
    print(f"   - エラー: {error_count}件")
    print(f"   - 出力先: {output_file}")
    print(f"   - 総件数: {len(all_works)}件")

if __name__ == '__main__':
    main()

