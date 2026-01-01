#!/usr/bin/env python3
"""
既存記事のURLにアクセスして、「中出し」作品かどうかを調べるスクリプト
"""

import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import urllib.request
import urllib.error
from bs4 import BeautifulSoup

def extract_content_id_from_url(url: str) -> str:
    """アフィリエイトURLからcontent_idを抽出"""
    try:
        # URLをパース
        parsed = urlparse(url)
        
        # lurlパラメータからcontent_idを抽出
        if 'lurl' in parse_qs(parsed.query):
            lurl = parse_qs(parsed.query)['lurl'][0]
            # URLデコード
            from urllib.parse import unquote
            decoded_lurl = unquote(lurl)
            # content_idを抽出（id=の後）
            match = re.search(r'id=([^&/]+)', decoded_lurl)
            if match:
                return match.group(1)
        
        # 直接URLから抽出
        match = re.search(r'id=([^&/]+)', url)
        if match:
            return match.group(1)
            
    except Exception as e:
        print(f"⚠️  URL解析エラー: {e}", file=sys.stderr)
    
    return None


def get_dmm_page_content(content_id: str) -> str:
    """DMMの作品ページのHTMLを取得"""
    # DMMの作品ページURL（videoaとvideoの両方を試す）
    urls = [
        f"https://www.dmm.co.jp/digital/videoa/-/detail/=/cid={content_id}/",
        f"https://www.dmm.co.jp/digital/video/-/detail/=/cid={content_id}/",
    ]
    
    # SSL証明書検証をスキップ（開発環境のみ）
    import ssl
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    # User-Agentを設定（DMMがブロックする可能性があるため）
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # 複数のURLを試す
    for url in urls:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10, context=ssl_context) as response:
                html = response.read().decode('utf-8')
                # HTMLが有効かチェック（空でない、エラーページでない）
                if html and len(html) > 1000 and '404' not in html.lower()[:500]:
                    return html
        except urllib.error.HTTPError as e:
            # 404の場合は次のURLを試す
            if e.code == 404:
                continue
            print(f"⚠️  HTTPエラー ({content_id}, {url}): {e.code} - {e.reason}", file=sys.stderr)
        except Exception as e:
            # エラーが発生した場合は次のURLを試す
            continue
    
    # すべてのURLで失敗
    print(f"⚠️  取得エラー ({content_id}): すべてのURLで取得に失敗", file=sys.stderr)
    return None


def check_nakadashi(html: str) -> bool:
    """HTMLから「中出し」が含まれているかチェック（詳細版）"""
    if not html:
        return False
    
    # BeautifulSoupでパース
    soup = BeautifulSoup(html, 'html.parser')
    
    # 「中出し」というキーワードを検索
    nakadashi_keywords = ['中出し', '中出', '中だし', '中だ出し']
    
    # 1. ジャンルタグを詳細に確認
    # DMMのジャンルタグは通常、特定のクラスやIDを持つ
    genre_selectors = [
        'table.mg-bg',
        'table[summary="ジャンル"]',
        'div[class*="genre"]',
        'div[class*="tag"]',
        'span[class*="genre"]',
        'a[class*="genre"]',
        'td[class*="genre"]',
        'ul[class*="genre"]',
        'li[class*="genre"]',
    ]
    
    for selector in genre_selectors:
        elements = soup.select(selector)
        for elem in elements:
            elem_text = elem.get_text()
            for keyword in nakadashi_keywords:
                if keyword in elem_text:
                    return True
    
    # 2. 作品説明文を確認
    description_selectors = [
        'div[class*="description"]',
        'div[class*="comment"]',
        'div[class*="review"]',
        'p[class*="description"]',
        'td[class*="description"]',
        'div#mu',
        'div[class*="mu"]',
    ]
    
    for selector in description_selectors:
        elements = soup.select(selector)
        for elem in elements:
            elem_text = elem.get_text()
            for keyword in nakadashi_keywords:
                if keyword in elem_text:
                    return True
    
    # 3. タイトルや見出しを確認
    title_selectors = ['h1', 'h2', 'h3', 'title']
    for selector in title_selectors:
        elements = soup.select(selector)
        for elem in elements:
            elem_text = elem.get_text()
            for keyword in nakadashi_keywords:
                if keyword in elem_text:
                    return True
    
    # 4. すべてのリンクテキストを確認
    links = soup.find_all('a')
    for link in links:
        link_text = link.get_text()
        for keyword in nakadashi_keywords:
            if keyword in link_text:
                return True
    
    # 5. ページ全体のテキストを確認（最後の手段）
    text = soup.get_text()
    for keyword in nakadashi_keywords:
        if keyword in text:
            return True
    
    return False


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
                frontmatter[key] = value
        
        return frontmatter
        
    except Exception as e:
        print(f"⚠️  ファイル読み込みエラー ({file_path}): {e}", file=sys.stderr)
        return {}


