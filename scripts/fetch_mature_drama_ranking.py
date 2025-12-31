#!/usr/bin/env python3
"""
DMM APIから熟女・人妻・ドラマ作品のランキングを取得するスクリプト
官能小説サイト「艶めく物語」専用
"""

import os
import json
import sys
import ssl
import argparse
import time
from datetime import datetime
from urllib.parse import urlencode
import urllib.request
import urllib.error
from typing import Dict, List, Any
from pathlib import Path

# .envファイルの読み込み
try:
    from dotenv import load_dotenv
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

# 熟女・人妻・ドラマジャンルの定義
MATURE_DRAMA_GENRES = {
    "mature": {
        "keyword": "熟女",
        "name": "熟女",
        "filter_keywords": ["熟女", "三十路", "四十路", "五十路", "還暦", "おばさん"]
    },
    "married": {
        "keyword": "人妻",
        "name": "人妻",
        "filter_keywords": ["人妻", "主婦", "奥さん", "妻", "寝取られ", "ネトラレ", "NTR"]
    },
    "drama": {
        "keyword": "ドラマ",
        "name": "ドラマ",
        "filter_keywords": ["ドラマ", "ストーリー", "近親相姦", "不倫", "NTR", "ネトラレ", "寝取", "寝取られ"]
    },
}


