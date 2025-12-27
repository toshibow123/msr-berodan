#!/usr/bin/env python3
"""
DMM APIを使用して商品画像URLを取得するスクリプト
"""

import os
import sys
import ssl
import urllib.request
import urllib.error
from urllib.parse import urlencode
import json

# ============================================
# 設定値（ここを編集してください）
# ============================================
API_ID = os.environ.get("DMM_API_ID", "your_api_id_here")
AFFILIATE_ID = os.environ.get("DMM_AFFILIATE_ID", "your_affiliate_id_here")

# 環境変数から取得できない場合は、直接設定してください
# API_ID = "your_actual_api_id"
# AFFILIATE_ID = "your_actual_affiliate_id"


def fetch_product_image(keyword: str, api_id: str, affiliate_id: str) -> str:
    """
    DMM APIから商品画像URLを取得
    
    Args:
        keyword: 検索キーワード（商品名や女優名など）
        api_id: DMM API ID
        affiliate_id: アフィリエイトID
        
    Returns:
        画像URL（見つからない場合は空文字列）
    """
    base_url = "https://api.dmm.com/affiliate/v3/ItemList"
    
    params = {
        "api_id": api_id,
        "affiliate_id": affiliate_id,
        "site": "FANZA",  # アダルト専用サイト
        "service": "digital",  # デジタル商品
        "floor": "videoa",  # アダルト動画
        "keyword": keyword,  # 検索キーワード
        "hits": 1,  # 1件のみ取得
        "output": "json"
    }
    
    url = f"{base_url}?{urlencode(params)}"
    
    try:
        # SSL証明書の検証をスキップ（macOS対応）
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=context, timeout=30) as response:
            data = response.read()
            api_response = json.loads(data.decode('utf-8'))
            
            # エラーチェック
            if "result" not in api_response:
                print(f"エラー: APIレスポンスが不正です", file=sys.stderr)
                return ""
            
            result = api_response["result"]
            
            # ステータスチェック
            if result.get("status") != 200:
                error_message = result.get("message", "不明なエラー")
                print(f"エラー: {error_message}", file=sys.stderr)
                return ""
            
            # 商品データの取得
            items = result.get("items", [])
            
            if not items:
                print(f"⚠️  キーワード「{keyword}」に該当する商品が見つかりませんでした", file=sys.stderr)
                return ""
            
            # 1件目の商品の画像URLを取得
            first_item = items[0]
            image_url = first_item.get("imageURL", {}).get("large", "")
            
            if not image_url:
                print(f"⚠️  商品画像URLが見つかりませんでした", file=sys.stderr)
                return ""
            
            return image_url
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else "詳細情報なし"
        print(f"HTTPエラーが発生しました: {e.code} {e.reason}", file=sys.stderr)
        print(f"エラー詳細: {error_body}", file=sys.stderr)
        return ""
    except urllib.error.URLError as e:
        print(f"URLエラーが発生しました: {e.reason}", file=sys.stderr)
        return ""
    except json.JSONDecodeError as e:
        print(f"JSONのパースに失敗しました: {e}", file=sys.stderr)
        return ""
    except KeyError as e:
        print(f"データ構造のエラー: キー '{e}' が見つかりません", file=sys.stderr)
        return ""
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}", file=sys.stderr)
        return ""


def main():
    """メイン処理"""
    # API IDとアフィリエイトIDの確認
    if API_ID == "your_api_id_here" or not API_ID:
        print("エラー: API_IDが設定されていません", file=sys.stderr)
        print("環境変数 DMM_API_ID を設定するか、スクリプト内で直接設定してください", file=sys.stderr)
        sys.exit(1)
    
    if AFFILIATE_ID == "your_affiliate_id_here" or not AFFILIATE_ID:
        print("エラー: AFFILIATE_IDが設定されていません", file=sys.stderr)
        print("環境変数 DMM_AFFILIATE_ID を設定するか、スクリプト内で直接設定してください", file=sys.stderr)
        sys.exit(1)
    
    # コマンドライン引数から検索キーワードを取得
    if len(sys.argv) < 2:
        print("使い方: python3 fetch_dmm_image.py <検索キーワード>", file=sys.stderr)
        print("例: python3 fetch_dmm_image.py 河北彩花", file=sys.stderr)
        sys.exit(1)
    
    keyword = sys.argv[1]
    
    print(f"🔍 キーワード「{keyword}」で検索中...")
    
    # 画像URLを取得
    image_url = fetch_product_image(keyword, API_ID, AFFILIATE_ID)
    
    if image_url:
        print(f"\n✅ 画像URLを取得しました:")
        print(image_url)
        sys.exit(0)
    else:
        print(f"\n❌ 画像URLの取得に失敗しました", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