def add_nakadashi_tag_to_article(file_path: Path) -> bool:
    """記事ファイルに「中出し」タグを追加し、記事本文にも情報を追加"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # frontmatterを抽出
        match = re.match(r'^(---\n.*?\n---)', content, re.DOTALL)
        if not match:
            return False
        
        frontmatter_text = match.group(1)
        rest_content = content[len(frontmatter_text):]
        
        # 既に「中出し」タグがあるかチェック
        tag_already_exists = '"中出し"' in frontmatter_text or "'中出し'" in frontmatter_text
        
        # tags行を探す
        tags_pattern = r'tags:\s*\[(.*?)\]'
        tags_match = re.search(tags_pattern, frontmatter_text)
        
        new_frontmatter = frontmatter_text
        if not tag_already_exists:
            if tags_match:
                # 既存のtagsに「中出し」を追加
                existing_tags = tags_match.group(1)
                # 既存のタグの後に「中出し」を追加
                new_tags = existing_tags.rstrip() + ', "中出し"'
                new_frontmatter = re.sub(tags_pattern, f'tags: [{new_tags}]', frontmatter_text)
            else:
                # tags行がない場合は追加
                new_frontmatter = frontmatter_text.rstrip() + '\ntags: ["中出し"]\n---'
        
        # 記事本文に「中出し」の情報を追加（既に含まれていない場合）
        new_rest_content = rest_content
        if '中出し' not in rest_content and '[K1]' not in rest_content:
            # 「ここがエロかったｗ」セクションの後に追加
            ero_section_pattern = r'(## ここがエロかったｗ.*?\n)'
            ero_match = re.search(ero_section_pattern, rest_content, re.DOTALL)
            
            if ero_match:
                # 「ここがエロかったｗ」セクションの後に追加
                insert_pos = ero_match.end()
                nakadashi_note = '\n**🎯 中出し作品**\n\nこの作品は[K1]シーンが含まれています。\n\n'
                new_rest_content = rest_content[:insert_pos] + nakadashi_note + rest_content[insert_pos:]
            else:
                # 「ここがエロかったｗ」セクションがない場合は、最初の見出しの後に追加
                first_heading_pattern = r'(## .*?\n)'
                first_heading_match = re.search(first_heading_pattern, rest_content)
                if first_heading_match:
                    insert_pos = first_heading_match.end()
                    nakadashi_note = '\n**🎯 中出し作品**\n\nこの作品は[K1]シーンが含まれています。\n\n'
                    new_rest_content = rest_content[:insert_pos] + nakadashi_note + rest_content[insert_pos:]
        
        # ファイルを書き込み
        new_content = new_frontmatter + new_rest_content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
        
    except Exception as e:
        print(f"⚠️  タグ追加エラー ({file_path}): {e}", file=sys.stderr)
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
    
    nakadashi_count = 0
    checked_count = 0
    error_count = 0
    updated_count = 0
    
    results = []
    
    for idx, md_file in enumerate(md_files, 1):
        print(f"\n[{idx}/{len(md_files)}] {md_file.name} をチェック中...")
        
        # frontmatterを解析
        frontmatter = parse_markdown_file(md_file)
        
        # content_idを取得
        content_id = frontmatter.get('contentId', '')
        affiliate_link = frontmatter.get('affiliateLink', '')
        
        if not content_id and affiliate_link:
            content_id = extract_content_id_from_url(affiliate_link)
        
        if not content_id:
            print(f"   ⚠️  content_idが見つかりません")
            error_count += 1
            continue
        
        # DMMページを取得
        html = get_dmm_page_content(content_id)
        
        if not html:
            print(f"   ⚠️  ページ取得に失敗しました")
            error_count += 1
            continue
        
        # 「中出し」をチェック
        is_nakadashi = check_nakadashi(html)
        
        checked_count += 1
        
        if is_nakadashi:
            nakadashi_count += 1
            print(f"   ✅ 中出し作品です")
            
            # タグを追加
            if add_nakadashi_tag_to_article(md_file):
                print(f"   📝 「中出し」タグを追加しました")
                updated_count += 1
            else:
                print(f"   ℹ️  既に「中出し」タグが追加済みです")
            
            results.append({
                'file': md_file.name,
                'content_id': content_id,
                'title': frontmatter.get('title', ''),
                'is_nakadashi': True
            })
        else:
            print(f"   ❌ 中出し作品ではありません")
        
        # API負荷軽減のため、少し待機
        time.sleep(1)
    
    # 結果を表示
    print("\n" + "=" * 80)
    print("📊 チェック結果")
    print("=" * 80)
    print(f"✅ チェック完了: {checked_count}件")
    print(f"🎯 中出し作品: {nakadashi_count}件")
    print(f"📝 タグ追加: {updated_count}件")
    print(f"❌ エラー: {error_count}件")
    
    if results:
        print("\n📝 中出し作品一覧:")
        for result in results:
            print(f"   - {result['content_id']}: {result['title'][:50]}...")
    
    # 結果をJSONファイルに保存
    import json
    output_file = project_root / "data" / "nakadashi_check_results.json"
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'total_checked': checked_count,
            'nakadashi_count': nakadashi_count,
            'error_count': error_count,
            'results': results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 結果を保存しました: {output_file}")


if __name__ == "__main__":
    main()

