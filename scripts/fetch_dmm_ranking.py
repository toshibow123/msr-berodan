#!/usr/bin/env python3
"""
DMM APIからニッチジャンルのアダルト動画の人気作品を取得するスクリプト
複数のジャンルに対応
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
from typing import Dict, List, Any, Optional

# ニッチジャンルの定義
NICHE_GENRES = {
    "drama": {
        "keyword": "ドラマ",
        "name": "ドラマ・ストーリー系",
        "filter_keywords": ["ドラマ", "ストーリー", "story", "drama"]
    },
    "reverse_ntr": {
        "keyword": "逆NTR",
        "name": "逆NTR専門",
        "filter_keywords": ["逆NTR", "逆寝取られ", "M男", "女性上位"]
    },
    "danchi": {
        "keyword": "団地妻",
        "name": "団地妻・人妻ドラマ",
        "filter_keywords": ["団地妻", "人妻", "近所の奥さん"]
    },
    "giri": {
        "keyword": "義母",
        "name": "義理の関係専門",
        "filter_keywords": ["義母", "義姉", "義妹", "義理"]
    },
    "debut": {
        "keyword": "新人",
        "name": "新人AV女優デビュー作",
        "filter_keywords": ["新人", "デビュー", "初撮り", "初めて"]
    },
    "height": {
        "keyword": "小柄",
        "name": "身長差カップル",
        "filter_keywords": ["小柄", "身長差", "体格差", "150cm"]
    },
    "dialect": {
        "keyword": "関西弁",
        "name": "方言女子専門",
        "filter_keywords": ["関西弁", "博多弁", "方言", "大阪弁"]
    },
    "glasses": {
        "keyword": "眼鏡",
        "name": "眼鏡っ子・インテリ系",
        "filter_keywords": ["眼鏡", "インテリ", "教師", "秘書", "メガネ"]
    },
    "location": {
        "keyword": "温泉",
        "name": "ロケーション別作品",
        "filter_keywords": ["温泉", "海", "野外", "ビーチ", "ロケ"]
    },
    "acting": {
        "keyword": "演技",
        "name": "演技力重視作品",
        "filter_keywords": ["演技", "ドラマ", "ストーリー", "演出"]
    }
}


def fetch_dmm_ranking(api_id: str, affiliate_id: str, keyword: str, sort: str = "rank", hits: int = 20, offset: int = 1) -> Dict[str, Any]:
    """
    DMM APIから指定キーワードでアダルト動画の人気作品を取得
    
    Args:
        api_id: DMM API ID
        affiliate_id: アフィリエイトID
        keyword: 検索キーワード
        sort: ソート順（rank, date, price）
        hits: 取得件数
        offset: オフセット（ページネーション用、1から開始）
        
    Returns:
        APIレスポンスのJSON
    """
    base_url = "https://api.dmm.com/affiliate/v3/ItemList"
    
    params = {
        "api_id": api_id,
        "affiliate_id": affiliate_id,
        "site": "FANZA",  # アダルト専用サイト
        "service": "digital",  # デジタル商品
        "floor": "videoa",  # アダルト動画
        "keyword": keyword,  # キーワード検索
        "sort": sort,  # ソート順
        "hits": hits,  # 取得件数
        "offset": offset,  # オフセット
        "output": "json"
    }
    
    url = f"{base_url}?{urlencode(params)}"
    
    # デバッグ用：URLを表示（認証情報はマスク）
    debug_url = url.replace(api_id, "***API_ID***").replace(affiliate_id, "***AFFILIATE_ID***")
    print(f"🔍 リクエストURL: {debug_url}")
    
    try:
        # macOSでSSL証明書が見つからない場合の対策
        # SSL検証をスキップするコンテキストを作成
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(url)
        # contextを明示的に指定
        with urllib.request.urlopen(req, context=context, timeout=30) as response:
            data = response.read()
            return json.loads(data.decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else "詳細情報なし"
        print(f"HTTPエラーが発生しました: {e.code} {e.reason}", file=sys.stderr)
        print(f"エラー詳細: {error_body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"URLエラーが発生しました: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"JSONのパースに失敗しました: {e}", file=sys.stderr)
        sys.exit(1)


def extract_ranking_data(api_response: Dict[str, Any], filter_keywords: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    APIレスポンスから必要なデータを抽出し、フィルタリング
    
    Args:
        api_response: DMM APIのレスポンス
        filter_keywords: フィルタリング用キーワードリスト
        
    Returns:
        整形されたランキングデータ
    """
    if "result" not in api_response or "items" not in api_response["result"]:
        print("APIレスポンスが予期しない形式です", file=sys.stderr)
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
            "maker": item.get("iteminfo", {}).get("maker", [{}])[0].get("name", "") if item.get("iteminfo", {}).get("maker") else ""
        }
        ranking.append(ranking_item)
    
    # フィルタリング処理
    if filter_keywords:
        filtered_ranking = []
        for item in ranking:
            title = item.get("title", "").lower()
            genres = [g.lower() for g in item.get("genre", [])]
            
            # タイトルまたはジャンルにキーワードが含まれるかチェック
            matches = False
            for keyword in filter_keywords:
                if keyword.lower() in title or any(keyword.lower() in g for g in genres):
                    matches = True
                    break
            
            if matches:
                filtered_ranking.append(item)
        
        ranking = filtered_ranking
    
    return ranking


