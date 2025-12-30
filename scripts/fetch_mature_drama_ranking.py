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
        "filter_keywords": ["人妻", "主婦", "奥さん", "妻", "寝取られ"]
    },
    "drama": {
        "keyword": "ドラマ",
        "name": "ドラマ",
        "filter_keywords": ["ドラマ", "ストーリー", "近親相姦", "不倫", "NTR"]
    },
}


def fetch_dmm_ranking(api_id: str, affiliate_id: str, keyword: str, sort: str = "rank", hits: int = 50, offset: int = 1) -> Dict[str, Any]:
    """
    DMM APIから指定キーワードで作品を取得
    
    Args:
        api_id: DMM API ID
        affiliate_id: アフィリエイトID
        keyword: 検索キーワード
        sort: ソート順（rank, date, price）
        hits: 取得件数
        offset: オフセット
        
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
        "keyword": keyword,
        "sort": sort,
        "hits": hits,
        "offset": offset,
        "output": "json"
    }
    
    url = f"{base_url}?{urlencode(params)}"
    
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=context, timeout=30) as response:
            data = response.read()
            return json.loads(data.decode('utf-8'))
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
    
    # ジャンルフィルタリング
    if filter_keywords:
        filtered_ranking = []
        for item in ranking:
            title = item.get("title", "").lower()
            genres = [g.lower() for g in item.get("genre", [])]
            
            matches = False
            for keyword in filter_keywords:
                if keyword.lower() in title or any(keyword.lower() in g for g in genres):
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


def is_valid_mature_drama_work(item: Dict[str, Any]) -> bool:
    """熟女・人妻・ドラマに該当するかを判定"""
    genres = [g.lower() for g in item.get("genre", [])]
    title = item.get("title", "").lower()
    
    # 必須ジャンル
    valid_keywords = [
        "熟女", "人妻", "主婦", "ドラマ", "三十路", "四十路", "五十路",
        "不倫", "ntr", "寝取", "近親相姦", "義母", "義姉", "奥さん"
    ]
    
    # 除外キーワード（若い女優のみの企画もの）
    exclude_keywords = [
        "素人", "ナンパ", "マジックミラー", "mm号", "10代", "ギャル"
    ]
    
    # 除外キーワードチェック
    for keyword in exclude_keywords:
        if keyword in title or any(keyword in g for g in genres):
            return False
    
    # 必須キーワードチェック
    for keyword in valid_keywords:
        if keyword in title or any(keyword in g for g in genres):
            return True
    
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
    
    print(f"🔍 ソート順: {args.sort}")
    print(f"📊 取得件数: {args.hits}件/ジャンル")
    
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
            api_response = fetch_dmm_ranking(
                api_id,
                affiliate_id,
                keyword=genre_info['keyword'],
                sort=args.sort,
                hits=args.hits
            )
            
            ranking_data = extract_ranking_data(api_response, filter_keywords=genre_info['filter_keywords'])
            
            # 熟女・人妻・ドラマ作品のフィルタリング
            ranking_data = [item for item in ranking_data if is_valid_mature_drama_work(item)]
            
            # 既存記事を除外
            if args.exclude_existing and existing_content_ids:
                ranking_data = [item for item in ranking_data if item.get("content_id") not in existing_content_ids]
            
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


