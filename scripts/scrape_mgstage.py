#!/usr/bin/env python3
"""
MGStageのデータをスクレイピングするスクリプト
官能小説サイト「艶めく物語」専用
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import random
import os
import sys
from urllib.parse import urljoin
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# .envファイルの読み込み
try:
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ .envファイルを読み込みました: {env_path}")
    else:
        print(f"⚠️  .envファイルが見つかりません: {env_path}")
except ImportError:
    print("⚠️  python-dotenvがインストールされていません。pip install python-dotenv を実行してください")
except Exception as e:
    print(f"⚠️  .envファイルの読み込みエラー: {e}")

# ==========================================
# 設定
# ==========================================
# アフィリエイトID（環境変数から取得）
AFFILIATE_ID = os.environ.get("MGS_AFFILIATE_ID")

if not AFFILIATE_ID:
    print("❌ 環境変数 MGS_AFFILIATE_ID が設定されていません", file=sys.stderr)
    print("   .envファイルに MGS_AFFILIATE_ID=YOUR_AFFILIATE_ID を設定してください", file=sys.stderr)
    sys.exit(1)

# 保存先
OUTPUT_DIR = Path(__file__).parent.parent / "data"
OUTPUT_FILE = OUTPUT_DIR / "mgs_scraped_data.json"
# 取得ページ数
MAX_PAGES = 5  # テスト用に少なめ。本番は100とかにする

# デフォルトの検索キーワード（DMMと同じようなワード）
DEFAULT_SEARCH_KEYWORDS = [
    "人妻",
    "熟女",
    "NTR",
    "ネトラレ",
    "ドラマ",
    "主婦"
]

def scrape_mgs(max_pages=MAX_PAGES, search_word=None, search_keywords=None, affiliate_id=None):
    """
    MGStageのデータをスクレイピング
    
    Args:
        max_pages: 各キーワードあたりの取得ページ数
        search_word: 検索キーワード（単一、後方互換性のため残す）
        search_keywords: 検索キーワードのリスト（複数対応）
        affiliate_id: アフィリエイトID（オプション、指定されない場合はグローバル変数を使用）
    """
    # アフィリエイトIDの決定
    actual_affiliate_id = affiliate_id or AFFILIATE_ID
    if not actual_affiliate_id:
        print("❌ アフィリエイトIDが設定されていません", file=sys.stderr)
        return []
    
    # 検索キーワードの決定
    if search_keywords:
        keywords = search_keywords
    elif search_word:
        keywords = [search_word]
    else:
        keywords = DEFAULT_SEARCH_KEYWORDS
    
    base_url = "https://www.mgstage.com/search/search.php"
    results = []
    seen_content_ids = set()  # 重複チェック用

    # セッションを作成（年齢認証のクッキーを保持するため）
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    session.headers.update(headers)
    
    # 年齢認証を通過する（クッキーを設定）
    print("🔐 年齢認証を通過中...")
    try:
        # まず年齢認証ページにアクセス
        age_check_url = "https://www.mgstage.com/search/search.php"
        age_check_response = session.get(age_check_url, timeout=10)
        
        # 年齢認証のクッキーを設定（adc=1）
        session.cookies.set('adc', '1', domain='mgstage.com', path='/')
        
        # 再度アクセスして認証が通ったか確認
        test_response = session.get(age_check_url, timeout=10)
        test_soup = BeautifulSoup(test_response.content, "html.parser")
        
        # 年齢認証ページかどうかチェック（"年齢認証"というテキストがあるか）
        if "年齢認証" in test_response.text:
            print("⚠️  年齢認証がまだ必要です。手動で確認してください。")
        else:
            print("✅ 年齢認証を通過しました")
    except Exception as e:
        print(f"⚠️  年齢認証の処理でエラーが発生しました: {e}")
        print("   続行しますが、年齢認証が必要な場合があります...")

    print("🚀 MGSデータのスクレイピングを開始します...")
    print(f"📊 各キーワードあたりの取得ページ数: {max_pages}ページ")
    print(f"🔗 アフィリエイトID: {actual_affiliate_id}")
    print(f"🔍 検索キーワード: {', '.join(keywords)}")
    print(f"📝 合計 {len(keywords)}個のキーワードで検索します\n")

    # 各キーワードで検索を実行
    for keyword_idx, keyword in enumerate(keywords, 1):
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"🔍 キーワード {keyword_idx}/{len(keywords)}: 「{keyword}」")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        keyword_results = 0
        
        for page in range(1, max_pages + 1):
            # 検索条件（例：配信開始日順、全ジャンル）
            url = f"{base_url}?sort=new&page={page}&search_word={keyword}"
            
            try:
                print(f"📄 ページ {page}/{max_pages} を取得中: {url}")
                
                # セッションを使用してリクエスト（クッキーが保持される）
                response = session.get(url, timeout=10)
                response.raise_for_status()
                response.encoding = response.apparent_encoding or 'utf-8'
                
                soup = BeautifulSoup(response.content, "html.parser")
                
                # MGStageの商品リストを取得（正しいセレクタ）
                products = soup.select(".product_list_item")
                
                if not products:
                    # フォールバック: 商品リンクから探す
                    all_links = soup.select("a[href*='/product/product_detail/']")
                    if all_links:
                        print(f"   🔍 商品リンクを {len(all_links)}件見つけました（フォールバック）")
                        # リンクの親要素を商品として扱う（.product_list_item を探す）
                        products = []
                        for link in all_links:
                            # 親要素を遡って .product_list_item を探す
                            parent = link.parent
                            while parent:
                                if 'product_list_item' in ' '.join(parent.get('class', [])):
                                    if parent not in products:
                                        products.append(parent)
                                    break
                                parent = parent.parent if parent.parent else None
                        # それでも見つからない場合は、リンクの親要素を使用
                        if not products:
                            products = [link.parent for link in all_links if link.parent]
                
                if products:
                    print(f"   🔍 商品を {len(products)}件見つかりました")
                
                # デバッグ用：常にHTMLを保存（最初のページのみ）
                if page == 1 and keyword_idx == 1:
                    debug_file = OUTPUT_DIR / f"mgs_debug_{keyword.replace('/', '_')}_{page}.html"
                    OUTPUT_DIR.mkdir(exist_ok=True)
                    try:
                        with open(debug_file, "w", encoding="utf-8") as f:
                            f.write(soup.prettify())
                        print(f"   💾 デバッグ用HTMLを保存しました: {debug_file}")
                    except Exception as e:
                        print(f"   ⚠️  HTML保存エラー: {e}")
                
                if not products:
                    # デバッグ情報を出力
                    print(f"   ⚠️  商品が見つかりませんでした。HTML構造を確認します...")
                    # 主要なクラス名を探す
                    all_classes = set()
                    for tag in soup.find_all(class_=True):
                        all_classes.update(tag.get('class', []))
                    print(f"   📋 見つかったクラス名（一部）: {sorted(list(all_classes))[:15]}")
                    # リスト要素を探す
                    lists = soup.find_all(['ul', 'ol', 'div'], class_=True)
                    print(f"   📋 リスト要素: {len(lists)}件")
                    if lists:
                        for lst in lists[:5]:
                            classes = ' '.join(lst.get('class', []))
                            if classes:
                                print(f"      <{lst.name} class='{classes}'>")
                    # HTMLを一時ファイルに保存（デバッグ用）
                    debug_file = OUTPUT_DIR / f"mgs_debug_{keyword}_{page}.html"
                    OUTPUT_DIR.mkdir(exist_ok=True)
                    with open(debug_file, "w", encoding="utf-8") as f:
                        f.write(soup.prettify())
                    print(f"   💾 デバッグ用HTMLを保存しました: {debug_file}")
                    print("⚠️ 商品が見つかりませんでした。次のページへ...")
                    continue

                page_count = 0
                for product in products:
                    try:
                        # 商品リンクを探す（/product/product_detail/を含むもののみ）
                        product_link = None
                        if product.name == "a":
                            # 商品自体がaタグの場合
                            href = product.get("href", "")
                            if "/product/product_detail/" in href:
                                product_link = product
                        else:
                            # 商品内のaタグを探す（タイトルリンクを優先）
                            title_link = product.select_one("a.title")
                            if title_link and "/product/product_detail/" in title_link.get("href", ""):
                                product_link = title_link
                            else:
                                # フォールバック: 商品内の/product/product_detail/を含むリンクを探す
                                links = product.select("a[href*='/product/product_detail/']")
                                if links:
                                    product_link = links[0]
                        
                        if not product_link:
                            continue
                        
                        link = product_link.get("href", "")
                        if not link or "/product/product_detail/" not in link:
                            continue
                        
                        # 相対URLの場合は絶対URLに変換
                        if not link.startswith("http"):
                            link = urljoin("https://www.mgstage.com", link)
                        
                        # タイトルの抽出（.title クラスのaタグから）
                        title = ""
                        title_tag = product.select_one("a.title")
                        if title_tag:
                            # span要素を除外してテキストを取得
                            title = title_tag.get_text(strip=True)
                            # ボタンなどのspanを除外
                            for span in title_tag.select("span"):
                                span_text = span.get_text(strip=True)
                                if span_text:
                                    title = title.replace(span_text, "").strip()
                        
                        # フォールバック: 他の方法でタイトルを探す
                        if not title:
                            title = product_link.text.strip()
                        if not title:
                            title_tag = product.select_one("h3, h4, h5, h6")
                            if title_tag:
                                title = title_tag.text.strip()
                        if not title:
                            img_tag = product.select_one("img")
                            if img_tag:
                                title = img_tag.get("alt", "").strip()
                        
                        if not title:
                            # 最後の手段：URLから推測
                            parts = link.split("/")
                            if parts:
                                title = parts[-1].replace(".html", "").replace("_", " ")
                        
                        if not title:
                            continue
                        
                        # 商品詳細URLにアフィリエイトIDを付与
                        separator = "&" if "?" in link else "?"
                        affiliate_url = f"{link}{separator}af={actual_affiliate_id}"
                        
                        # 画像URLの抽出
                        image_url = ""
                        # まず商品要素内のimgを探す
                        image_tag = product.select_one("img")
                        if not image_tag and product_link:
                            # aタグの親要素から探す
                            parent = product_link.parent
                            if parent:
                                image_tag = parent.select_one("img")
                        
                        if image_tag:
                            image_url = image_tag.get("src") or image_tag.get("data-src") or image_tag.get("data-original") or ""
                            if image_url:
                                # 相対URLの場合は絶対URLに変換
                                if not image_url.startswith("http"):
                                    image_url = urljoin("https://www.mgstage.com", image_url)
                        
                        # content_idを抽出（URLから）
                        content_id = ""
                        if "/product/product_detail/" in link:
                            # /product/product_detail/XXXXXX/ の形式から抽出
                            parts = link.split("/product/product_detail/")
                            if len(parts) > 1:
                                content_id = parts[1].split("/")[0].split("?")[0]
                        elif "/product/detail/" in link:
                            # フォールバック: /product/detail/XXXXXX/ の形式から抽出
                            parts = link.split("/product/detail/")
                            if len(parts) > 1:
                                content_id = parts[1].split("/")[0].split("?")[0]
                        elif "/product/" in link:
                            parts = link.split("/product/")
                            if len(parts) > 1:
                                content_id = parts[1].split("/")[0].split("?")[0]
                        elif "/" in link:
                            parts = link.rstrip("/").split("/")
                            content_id = parts[-1].split("?")[0].replace(".html", "")
                        
                        # 発売日の取得（可能であれば）
                        date_tag = product.select_one(".date, .release-date, time")
                        release_date = ""
                        if date_tag:
                            release_date = date_tag.text.strip()
                        else:
                            release_date = datetime.now().strftime("%Y-%m-%d")
                        
                        # 重複チェック（content_idが既に存在する場合はスキップ）
                        if content_id and content_id in seen_content_ids:
                            continue
                        if content_id:
                            seen_content_ids.add(content_id)
                        
                        # DMMのJSON形式に合わせる（ここが重要）
                        item_data = {
                            "rank": len(results) + 1,
                            "content_id": content_id or f"mgs_{len(results) + 1}",
                            "title": title,
                            "url": link,
                            "affiliate_url": affiliate_url,
                            "image_url": image_url,
                            "price": "",
                            "release_date": release_date,
                            "actress": [],
                            "genre": [],
                            "maker": "",
                            "director": "",
                            "description": "",
                            "service": "MGS",  # 判別用タグ
                            "search_keyword": keyword  # どのキーワードで見つかったか
                        }
                        results.append(item_data)
                        page_count += 1
                        keyword_results += 1
                        
                    except Exception as e:
                        print(f"      ⚠️  商品データの抽出エラー: {e}")
                        continue

                print(f"   ✅ {page_count}件の商品を取得しました（このページ）")
                
                # サーバー負荷対策（重要）
                if page < max_pages:
                    sleep_time = random.uniform(1.0, 3.0)
                    print(f"   ⏳ {sleep_time:.1f}秒待機中...")
                    time.sleep(sleep_time)

            except requests.exceptions.RequestException as e:
                print(f"❌ リクエストエラー: {e}")
                break
            except Exception as e:
                print(f"❌ エラー発生: {e}")
                import traceback
                traceback.print_exc()
                break
        
        print(f"✅ キーワード「{keyword}」で {keyword_results}件の商品を取得しました")
        
        # キーワード間の待機時間
        if keyword_idx < len(keywords):
            sleep_time = random.uniform(2.0, 4.0)
            print(f"⏳ 次のキーワードまで {sleep_time:.1f}秒待機中...\n")
            time.sleep(sleep_time)

    # 保存
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    output_data = {
        "fetched_at": datetime.now().isoformat(),
        "total_count": len(results),
        "affiliate_id": actual_affiliate_id,
        "ranking": results
    }
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 完了！ {len(results)}件のデータを保存しました: {OUTPUT_FILE}")
    return results

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="MGStageのデータをスクレイピング")
    parser.add_argument(
        "--pages",
        type=int,
        default=MAX_PAGES,
        help="取得するページ数"
    )
    parser.add_argument(
        "--search-word",
        type=str,
        help="検索キーワード（単一、オプション）"
    )
    parser.add_argument(
        "--search-keywords",
        type=str,
        nargs="+",
        help="検索キーワード（複数指定可能、例: --search-keywords 人妻 熟女 NTR）"
    )
    parser.add_argument(
        "--use-default-keywords",
        action="store_true",
        help="デフォルトの検索キーワードを使用（人妻、熟女、NTR、ネトラレ、ドラマ、主婦）"
    )
    parser.add_argument(
        "--affiliate-id",
        type=str,
        help="アフィリエイトID（オプション、環境変数MGS_AFFILIATE_IDが優先）"
    )
    
    args = parser.parse_args()
    
    # コマンドライン引数で指定された場合はそれを使用
    affiliate_id = args.affiliate_id or AFFILIATE_ID
    
    if not affiliate_id:
        print("❌ アフィリエイトIDが設定されていません", file=sys.stderr)
        print("   --affiliate-id オプションで指定するか、.envファイルに MGS_AFFILIATE_ID を設定してください", file=sys.stderr)
        sys.exit(1)
    
    # 検索キーワードの決定
    search_keywords = None
    if args.search_keywords:
        search_keywords = args.search_keywords
    elif args.use_default_keywords:
        search_keywords = DEFAULT_SEARCH_KEYWORDS
    elif args.search_word:
        search_keywords = [args.search_word]
    else:
        # デフォルトで複数キーワードを使用
        search_keywords = DEFAULT_SEARCH_KEYWORDS
    
    scrape_mgs(
        max_pages=args.pages, 
        search_word=args.search_word,  # 後方互換性のため残す
        search_keywords=search_keywords,
        affiliate_id=affiliate_id
    )