def get_existing_content_ids(content_dir: str) -> set:
    """
    既存の記事からcontent_idを取得
    
    Args:
        content_dir: contentディレクトリのパス
        
    Returns:
        content_idのセット
    """
    existing_ids = set()
    if not os.path.exists(content_dir):
        return existing_ids
    
    try:
        for filename in os.listdir(content_dir):
            if filename.endswith('.md'):
                # ファイル名からcontent_idを抽出（例: 2025-12-14-1start00473.md -> 1start00473）
                parts = filename.replace('.md', '').split('-')
                if len(parts) >= 4:
                    content_id = '-'.join(parts[3:])  # 日付部分を除いた残り
                    existing_ids.add(content_id)
    except Exception as e:
        print(f"⚠️  既存記事の読み込みエラー: {e}", file=sys.stderr)
    
    return existing_ids


def save_to_json(data: List[Dict[str, Any]], output_path: str) -> None:
    """
    データをJSON形式で保存
    
    Args:
        data: 保存するデータ
        output_path: 保存先のファイルパス
    """
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
        print(f"ファイルの保存に失敗しました: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """メイン処理"""
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(description="DMM APIからニッチジャンルの動画データを取得")
    parser.add_argument(
        "--genre",
        type=str,
        choices=list(NICHE_GENRES.keys()) + ["all"],
        default="drama",
        help="取得するジャンル（allで全ジャンル取得）"
    )
    parser.add_argument(
        "--sort",
        type=str,
        choices=["rank", "date", "price"],
        default="rank",
        help="ソート順（rank: ランキング順, date: 最新順, price: 価格順）"
    )
    parser.add_argument(
        "--hits",
        type=int,
        default=20,
        help="取得件数"
    )
    parser.add_argument(
        "--past",
        action="store_true",
        help="過去作を取得（ランキング以外からも取得）"
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=3,
        help="過去作取得時のページ数（1ページあたりhits件）"
    )
    parser.add_argument(
        "--exclude-existing",
        action="store_true",
        help="既存の記事（content/フォルダ）と重複する作品を除外"
    )
    args = parser.parse_args()
    
    # 環境変数から認証情報を取得
    api_id = os.environ.get("DMM_API_ID")
    affiliate_id = os.environ.get("DMM_AFFILIATE_ID")
    
    if not api_id:
        print("エラー: 環境変数 DMM_API_ID が設定されていません", file=sys.stderr)
        sys.exit(1)
    
    if not affiliate_id:
        print("エラー: 環境変数 DMM_AFFILIATE_ID が設定されていません", file=sys.stderr)
        sys.exit(1)
    
    # 出力先ディレクトリを作成
    output_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(output_dir, exist_ok=True)
    
    # 取得するジャンルのリスト
    if args.genre == "all":
        genres_to_fetch = list(NICHE_GENRES.keys())
    else:
        genres_to_fetch = [args.genre]
    
    print(f"📝 API ID: {api_id[:10]}... (マスク済み)")
    print(f"📝 アフィリエイトID: {affiliate_id}")
    print(f"🔍 ソート順: {args.sort}")
    print(f"📊 取得件数: {args.hits}件/ジャンル")
    print(f"🎯 取得ジャンル数: {len(genres_to_fetch)}個")
    if args.past:
        print(f"📚 過去作取得モード: 有効（{args.pages}ページ分）")
    if args.exclude_existing:
        print(f"🚫 既存記事除外: 有効")
    print()
    
    # 既存記事のcontent_idを取得（除外機能が有効な場合）
    existing_content_ids = set()
    if args.exclude_existing:
        content_dir = os.path.join(os.path.dirname(__file__), "..", "content")
        existing_content_ids = get_existing_content_ids(content_dir)
        print(f"📋 既存記事数: {len(existing_content_ids)}件")
        if existing_content_ids:
            print(f"   除外対象: {', '.join(list(existing_content_ids)[:5])}{'...' if len(existing_content_ids) > 5 else ''}")
        print()
    
    # 各ジャンルごとにデータ取得
    all_results = {}
    
    for genre_key in genres_to_fetch:
        genre_info = NICHE_GENRES[genre_key]
        print(f"🔄 [{genre_info['name']}] データ取得中...")
        print(f"   キーワード: {genre_info['keyword']}")
        
        try:
            all_items = []
            
            # 過去作取得モードの場合、複数ページから取得
            if args.past:
                for page in range(1, args.pages + 1):
                    offset = (page - 1) * args.hits + 1
                    print(f"   📄 ページ {page} 取得中（offset: {offset}）...")
                    
                    api_response = fetch_dmm_ranking(
                        api_id, 
                        affiliate_id, 
                        keyword=genre_info['keyword'],
                        sort="date" if args.past else args.sort,  # 過去作取得時は新着順
                        hits=args.hits,
                        offset=offset
                    )
                    
                    page_data = extract_ranking_data(api_response, filter_keywords=genre_info['filter_keywords'])
                    all_items.extend(page_data)
                    
                    # 既存記事を除外
                    if args.exclude_existing and existing_content_ids:
                        all_items = [item for item in all_items if item.get("content_id") not in existing_content_ids]
                    
                    # ページ間で少し待機（API負荷軽減）
                    if page < args.pages:
                        time.sleep(1)
                
                ranking_data = all_items
            else:
                # 通常モード（1ページのみ）
                api_response = fetch_dmm_ranking(
                    api_id, 
                    affiliate_id, 
                    keyword=genre_info['keyword'],
                    sort=args.sort,
                    hits=args.hits
                )
                
                ranking_data = extract_ranking_data(api_response, filter_keywords=genre_info['filter_keywords'])
                
                # 既存記事を除外
                if args.exclude_existing and existing_content_ids:
                    ranking_data = [item for item in ranking_data if item.get("content_id") not in existing_content_ids]
            
            # 最大件数までに制限
            ranking_data = ranking_data[:args.hits * (args.pages if args.past else 1)]
            
            # ランク番号を1から振り直す
            for idx, item in enumerate(ranking_data, start=1):
                item["rank"] = idx
            
            if not ranking_data:
                print(f"   ⚠️  {genre_info['name']}の作品が見つかりませんでした")
                continue
            
            print(f"   ✅ {len(ranking_data)}件の作品を取得しました")
            
            # ジャンルごとにJSONファイルを保存
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            genre_output_path = os.path.join(output_dir, f"dmm_ranking_{genre_key}_{timestamp}.json")
            genre_latest_path = os.path.join(output_dir, f"dmm_ranking_{genre_key}_latest.json")
            
            save_to_json(ranking_data, genre_output_path)
            save_to_json(ranking_data, genre_latest_path)
            
            all_results[genre_key] = {
                "genre_name": genre_info['name'],
                "data": ranking_data
            }
            
            # 簡易表示
            print(f"\n   📈 {genre_info['name']} ランキング TOP5:")
            for item in ranking_data[:5]:
                print(f"      {item['rank']:2d}. {item['title'][:50]}...")
            print()
            
        except Exception as e:
            print(f"   ❌ エラー: {e}", file=sys.stderr)
            continue
    
    # 全ジャンルをまとめたファイルも保存（オプション）
    if len(genres_to_fetch) > 1:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        combined_path = os.path.join(output_dir, f"dmm_ranking_all_{timestamp}.json")
        combined_latest_path = os.path.join(output_dir, "dmm_ranking_all_latest.json")
        
        combined_data = {
            "fetched_at": datetime.now().isoformat(),
            "genres": all_results
        }
        
        with open(combined_path, "w", encoding="utf-8") as f:
            json.dump(combined_data, f, ensure_ascii=False, indent=2)
        with open(combined_latest_path, "w", encoding="utf-8") as f:
            json.dump(combined_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 全ジャンル統合データを保存しました: {combined_latest_path}")
    
    print("\n" + "=" * 80)
    print("📊 取得完了サマリー:")
    print("=" * 80)
    for genre_key, result in all_results.items():
        print(f"  {result['genre_name']}: {len(result['data'])}件")
    print("=" * 80)


if __name__ == "__main__":
    main()