def fetch_dmm_ranking(
    api_id: str, 
    affiliate_id: str, 
    keyword: str = None,
    sort: str = "rank", 
    hits: int = 50, 
    offset: int = 1,
    genre_id: str = None,
    maker_id: str = None,
    actress_id: str = None,
    series_id: str = None,
    price_from: int = None,
    price_to: int = None,
    gte_date: str = None,
    lte_date: str = None
) -> Dict[str, Any]:
    """
    DMM APIから作品を取得
    
    Args:
        api_id: DMM API ID
        affiliate_id: アフィリエイトID
        keyword: 検索キーワード（オプション）
        sort: ソート順（rank, date, price, review）
        hits: 取得件数
        offset: オフセット
        genre_id: ジャンルID（オプション）
        maker_id: メーカーID（オプション）
        actress_id: 出演者ID（オプション）
        series_id: シリーズID（オプション）
        price_from: 価格の最小値（オプション）
        price_to: 価格の最大値（オプション）
        gte_date: 発売日の開始日（YYYY-MM-DD形式、オプション）
        lte_date: 発売日の終了日（YYYY-MM-DD形式、オプション）
        
    Returns:
        APIレスポンスのJSON
    """
    base_url = "https://api.dmm.com/affiliate/v3/ItemList"
    
    params = {
        "api_id": api_id,
        "affiliate_id": affiliate_id,
        "site": "FANZA",
        "service": "digital",
        "floor": "videoa",
        "sort": sort,
        "hits": hits,
        "offset": offset,
        "output": "json"
    }
    
    # オプションパラメータを追加
    if keyword:
        params["keyword"] = keyword
    if genre_id:
        params["genre_id"] = genre_id
    if maker_id:
        params["maker_id"] = maker_id
    if actress_id:
        params["actress_id"] = actress_id
    if series_id:
        params["series_id"] = series_id
    if price_from is not None:
        params["price_from"] = price_from
    if price_to is not None:
        params["price_to"] = price_to
    # DMM APIの日付パラメータは異なる可能性があるため、一旦コメントアウト
    # 代わりに、sort=dateでoffsetを大きくして過去のページを取得する方法を使用
    # if gte_date:
    #     params["gte_date"] = gte_date
    # if lte_date:
    #     params["lte_date"] = lte_date
    
    url = f"{base_url}?{urlencode(params)}"
    
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=context, timeout=30) as response:
            data = response.read()
            return json.loads(data.decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else "エラー詳細なし"
        print(f"❌ API取得エラー (HTTP {e.code}): {e.reason}", file=sys.stderr)
        print(f"   エラー詳細: {error_body[:200]}", file=sys.stderr)
        # デバッグ用: URLを表示（認証情報はマスク）
        debug_url = url.replace(api_id, "***API_ID***").replace(affiliate_id, "***AFFILIATE_ID***")
        print(f"   リクエストURL: {debug_url[:200]}...", file=sys.stderr)
        return {}
    except Exception as e:
        print(f"❌ API取得エラー: {e}", file=sys.stderr)
        return {}


def extract_ranking_data(api_response: Dict[str, Any], filter_keywords: List[str] = None) -> List[Dict[str, Any]]:
    """APIレスポンスから必要なデータを抽出"""
    if "result" not in api_response or "items" not in api_response["result"]:
        return []
    
    items = api_response["result"]["items"]
    ranking = []
    
    for idx, item in enumerate(items, start=1):
        ranking_item = {
            "rank": idx,
            "content_id": item.get("content_id", ""),
            "title": item.get("title", ""),
            "url": item.get("URL", ""),
            "affiliate_url": item.get("affiliateURL", ""),
            "image_url": item.get("imageURL", {}).get("large", ""),
            "price": item.get("prices", {}).get("price", ""),
            "release_date": item.get("date", ""),
            "actress": [actress.get("name", "") for actress in item.get("iteminfo", {}).get("actress", [])],
            "genre": [genre.get("name", "") for genre in item.get("iteminfo", {}).get("genre", [])],
            "maker": item.get("iteminfo", {}).get("maker", [{}])[0].get("name", "") if item.get("iteminfo", {}).get("maker") else "",
            "director": item.get("iteminfo", {}).get("director", [{}])[0].get("name", "") if item.get("iteminfo", {}).get("director") else "",
            "description": item.get("review", {}).get("text", "") if item.get("review") else "",
        }
        ranking.append(ranking_item)
    
    # ジャンルフィルタリング（緩和: タイトルまたはジャンルに含まれていればOK）
    if filter_keywords:
        filtered_ranking = []
        for item in ranking:
            title = item.get("title", "").lower()
            genres = [g.lower() for g in item.get("genre", [])]
            genres_str = " ".join(genres)
            
            matches = False
            for keyword in filter_keywords:
                keyword_lower = keyword.lower()
                # タイトルまたはジャンルに含まれていればOK
                if keyword_lower in title or keyword_lower in genres_str:
                    matches = True
                    break
            
            if matches:
                filtered_ranking.append(item)
        
        ranking = filtered_ranking
    
    return ranking


def get_existing_content_ids(content_dir: Path) -> set:
    """既存の記事からcontent_idを取得"""
    existing_ids = set()
    if not content_dir.exists():
        return existing_ids
    
    try:
        for filename in os.listdir(content_dir):
            if filename.endswith('.md'):
                parts = filename.replace('.md', '').split('-')
                if len(parts) >= 4:
                    content_id = '-'.join(parts[3:])
                    existing_ids.add(content_id)
    except Exception as e:
        print(f"⚠️  既存記事の読み込みエラー: {e}", file=sys.stderr)
    
    return existing_ids


def is_valid_mature_drama_work(item: Dict[str, Any], debug: bool = False) -> bool:
    """熟女・人妻・ドラマに該当するかを判定"""
    genres = [g.lower() for g in item.get("genre", [])]
    title = item.get("title", "").lower()
    
    # 必須ジャンル（拡張版）
    valid_keywords = [
        "熟女", "人妻", "主婦", "ドラマ", "三十路", "四十路", "五十路",
        "不倫", "ntr", "ネトラレ", "寝取", "寝取られ", "近親相姦", "義母", "義姉", "奥さん",
        "妻", "不貞", "人妻・主婦", "熟女・おばさん", "ドラマ", "ストーリー"
    ]
    
    # 除外キーワード（若い女優のみの企画もの）
    exclude_keywords = [
        "素人", "ナンパ", "マジックミラー", "mm号", "10代", "ギャル", "jk", "jc"
    ]
    
    # 除外キーワードチェック
    for keyword in exclude_keywords:
        if keyword in title or any(keyword in g for g in genres):
            if debug:
                print(f"      ❌ 除外: {keyword} が含まれています")
            return False
    
    # 必須キーワードチェック
    for keyword in valid_keywords:
        if keyword in title or any(keyword in g for g in genres):
            if debug:
                print(f"      ✅ 該当: {keyword} が含まれています")
            return True
    
    if debug:
        print(f"      ⚠️  該当なし: タイトル={title[:50]}, ジャンル={genres}")
    return False


def save_to_json(data: List[Dict[str, Any]], output_path: str) -> None:
    """データをJSON形式で保存"""
    output_data = {
        "fetched_at": datetime.now().isoformat(),
        "total_count": len(data),
        "ranking": data
    }
    
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f"✅ データを保存しました: {output_path}")
    except IOError as e:
        print(f"❌ ファイルの保存に失敗しました: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(description="熟女・人妻・ドラマ作品のランキング取得")
    parser.add_argument(
        "--genre",
        type=str,
        choices=list(MATURE_DRAMA_GENRES.keys()) + ["all"],
        default="all",
        help="取得するジャンル（allで全ジャンル取得）"
    )
    parser.add_argument(
        "--sort",
        type=str,
        choices=["rank", "date", "price"],
        default="rank",
        help="ソート順"
    )
    parser.add_argument(
        "--hits",
        type=int,
        default=50,
        help="取得件数"
    )
    parser.add_argument(
        "--exclude-existing",
        action="store_true",
        help="既存の記事と重複する作品を除外"
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["ranking", "latest", "all"],
        default="ranking",
        help="取得モード: ranking=ランキング順, latest=新着順, all=両方"
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=1,
        help="取得ページ数（1ページあたりhits件）"
    )
    parser.add_argument(
        "--genre-id",
        type=str,
        help="ジャンルIDで指定（例: 4001）"
    )
    parser.add_argument(
        "--maker-id",
        type=str,
        help="メーカーIDで指定"
    )
    parser.add_argument(
        "--actress-id",
        type=str,
        help="出演者IDで指定"
    )
    parser.add_argument(
        "--series-id",
        type=str,
        help="シリーズIDで指定"
    )
    parser.add_argument(
        "--price-from",
        type=int,
        help="価格の最小値（円）"
    )
    parser.add_argument(
        "--price-to",
        type=int,
        help="価格の最大値（円）"
    )
    parser.add_argument(
        "--date-from",
        type=str,
        help="発売日の開始日（YYYY-MM-DD形式）"
    )
    parser.add_argument(
        "--date-to",
        type=str,
        help="発売日の終了日（YYYY-MM-DD形式）"
    )
    parser.add_argument(
        "--sort-by",
        type=str,
        choices=["rank", "date", "price", "review"],
        default=None,
        help="ソート順を上書き（rank=ランキング, date=新着, price=価格, review=レビュー）"
    )
    parser.add_argument(
        "--year-from",
        type=int,
        help="取得開始年（例: 2014）"
    )
    parser.add_argument(
        "--year-to",
        type=int,
        help="取得終了年（例: 2020）"
    )
    parser.add_argument(
        "--oldest-first",
        action="store_true",
        help="古い順に取得（sort=dateでoffsetを大きくして取得）"
    )
    args = parser.parse_args()
    
    # 環境変数から認証情報を取得
    api_id = os.environ.get("DMM_API_ID")
    affiliate_id = os.environ.get("DMM_AFFILIATE_ID")
    
    if not api_id or not affiliate_id:
        print("❌ 環境変数 DMM_API_ID または DMM_AFFILIATE_ID が設定されていません", file=sys.stderr)
        sys.exit(1)
    
    # ディレクトリ設定
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    output_dir = project_root / "data"
    content_dir = project_root / "content"
    
    output_dir.mkdir(exist_ok=True)
    
    print("\n" + "✨" * 40)
    print("  熟女・人妻・ドラマ作品ランキング取得")
    print("  〜艶めく物語〜")
    print("✨" * 40 + "\n")
    
    # ソート順の決定
    sort_order = args.sort_by if args.sort_by else args.sort
    print(f"🔍 ソート順: {sort_order}")
    print(f"📊 取得件数: {args.hits}件/ジャンル")
    print(f"📄 取得モード: {args.mode}")
    if args.pages > 1:
        print(f"📄 取得ページ数: {args.pages}ページ（合計最大{args.hits * args.pages}件/ジャンル）")
    
    # 発売日範囲の設定
    date_from = args.date_from
    date_to = args.date_to
    
    if args.year_from:
        if not date_from:
            date_from = f"{args.year_from}-01-01"
        print(f"📅 取得開始年: {args.year_from}年")
    if args.year_to:
        if not date_to:
            date_to = f"{args.year_to}-12-31"
        print(f"📅 取得終了年: {args.year_to}年")
    
    if args.oldest_first:
        print(f"⏮️  古い順取得モード: 有効（sort=dateでoffsetを大きくして取得）")
    
    # 追加フィルター条件の表示
    if args.genre_id:
        print(f"🎭 ジャンルID指定: {args.genre_id}")
    if args.maker_id:
        print(f"🏭 メーカーID指定: {args.maker_id}")
    if args.actress_id:
        print(f"👤 出演者ID指定: {args.actress_id}")
    if args.series_id:
        print(f"📚 シリーズID指定: {args.series_id}")
    if args.price_from or args.price_to:
        print(f"💰 価格範囲: {args.price_from or 0}円 〜 {args.price_to or '上限なし'}円")
    if date_from or date_to:
        print(f"📅 発売日範囲: {date_from or '開始なし'} 〜 {date_to or '終了なし'}")
    
    # 既存記事の除外設定
    existing_content_ids = set()
    if args.exclude_existing:
        existing_content_ids = get_existing_content_ids(content_dir)
        print(f"🚫 既存記事除外: 有効（{len(existing_content_ids)}件）")
    
    print()
    
    # 取得するジャンルのリスト
    if args.genre == "all":
        genres_to_fetch = list(MATURE_DRAMA_GENRES.keys())
    else:
        genres_to_fetch = [args.genre]
    
    all_results = {}
    
    # 各ジャンルごとにデータ取得
    for genre_key in genres_to_fetch:
        genre_info = MATURE_DRAMA_GENRES[genre_key]
        print(f"🔄 [{genre_info['name']}] データ取得中...")
        
        try:
            all_items = []
            
            # 取得モードに応じて複数ページから取得
            if args.mode == "ranking":
                # ランキング順のみ
                sort_mode = "rank"
                pages_to_fetch = args.pages
            elif args.mode == "latest":
                # 新着順のみ
                sort_mode = "date"
                pages_to_fetch = args.pages
            else:  # all
                # ランキング順と新着順の両方
                sort_mode = "rank"
                pages_to_fetch = args.pages
            
            # 古い順取得モードの場合、offsetを大きくして過去のページを取得
            if args.oldest_first:
                sort_mode = "date"
                # 古い順に取得するため、offsetを大きく設定
                # 例: 1000件目から取得する場合、offset=1001
                base_offset = 1000  # デフォルトの開始offset
                pages_to_fetch = args.pages
            
            # 発売日範囲指定がある場合、sort=dateでoffsetを調整して取得
            # DMM APIでは直接日付範囲を指定できないため、sort=dateで大量のoffsetから取得
            if date_from or date_to:
                sort_mode = "date"
                # 日付範囲指定時は、offsetを大きくして過去のページを取得
                # 2014年から取得する場合、offsetを大きく設定
                if date_from:
                    # 2014年から取得する場合、offsetを5000程度に設定
                    try:
                        year = int(date_from.split("-")[0])
                        if year <= 2015:
                            base_offset = 5000  # 2015年以前はoffsetを大きく
                        elif year <= 2018:
                            base_offset = 3000
                        elif year <= 2020:
                            base_offset = 1000
                        else:
                            base_offset = 0
                    except:
                        base_offset = 1000
                else:
                    base_offset = 0
            
            # 複数ページから取得
            for page in range(1, pages_to_fetch + 1):
                if args.oldest_first or (date_from or date_to):
                    # 古い順または日付範囲指定: offsetを大きくして過去のページを取得
                    offset = base_offset + (page - 1) * args.hits + 1
                else:
                    offset = (page - 1) * args.hits + 1
                
                if pages_to_fetch > 1:
                    print(f"   📄 ページ {page}/{pages_to_fetch} 取得中（offset: {offset}）...")
                
                api_response = fetch_dmm_ranking(
                    api_id,
                    affiliate_id,
                    keyword=genre_info['keyword'] if not args.genre_id else None,
                    sort=sort_order,
                    hits=args.hits,
                    offset=offset,
                    genre_id=args.genre_id,
                    maker_id=args.maker_id,
                    actress_id=args.actress_id,
                    series_id=args.series_id,
                    price_from=args.price_from,
                    price_to=args.price_to,
                    gte_date=None,  # DMM APIでは直接日付範囲指定ができないため、Noneに設定
                    lte_date=None   # sort=dateでoffsetを調整して取得
                )
                
                page_data = extract_ranking_data(api_response, filter_keywords=genre_info['filter_keywords'])
                all_items.extend(page_data)
                
                # ページ間で少し待機（API負荷軽減）
                if page < pages_to_fetch:
                    time.sleep(1)
            
            # allモードの場合、新着順も取得
            if args.mode == "all":
                print(f"   📄 新着順も取得中...")
                for page in range(1, args.pages + 1):
                    offset = (page - 1) * args.hits + 1
                    if args.pages > 1:
                        print(f"   📄 新着順 ページ {page}/{args.pages} 取得中（offset: {offset}）...")
                    
                    api_response = fetch_dmm_ranking(
                        api_id,
                        affiliate_id,
                        keyword=genre_info['keyword'] if not args.genre_id else None,
                        sort="date",
                        hits=args.hits,
                        offset=offset,
                        genre_id=args.genre_id,
                        maker_id=args.maker_id,
                        actress_id=args.actress_id,
                        series_id=args.series_id,
                        price_from=args.price_from,
                        price_to=args.price_to,
                        gte_date=date_from,
                        lte_date=date_to
                    )
                    
                    page_data = extract_ranking_data(api_response, filter_keywords=genre_info['filter_keywords'])
                    all_items.extend(page_data)
                    
                    # ページ間で少し待機
                    if page < args.pages:
                        time.sleep(1)
            
            # 重複を除去（content_idでユニーク化）
            seen_ids = set()
            unique_items = []
            for item in all_items:
                if item.get("content_id") not in seen_ids:
                    seen_ids.add(item.get("content_id"))
                    unique_items.append(item)
            
            ranking_data = unique_items
            print(f"   📊 フィルタリング前: {len(ranking_data)}件（重複除去後）")
            
            # 熟女・人妻・ドラマ作品のフィルタリング
            before_count = len(ranking_data)
            ranking_data = [item for item in ranking_data if is_valid_mature_drama_work(item)]
            after_count = len(ranking_data)
            print(f"   📊 バリデーション後: {after_count}件 (除外: {before_count - after_count}件)")
            
            # 既存記事を除外
            if args.exclude_existing and existing_content_ids:
                before_exclude = len(ranking_data)
                ranking_data = [item for item in ranking_data if item.get("content_id") not in existing_content_ids]
                after_exclude = len(ranking_data)
                print(f"   📊 既存記事除外後: {after_exclude}件 (除外: {before_exclude - after_exclude}件)")
            
            # ランク番号を振り直す
            for idx, item in enumerate(ranking_data, start=1):
                item["rank"] = idx
            
            if not ranking_data:
                print(f"   ⚠️  {genre_info['name']}の作品が見つかりませんでした")
                continue
            
            print(f"   ✅ {len(ranking_data)}件の作品を取得しました")
            
            # JSONファイルを保存
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            genre_output_path = output_dir / f"mature_drama_{genre_key}_{timestamp}.json"
            genre_latest_path = output_dir / f"mature_drama_{genre_key}_latest.json"
            
            save_to_json(ranking_data, str(genre_output_path))
            save_to_json(ranking_data, str(genre_latest_path))
            
            all_results[genre_key] = {
                "genre_name": genre_info['name'],
                "data": ranking_data
            }
            
            # TOP5表示
            print(f"\n   📈 {genre_info['name']} TOP5:")
            for item in ranking_data[:5]:
                actresses = "、".join(item['actress'][:2]) if item['actress'] else "不明"
                print(f"      {item['rank']:2d}. {item['title'][:40]}... ({actresses})")
            print()
            
            time.sleep(1)  # API負荷軽減
            
        except Exception as e:
            print(f"   ❌ エラー: {e}", file=sys.stderr)
            continue
    
    # 全ジャンル統合ファイルを保存
    if len(genres_to_fetch) > 1:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        combined_latest_path = output_dir / "mature_drama_all_latest.json"
        
        # 全ジャンルのデータを統合
        all_items = []
        for result in all_results.values():
            all_items.extend(result['data'])
        
        # 重複を除去（content_idでユニーク化）
        seen_ids = set()
        unique_items = []
        for item in all_items:
            if item['content_id'] not in seen_ids:
                seen_ids.add(item['content_id'])
                unique_items.append(item)
        
        save_to_json(unique_items, str(combined_latest_path))
        print(f"✅ 全ジャンル統合（重複除去後）: {len(unique_items)}件")
    
    print("\n" + "=" * 80)
    print("📊 取得完了サマリー:")
    print("=" * 80)
    total_count = 0
    for genre_key, result in all_results.items():
        count = len(result['data'])
        total_count += count
        print(f"  {result['genre_name']}: {count}件")
    print(f"\n  合計: {total_count}件")
    print("=" * 80)
    print("\n💡 次のステップ:")
    print("   python3 scripts/bulk_generate_mature_drama_articles.py")
    print()


if __name__ == "__main__":
    main()


