#!/usr/bin/env python3
"""
既存のMarkdown記事のアフィリエイトリンクをHTMLの<a>タグに変換するスクリプト
"""

import os
import re
import sys
from pathlib import Path


def fix_affiliate_links_in_file(file_path: str) -> bool:
    """
    ファイル内のアフィリエイトリンクを修正
    
    Args:
        file_path: Markdownファイルのパス
        
    Returns:
        修正があった場合はTrue
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        original_content = content
        
        # Markdownリンク構文をHTMLの<a>タグに変換
        # <div className="affiliate-link">[text](url)</div> のパターン
        pattern1 = r'<div className="affiliate-link">\s*\[([^\]]+)\]\(([^)]+)\)\s*</div>'
        replacement1 = r'<div className="affiliate-link">\n  <a href="\2" target="_blank" rel="noopener noreferrer">\1</a>\n</div>'
        content = re.sub(pattern1, replacement1, content)
        
        # <div className="affiliate-link-inline">[text](url)</div> のパターン
        pattern2 = r'<div className="affiliate-link-inline">\s*\[([^\]]+)\]\(([^)]+)\)\s*</div>'
        replacement2 = r'<div className="affiliate-link-inline">\n  <a href="\2" target="_blank" rel="noopener noreferrer">\1</a>\n</div>'
        content = re.sub(pattern2, replacement2, content)
        
        # 変更があった場合のみファイルを保存
        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"エラー: {file_path} の処理に失敗しました: {e}", file=sys.stderr)
        return False


def main():
    """メイン処理"""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    content_dir = project_root / "content"
    
    if not content_dir.exists():
        print("エラー: contentディレクトリが見つかりません", file=sys.stderr)
        sys.exit(1)
    
    print("🔧 アフィリエイトリンクを修正中...\n")
    
    fixed_count = 0
    for md_file in content_dir.glob("*.md"):
        if fix_affiliate_links_in_file(str(md_file)):
            print(f"✅ 修正: {md_file.name}")
            fixed_count += 1
        else:
            print(f"⏭️  変更なし: {md_file.name}")
    
    print(f"\n🎉 完了！ {fixed_count}件のファイルを修正しました")


if __name__ == "__main__":
    main()

