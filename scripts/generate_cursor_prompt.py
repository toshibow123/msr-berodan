#!/usr/bin/env python3
"""
DMM作品URLから情報をスクレイピングし、Cursor（AI）に記事を書かせるための
詳細な指示プロンプトを生成してクリップボードにコピーするスクリプト
"""

import re
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse, parse_qs, unquote
import pyperclip


def extract_content_id_from_url(url: str) -> str | None:
    """
    URLから品番（content_id）を抽出（アフィリエイトリンク対応版）
    
    Args:
        url: DMM作品URL
        
    Returns:
        content_id または None
    """
    # アフィリエイトリンクの場合、実URLを取り出す
    if "al.fanza.co.jp" in url or "al.dmm.co.jp" in url:
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        if 'lurl' in qs:
            url = unquote(qs['lurl'][0])
            print(f"🔍 アフィリエイトリンクを検出: 実URLに変換しました")
    
    # 正規表現で品番を抽出（複数パターン対応）
    patterns = [
        r'cid=([a-z0-9_]+)',        # 通常のDMM: /cid=abc123/
        r'id=([a-z0-9_]+)',          # 動画配信: /id=abc123/
        r'/detail/=/cid=([a-z0-9_]+)', # パス埋め込み形式
        r'content_id=([a-z0-9_]+)',  # クエリパラメータ形式
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return None


def scrape_dmm_product_info(url: str) -> dict | None:
    """
    DMM作品ページから情報をスクレイピング
    
    Args:
        url: DMM作品URL
        
    Returns:
        作品情報の辞書、または None
    """
    try:
        # age_check_done=1 cookieを設定
        cookies = {
            'age_check_done': '1'
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        print("📡 ページを取得中...")
        response = requests.get(url, cookies=cookies, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 作品名を取得
        title = ""
        title_elem = soup.select_one('h1#title, h1.title, .itemBox h1, .itemBox .title')
        if title_elem:
            title = title_elem.get_text(strip=True)
        else:
            # タイトルが見つからない場合、metaタグから取得
            meta_title = soup.select_one('meta[property="og:title"]')
            if meta_title:
                title = meta_title.get('content', '').strip()
        
        if not title:
            print("⚠️  作品名が見つかりませんでした")
        
        # 作品ID (CID) を取得
        content_id = extract_content_id_from_url(url)
        if not content_id:
            # URLから取得できない場合、ページ内から探す
            cid_pattern = re.search(r'cid[=:](\w+)', response.text, re.IGNORECASE)
            if cid_pattern:
                content_id = cid_pattern.group(1)
        
        # 紹介文を取得
        description = ""
        # 複数のパターンで紹介文を探す
        desc_selectors = [
            '.itemBox .itemText',
            '.itemBox .description',
            '.itemBox .review',
            '#itemText',
            '.itemText',
            '.description',
            '.review'
        ]
        
        for selector in desc_selectors:
            desc_elem = soup.select_one(selector)
            if desc_elem:
                description = desc_elem.get_text(strip=True)
                if description:
                    break
        
        # まだ見つからない場合、meta descriptionから取得
        if not description:
            meta_desc = soup.select_one('meta[name="description"], meta[property="og:description"]')
            if meta_desc:
                description = meta_desc.get('content', '').strip()
        
        # 作品特徴（タグ情報）を取得
        keywords = []
        
        # 出演者を取得
        actresses = []
        actress_elems = soup.select('.actressName, .actress, .performer, [data-actress]')
        for elem in actress_elems:
            name = elem.get_text(strip=True)
            if name and name not in actresses:
                actresses.append(name)
        
        # ジャンルを取得
        genres = []
        genre_elems = soup.select('.genre, .category, [data-genre]')
        for elem in genre_elems:
            genre = elem.get_text(strip=True)
            if genre and genre not in genres:
                genres.append(genre)
        
        # メーカーを取得
        maker = ""
        maker_elem = soup.select_one('.maker, .brand, [data-maker]')
        if maker_elem:
            maker = maker_elem.get_text(strip=True)
        
        # シリーズを取得
        series = ""
        series_elem = soup.select_one('.series, [data-series]')
        if series_elem:
            series = series_elem.get_text(strip=True)
        
        # タグを取得
        tags = []
        tag_elems = soup.select('.tag, [data-tag]')
        for elem in tag_elems:
            tag = elem.get_text(strip=True)
            if tag and tag not in tags:
                tags.append(tag)
        
        # 作品特徴をカンマ区切りで結合
        if actresses:
            keywords.extend(actresses)
        if genres:
            keywords.extend(genres)
        if maker:
            keywords.append(f"メーカー: {maker}")
        if series:
            keywords.append(f"シリーズ: {series}")
        if tags:
            keywords.extend(tags)
        
        keywords_str = "、".join(keywords) if keywords else "不明"
        
        # メイン画像URL（パッケージ画像）を取得
        main_image_url = ""
        # 複数のパターンで画像を探す
        image_selectors = [
            '.itemBox img[src*="pics.dmm.co.jp"]',
            '.itemBox .package img',
            '.package img',
            'img[src*="pics.dmm.co.jp"]',
            'meta[property="og:image"]'
        ]
        
        for selector in image_selectors:
            if selector.startswith('meta'):
                img_elem = soup.select_one(selector)
                if img_elem:
                    main_image_url = img_elem.get('content', '')
            else:
                img_elem = soup.select_one(selector)
                if img_elem:
                    main_image_url = img_elem.get('src', '') or img_elem.get('data-src', '')
            
            if main_image_url:
                # 相対URLの場合は絶対URLに変換
                if main_image_url.startswith('//'):
                    main_image_url = 'https:' + main_image_url
                elif main_image_url.startswith('/'):
                    main_image_url = 'https://www.dmm.co.jp' + main_image_url
                break
        
        # サンプル画像URLリストを取得（拡大画像）
        sample_images = []
        
        # サンプル画像のセレクタを複数試す
        sample_selectors = [
            '.sampleImage img',
            '.sample img',
            '.gallery img',
            '[data-sample] img',
            'img[src*="sample"]',
            'img[src*="jp-"]'
        ]
        
        for selector in sample_selectors:
            img_elems = soup.select(selector)
            for img_elem in img_elems:
                img_url = img_elem.get('src', '') or img_elem.get('data-src', '') or img_elem.get('data-original', '')
                if img_url and 'pics.dmm.co.jp' in img_url:
                    # サムネイルではなく拡大画像を取得
                    # サムネイルURLを拡大画像URLに変換
                    if 'thumb' in img_url or 'small' in img_url:
                        img_url = img_url.replace('thumb', '').replace('small', '')
                    # 相対URLの場合は絶対URLに変換
                    if img_url.startswith('//'):
                        img_url = 'https:' + img_url
                    elif img_url.startswith('/'):
                        img_url = 'https://www.dmm.co.jp' + img_url
                    
                    if img_url not in sample_images:
                        sample_images.append(img_url)
        
        # content_idからサンプル画像URLを生成（ページから取得できない場合）
        if not sample_images and content_id:
            # DMMのサンプル画像URLパターン
            base_url = f"https://pics.dmm.co.jp/digital/videoa/{content_id}/{content_id}jp-"
            for i in range(1, 7):  # 1-6枚目
                sample_images.append(f"{base_url}{i}.jpg")
        
        return {
            "title": title,
            "content_id": content_id or "unknown",
            "description": description,
            "keywords": keywords_str,
            "main_image_url": main_image_url,
            "sample_images": sample_images,
            "url": url
        }
        
    except requests.RequestException as e:
        print(f"❌ ページ取得エラー: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"❌ スクレイピングエラー: {e}", file=sys.stderr)
        return None


def generate_cursor_prompt(product_info: dict) -> str:
    """
    Cursor用のプロンプトを生成
    
    Args:
        product_info: 作品情報の辞書
        
    Returns:
        プロンプト文字列
    """
    title = product_info.get("title", "")
    description = product_info.get("description", "")
    content_id = product_info.get("content_id", "")
    url = product_info.get("url", "")
    keywords = product_info.get("keywords", "")
    main_image_url = product_info.get("main_image_url", "")
    sample_images = product_info.get("sample_images", [])
    
    # サンプル画像URLリストを整形
    sample_images_list = ""
    if sample_images:
        for i, img_url in enumerate(sample_images[:10], 1):  # 最大10枚
            sample_images_list += f"   {i}. {img_url}\n"
    else:
        sample_images_list = "   （サンプル画像が見つかりませんでした）\n"
    
    # 今日の日付を取得
    today = datetime.now().strftime("%Y-%m-%d")
    
    prompt = f"""# 依頼
以下の作品データ（特に「紹介文」と「作品特徴」）を元に、例の「ｗ」多めの視聴者モードでレビューを書いて。
内容は「きれいなまとめ」にせず、一人のファンとして興奮を爆発させてｗ

# 作品データ
- 作品名： {title}
- 紹介文： {description}
- 作品ID： {content_id}
- 作品URL： {url}
- 作品特徴： {keywords}

- メイン画像URL： {main_image_url}
- サンプル画像URLリスト：
{sample_images_list}

# 指示
1. **執筆ルール:**
   - フィルター回避のため、エロワードは [K1][K2][K3] 等で伏せ字にして。
   - 「紹介文」にあるシチュエーションや、「作品特徴」にある女優の属性をしっかり本文に盛り込んで。

2. **画像の配置:**
   - 記事冒頭にメイン画像を `![{title}]({main_image_url})` で配置。
   - 記事の途中にサンプル画像をリストからランダムに数枚選んで配置（URLは改変不可）。

3. **保存処理:**
   - 記事が完成したら、以前のスクリプト同様のロジック（置換・動画コード追加）を適用した上で、以下のパスに保存するコードを実行（またはファイル作成）して。
   - 保存パス: `/Users/takahashitoshifumi/Desktop/Adult-affi/content/{today}-{content_id}.md`
   - ※ `{today}` は実行日の日付 (YYYY-MM-DD)
"""
    
    return prompt


def main():
    """メイン処理"""
    print("\n" + "=" * 80)
    print("  DMM作品URL → Cursor用プロンプト生成ツール")
    print("=" * 80 + "\n")
    
    # URL入力
    url = input("作品URLを入力してください: ").strip()
    
    if not url:
        print("❌ URLが入力されていません", file=sys.stderr)
        sys.exit(1)
    
    # スクレイピング
    print("\n🔍 作品情報を取得中...")
    product_info = scrape_dmm_product_info(url)
    
    if not product_info:
        print("❌ 作品情報の取得に失敗しました", file=sys.stderr)
        sys.exit(1)
    
    # 取得した情報を表示
    print("\n✅ 取得した情報:")
    print(f"   作品名: {product_info.get('title', '不明')}")
    print(f"   作品ID: {product_info.get('content_id', '不明')}")
    print(f"   紹介文: {product_info.get('description', '不明')[:100]}...")
    print(f"   作品特徴: {product_info.get('keywords', '不明')[:100]}...")
    print(f"   メイン画像: {product_info.get('main_image_url', '不明')[:80]}...")
    print(f"   サンプル画像: {len(product_info.get('sample_images', []))}枚")
    
    # プロンプトを生成
    print("\n📝 プロンプトを生成中...")
    prompt = generate_cursor_prompt(product_info)
    
    # クリップボードにコピー
    try:
        pyperclip.copy(prompt)
        print("\n✅ プロンプトをクリップボードにコピーしました！")
        print("\n" + "=" * 80)
        print("生成されたプロンプト:")
        print("=" * 80)
        print(prompt)
        print("=" * 80)
        print("\n💡 Cursorのチャット欄に貼り付けて使用してください。")
    except Exception as e:
        print(f"\n⚠️  クリップボードへのコピーに失敗しました: {e}", file=sys.stderr)
        print("\n生成されたプロンプト:")
        print("=" * 80)
        print(prompt)
        print("=" * 80)
        print("\n💡 上記のプロンプトを手動でコピーしてください。")


if __name__ == "__main__":
    main()

