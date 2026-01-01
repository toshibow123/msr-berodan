#!/usr/bin/env python3
"""
既存記事のタグを、DMM APIから取得したジャンル情報で更新するスクリプト
"""

import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse, parse_qs, unquote
import urllib.request
import urllib.error
import ssl

# .envファイルの読み込み
try:
    from dotenv import load_dotenv
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ .envファイルを読み込みました: {env_path}")
except ImportError:
    print("⚠️  python-dotenvがインストールされていません。pip install python-dotenv を実行してください")
except Exception as e:
    print(f"⚠️  .envファイルの読み込みエラー: {e}")

import os

def fetch_dmm_product_info(api_id: str, affiliate_id: str, content_id: str) -> dict | None:
    """DMM APIから作品情報を取得"""
    base_url = "https://api.dmm.com/affiliate/v3/ItemList"
    
    params = {
        "api_id": api_id,
        "affiliate_id": affiliate_id,
        "site": "FANZA",
        "service": "digital",
        "floor": "video",
        "cid": content_id,
        "output": "json"
    }
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    try:
        # SSL証明書検証をスキップ（開発環境のみ）
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10, context=ssl_context) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if "result" in data and "items" in data["result"] and len(data["result"]["items"]) > 0:
                item = data["result"]["items"][0]
                
                return {
                    "content_id": item.get("content_id", ""),
                    "title": item.get("title", ""),
                    "genre": [genre.get("name", "") for genre in item.get("iteminfo", {}).get("genre", [])],
                    "actress": [actress.get("name", "") for actress in item.get("iteminfo", {}).get("actress", [])],
                    "maker": item.get("iteminfo", {}).get("maker", [{}])[0].get("name", "") if item.get("iteminfo", {}).get("maker") else "",
                    "director": item.get("iteminfo", {}).get("director", [{}])[0].get("name", "") if item.get("iteminfo", {}).get("director") else "",
                }
            
    except Exception as e:
        print(f"⚠️  API取得エラー ({content_id}): {e}", file=sys.stderr)
        return None
    
    return None


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
                    # 配列から値を抽出
                    array_content = value[1:-1]
                    array_values = []
                    for item in array_content.split(','):
                        item = item.strip().strip('"').strip("'")
                        if item:
                            array_values.append(item)
                    frontmatter[key] = array_values
                else:
                    frontmatter[key] = value
        
        return frontmatter
        
    except Exception as e:
        print(f"⚠️  ファイル読み込みエラー ({file_path}): {e}", file=sys.stderr)
        return {}


def update_article_tags(file_path: Path, api_genres: list, api_actress: list, api_maker: str) -> bool:
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
        existing_frontmatter = parse_markdown_file(file_path)
        existing_tags = existing_frontmatter.get('tags', [])
        
        # 新しいタグリストを作成
        new_tags = []
        
        # 1. 既存のタグを保持（マッチしたジャンル、年、女優、メーカーなど）
        matched_genres = existing_frontmatter.get('genre', [])
        if matched_genres:
            new_tags.extend([f'"{g}"' for g in matched_genres])
        
        # 年を抽出
        year = None
        for tag in existing_tags:
            if isinstance(tag, str) and tag.endswith('年'):
                year = tag
                break
        
        if year:
            new_tags.append(f'"{year}"')
        
        # 2. DMM APIから取得したすべてのジャンルを追加
        important_genres = ['中出し', '中出', 'ベロチュー', 'ガチイキ', '3P', '4P', '不倫', 'NTR', 'ネトラレ', '寝取られ']
        
        # 重要なジャンルを優先的に追加
        for genre in api_genres:
            genre_quoted = f'"{genre}"'
            if any(important in genre for important in important_genres):
                if genre_quoted not in new_tags:
                    new_tags.append(genre_quoted)
        
        # その他のジャンルを追加
        for genre in api_genres:
            genre_quoted = f'"{genre}"'
            if genre_quoted not in new_tags:
                new_tags.append(genre_quoted)
        
        # 3. 女優タグ（最大2人まで、既存のものを優先）
        existing_actress_tags = [t for t in existing_tags if isinstance(t, str) and t in api_actress]
        if existing_actress_tags:
            new_tags.extend([f'"{a}"' for a in existing_actress_tags[:2]])
        elif api_actress:
            new_tags.extend([f'"{a}"' for a in api_actress[:2]])
        
        # 4. メーカータグ
        if api_maker:
            maker_quoted = f'"{api_maker}"'
            if maker_quoted not in new_tags:
                new_tags.append(maker_quoted)
        
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


def extract_content_id_from_url(url: str) -> str:
    """アフィリエイトURLからcontent_idを抽出"""
    try:
        parsed = urlparse(url)
        if 'lurl' in parse_qs(parsed.query):
            lurl = parse_qs(parsed.query)['lurl'][0]
            decoded_lurl = unquote(lurl)
            match = re.search(r'id=([^&/]+)', decoded_lurl)
            if match:
                return match.group(1)
        match = re.search(r'id=([^&/]+)', url)
        if match:
            return match.group(1)
    except Exception as e:
        print(f"⚠️  URL解析エラー: {e}", file=sys.stderr)
    return None


def main():
    """メイン処理"""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    content_dir = project_root / "content"
    
    if not content_dir.exists():
        print(f"❌ contentディレクトリが見つかりません: {content_dir}")
        sys.exit(1)
    
    # DMM API認証情報
    api_id = os.getenv("DMM_API_ID")
    affiliate_id = os.getenv("DMM_AFFILIATE_ID")
    
    if not api_id or not affiliate_id:
        print("❌ DMM_API_IDまたはDMM_AFFILIATE_IDが設定されていません")
        sys.exit(1)
    
    # すべてのMarkdownファイルを取得
    md_files = sorted(content_dir.glob("*.md"))
    
    print(f"📁 記事ファイル数: {len(md_files)}件")
    print("=" * 80)
    
    updated_count = 0
    error_count = 0
    skipped_count = 0
    
    for idx, md_file in enumerate(md_files, 1):
        print(f"\n[{idx}/{len(md_files)}] {md_file.name} を処理中...")
        
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
        
        # DMM APIから作品情報を取得
        product_info = fetch_dmm_product_info(api_id, affiliate_id, content_id)
        
        if not product_info:
            print(f"   ⚠️  作品情報の取得に失敗しました")
            error_count += 1
            continue
        
        api_genres = product_info.get('genre', [])
        
        if not api_genres:
            print(f"   ⚠️  ジャンル情報がありません")
            skipped_count += 1
            continue
        
        # タグを更新
        if update_article_tags(md_file, api_genres, product_info.get('actress', []), product_info.get('maker', '')):
            print(f"   ✅ タグを更新しました（ジャンル: {len(api_genres)}件）")
            updated_count += 1
        else:
            print(f"   ⚠️  タグの更新に失敗しました")
            error_count += 1
        
        # API負荷軽減のため、少し待機
        time.sleep(1)
    
    # 結果を表示
    print("\n" + "=" * 80)
    print("📊 更新結果")
    print("=" * 80)
    print(f"✅ 更新完了: {updated_count}件")
    print(f"⚠️  スキップ: {skipped_count}件")
    print(f"❌ エラー: {error_count}件")
    print("=" * 80)


if __name__ == "__main__":
    main()

