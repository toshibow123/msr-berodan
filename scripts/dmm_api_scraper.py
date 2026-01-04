#!/usr/bin/env python3
"""
DMM API を使用してアダルト動画データを取得するスクリプト

要件:
- 特定キーワード（熟女、人妻等）を含む作品を検索
- ベスト・総集編を除外
- 女優名が存在する作品のみを対象
- 重複除去とレート制限対応
"""

import os
import json
import time
import requests
from typing import List, Dict, Set, Optional
from datetime import datetime
from dotenv import load_dotenv

# 環境変数を読み込み（親ディレクトリの.envファイルを参照）
load_dotenv('../.env')

class DMMAPIScraper:
    def __init__(self):
        """DMM API スクレイパーの初期化"""
        self.api_id = os.getenv('DMM_API_ID')
        self.affiliate_id = os.getenv('DMM_AFFILIATE_ID')
        
        if not self.api_id or not self.affiliate_id:
            raise ValueError("DMM_API_ID と DMM_AFFILIATE_ID を .env ファイルに設定してください")
        
        # DMM API v3 公式エンドポイント（年齢認証対応）
        self.base_url = "https://api.dmm.com/affiliate/v3/ItemList"
        self.collected_ids: Set[str] = set()  # 重複防止用
        
        # セッション設定（年齢認証突破用）
        self.session = requests.Session()
        self.setup_session()
        
        # 検索対象キーワード（包含タグ）
        self.include_keywords = [
            'お母さん', '女将・女主人', '義母', '熟女', 
            '寝取り・寝取られ・NTR', '人妻・主婦', '未亡人', 
            'ママ友', '若妻・幼妻', '妊婦', 'ドラマ'
        ]
        
        # 除外キーワード
        self.exclude_keywords = ['ベスト・総集編', 'ベスト', '総集編']
        
        print(f"🚀 DMM API スクレイパー初期化完了")
        print(f"📋 検索キーワード: {', '.join(self.include_keywords)}")
        print(f"🚫 除外キーワード: {', '.join(self.exclude_keywords)}")

    def setup_session(self):
        """
        年齢認証突破用のセッション設定
        """
        # 年齢認証突破用のヘッダー
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8',
            'Accept-Language': 'ja-JP,ja;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
        
        # 年齢認証突破用のCookie
        cookies = {
            'age_check_done': '1',
            'ckcy': '1',
            'cklg': 'ja',
            'region': 'JP',
            'timezone': 'Asia/Tokyo',
            'adult_check_done': '1',
            'over18': '1'
        }
        
        self.session.headers.update(headers)
        
        # Cookieを個別に設定（重複回避）
        for name, value in cookies.items():
            self.session.cookies.set(name, value, domain='.dmm.com')
        
        print(f"🍪 年齢認証Cookie設定完了: {len(cookies)}個のCookieを設定")
        
        # 事前に年齢認証を突破
        self.bypass_age_verification()

    def bypass_age_verification(self):
        """
        事前に年齢認証ページにアクセスしてCookieを確実に設定
        """
        try:
            print(f"🔓 年齢認証突破を実行中...")
            
            # DMM トップページにアクセス
            dmm_top = "https://www.dmm.co.jp/"
            response = self.session.get(dmm_top, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ DMM トップページアクセス成功")
                
                # 年齢認証ページが表示された場合の処理
                if 'age_check' in response.url or 'rating' in response.url:
                    print(f"🚫 年齢認証ページを検出、突破を試行...")
                    
                    # 年齢認証フォームの送信を模擬
                    age_check_data = {
                        'age_check_done': '1',
                        'redirect_url': '/',
                        'submit': '同意する'
                    }
                    
                    age_response = self.session.post(
                        response.url,
                        data=age_check_data,
                        timeout=10,
                        allow_redirects=True
                    )
                    
                    if age_response.status_code == 200:
                        print(f"✅ 年齢認証突破成功")
                    else:
                        print(f"⚠️  年齢認証突破に失敗: {age_response.status_code}")
                else:
                    print(f"✅ 年齢認証は不要でした")
                    
            else:
                print(f"⚠️  DMM トップページアクセス失敗: {response.status_code}")
                
        except Exception as e:
            print(f"⚠️  年齢認証突破でエラー: {e}")
            print(f"💡 Cookieによる認証を継続します")

    def search_videos(self, keyword: str, offset: int = 1, hits: int = 100) -> Optional[Dict]:
        """
        指定キーワードで動画を検索
        
        Args:
            keyword: 検索キーワード
            offset: 検索開始位置
            hits: 取得件数（最大100）
        
        Returns:
            APIレスポンス（辞書形式）またはNone
        """
        params = {
            'api_id': self.api_id,
            'affiliate_id': self.affiliate_id,
            'site': 'FANZA',
            'service': 'digital',
            'floor': 'videoa',  # アダルト動画フロア
            'hits': min(hits, 100),  # 最大100件
            'offset': offset,
            'keyword': keyword,
            'output': 'json',
            'sort': 'date'  # 発売日順でソート
        }
        
        try:
            print(f"🔍 検索中: '{keyword}' (offset: {offset})")
            
            # リクエスト固有のヘッダーを追加
            request_headers = {
                'Referer': 'https://www.dmm.co.jp/',
                'Origin': 'https://www.dmm.co.jp'
            }
            
            # 既存のセッションヘッダーに追加
            temp_headers = self.session.headers.copy()
            temp_headers.update(request_headers)
            
            response = self.session.get(
                self.base_url, 
                params=params,
                headers=request_headers,
                timeout=30,
                allow_redirects=True
            )
            
            print(f"📡 リクエストURL: {response.url}")
            print(f"📊 ステータスコード: {response.status_code}")
            
            # Cookie情報を安全に表示（重複回避）
            cookie_info = []
            for cookie in self.session.cookies:
                cookie_info.append(f"{cookie.name}={cookie.value}")
            print(f"🍪 送信Cookie: {'; '.join(cookie_info)}")
            
            response.raise_for_status()
            
            # レスポンス内容の詳細チェック
            content_type = response.headers.get('Content-Type', '')
            print(f"📋 Content-Type: {content_type}")
            
            # HTMLレスポンスの場合（年齢認証ページなど）
            if 'text/html' in content_type:
                print(f"⚠️  HTMLレスポンスを受信（年齢認証ページの可能性）")
                
                # HTMLタイトルを抽出してデバッグ情報として表示
                html_content = response.text
                title_start = html_content.find('<title>')
                title_end = html_content.find('</title>')
                
                if title_start != -1 and title_end != -1:
                    title = html_content[title_start + 7:title_end]
                    print(f"📄 ページタイトル: {title}")
                
                # 年齢認証関連のキーワードをチェック
                age_check_keywords = ['年齢確認', '18歳以上', 'age verification', 'rating']
                for keyword in age_check_keywords:
                    if keyword in html_content:
                        print(f"🚫 年齢認証ページを検出: '{keyword}' が含まれています")
                        break
                
                print(f"📄 レスポンス内容（最初の500文字）:")
                print(f"{html_content[:500]}...")
                return None
            
            # JSONレスポンスの処理
            try:
                data = response.json()
            except json.JSONDecodeError as json_error:
                print(f"❌ JSON デコードエラー: {json_error}")
                print(f"📄 レスポンス内容（最初の500文字）:")
                print(f"{response.text[:500]}...")
                
                # XMLレスポンスの可能性もチェック
                if response.text.strip().startswith('<?xml'):
                    print(f"📋 XMLレスポンスを検出")
                elif response.text.strip().startswith('<html'):
                    print(f"📋 HTMLレスポンスを検出")
                
                return None
            
            # APIエラーレスポンスのチェック
            if 'error' in data:
                error_info = data['error']
                print(f"❌ API エラー: {error_info}")
                
                # エラーの詳細情報があれば表示
                if isinstance(error_info, dict):
                    error_code = error_info.get('code', 'Unknown')
                    error_message = error_info.get('message', 'No message')
                    print(f"   エラーコード: {error_code}")
                    print(f"   エラーメッセージ: {error_message}")
                
                return None
            
            # 正常なレスポンスの処理
            if 'result' in data and 'items' in data['result']:
                total_count = data['result'].get('total_count', 0)
                items_count = len(data['result']['items'])
                print(f"✅ 取得成功: {items_count}件 (総件数: {total_count}件)")
                return data
            else:
                print(f"⚠️  検索結果なし: '{keyword}'")
                print(f"📋 レスポンス構造: {list(data.keys()) if data else 'Empty'}")
                
                # レスポンス構造の詳細を表示
                if data:
                    for key, value in data.items():
                        if isinstance(value, dict):
                            print(f"   {key}: {list(value.keys())}")
                        elif isinstance(value, list):
                            print(f"   {key}: リスト（{len(value)}件）")
                        else:
                            print(f"   {key}: {type(value).__name__}")
                
                return None
                
        except requests.exceptions.ConnectionError as e:
            print(f"❌ 接続エラー: {e}")
            print(f"💡 ヒント: ネットワーク接続またはDNS設定を確認してください")
            return None
        except requests.exceptions.Timeout as e:
            print(f"❌ タイムアウトエラー: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ API リクエストエラー: {e}")
            return None

    def is_valid_item(self, item: Dict) -> bool:
        """
        アイテムが取得条件を満たすかチェック
        
        Args:
            item: APIから取得したアイテムデータ
        
        Returns:
            有効な場合True
        """
        # content_id の重複チェック
        content_id = item.get('content_id', '')
        if content_id in self.collected_ids:
            return False
        
        # 女優名の存在チェック
        actresses = item.get('iteminfo', {}).get('actress', [])
        if not actresses or len(actresses) == 0:
            return False
        
        # 女優名が空でないかチェック
        valid_actresses = [a for a in actresses if a.get('name', '').strip()]
        if not valid_actresses:
            return False
        
        # ジャンル情報の取得
        genres = item.get('iteminfo', {}).get('genre', [])
        genre_names = [g.get('name', '') for g in genres]
        
        # 除外キーワードのチェック
        for exclude_keyword in self.exclude_keywords:
            if any(exclude_keyword in genre_name for genre_name in genre_names):
                print(f"🚫 除外: {item.get('title', 'Unknown')} (理由: {exclude_keyword})")
                return False
        
        return True

    def extract_item_data(self, item: Dict) -> Dict:
        """
        APIレスポンスから必要なデータを抽出
        
        Args:
            item: APIから取得したアイテムデータ
        
        Returns:
            抽出されたデータ辞書
        """
        # 基本情報
        content_id = item.get('content_id', '')
        title = item.get('title', '')
        
        # 女優名の抽出
        actresses = item.get('iteminfo', {}).get('actress', [])
        actress_names = [a.get('name', '') for a in actresses if a.get('name', '').strip()]
        
        # ジャンル情報の抽出
        genres = item.get('iteminfo', {}).get('genre', [])
        genre_names = [g.get('name', '') for g in genres]
        
        # 画像URL
        package_images = item.get('imageURL', {})
        package_url = package_images.get('large', '') or package_images.get('medium', '') or package_images.get('small', '')
        
        # サンプル画像
        sample_images = item.get('sampleImageURL', {}).get('sample_s', {}).get('image', [])
        
        # アフィリエイトURL
        affiliate_url = item.get('affiliateURL', '')
        
        # 発売日
        date = item.get('date', '')
        
        return {
            'content_id': content_id,
            'title': title,
            'actress': ', '.join(actress_names),
            'actresses': actress_names,
            'genres': genre_names,
            'package_image': package_url,
            'sample_images': sample_images,
            'affiliate_url': affiliate_url,
            'date': date,
            'collected_at': datetime.now().isoformat()
        }

    def collect_all_videos(self, max_per_keyword: int = 500) -> List[Dict]:
        """
        全キーワードで動画データを収集
        
        Args:
            max_per_keyword: キーワードあたりの最大取得件数
        
        Returns:
            収集されたビデオデータのリスト
        """
        all_videos = []
        
        for keyword in self.include_keywords:
            print(f"\n🎯 キーワード '{keyword}' の検索開始")
            
            offset = 1
            keyword_count = 0
            
            while keyword_count < max_per_keyword:
                # API レート制限対応
                time.sleep(1)  # 1秒待機
                
                # 検索実行
                response_data = self.search_videos(keyword, offset=offset, hits=100)
                
                if not response_data or 'result' not in response_data:
                    print(f"⚠️  '{keyword}' の検索終了（データなし）")
                    break
                
                items = response_data['result'].get('items', [])
                if not items:
                    print(f"⚠️  '{keyword}' の検索終了（アイテムなし）")
                    break
                
                # アイテムの処理
                valid_items = 0
                for item in items:
                    if self.is_valid_item(item):
                        video_data = self.extract_item_data(item)
                        all_videos.append(video_data)
                        self.collected_ids.add(video_data['content_id'])
                        valid_items += 1
                        keyword_count += 1
                        
                        if keyword_count >= max_per_keyword:
                            break
                
                print(f"📊 '{keyword}': {valid_items}件の有効なアイテムを追加 (累計: {len(all_videos)}件)")
                
                # 次のページへ
                offset += len(items)
                
                # 取得件数が100件未満の場合は最後のページ
                if len(items) < 100:
                    print(f"✅ '{keyword}' の検索完了（最終ページ）")
                    break
        
        print(f"\n🎉 全検索完了! 総取得件数: {len(all_videos)}件")
        return all_videos

    def save_to_json(self, videos: List[Dict], filename: str = 'actress_videos.json'):
        """
        収集したデータをJSONファイルに保存
        
        Args:
            videos: ビデオデータのリスト
            filename: 保存ファイル名
        """
        try:
            # 統計情報の追加
            metadata = {
                'total_count': len(videos),
                'collected_at': datetime.now().isoformat(),
                'keywords_used': self.include_keywords,
                'excluded_keywords': self.exclude_keywords,
                'unique_actresses': len(set(v['actress'] for v in videos)),
                'videos': videos
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            print(f"💾 データ保存完了: {filename}")
            print(f"📊 統計:")
            print(f"   - 総作品数: {metadata['total_count']}件")
            print(f"   - ユニーク女優数: {metadata['unique_actresses']}人")
            
        except Exception as e:
            print(f"❌ ファイル保存エラー: {e}")

    def display_summary(self, videos: List[Dict]):
        """
        収集結果のサマリーを表示
        
        Args:
            videos: ビデオデータのリスト
        """
        if not videos:
            print("📋 収集されたデータがありません")
            return
        
        print(f"\n📋 収集サマリー")
        print(f"{'='*50}")
        
        # 女優別の作品数
        actress_count = {}
        genre_count = {}
        
        for video in videos:
            actress = video['actress']
            actress_count[actress] = actress_count.get(actress, 0) + 1
            
            for genre in video['genres']:
                genre_count[genre] = genre_count.get(genre, 0) + 1
        
        # 上位女優
        print(f"\n👑 作品数上位女優 (TOP 10):")
        sorted_actresses = sorted(actress_count.items(), key=lambda x: x[1], reverse=True)
        for i, (actress, count) in enumerate(sorted_actresses[:10], 1):
            print(f"   {i:2d}. {actress}: {count}作品")
        
        # 上位ジャンル
        print(f"\n🏷️  人気ジャンル (TOP 10):")
        sorted_genres = sorted(genre_count.items(), key=lambda x: x[1], reverse=True)
        for i, (genre, count) in enumerate(sorted_genres[:10], 1):
            print(f"   {i:2d}. {genre}: {count}作品")
        
        # 最新作品
        print(f"\n🆕 最新作品 (TOP 5):")
        sorted_videos = sorted(videos, key=lambda x: x['date'], reverse=True)
        for i, video in enumerate(sorted_videos[:5], 1):
            print(f"   {i}. {video['title'][:50]}... ({video['actress']}) - {video['date']}")


def main():
    """メイン実行関数"""
    print("🎬 DMM API アダルト動画データ収集スクリプト")
    print("=" * 60)
    
    try:
        # スクレイパーの初期化
        scraper = DMMAPIScraper()
        
        # データ収集の実行
        print(f"\n🚀 データ収集開始...")
        videos = scraper.collect_all_videos(max_per_keyword=200)  # キーワードあたり200件まで
        
        if videos:
            # 結果の表示
            scraper.display_summary(videos)
            
            # JSONファイルに保存
            scraper.save_to_json(videos, 'actress_videos.json')
            
            print(f"\n✅ 処理完了!")
        else:
            print(f"\n⚠️  収集されたデータがありません")
            
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
