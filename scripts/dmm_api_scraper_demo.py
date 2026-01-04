#!/usr/bin/env python3
"""
DMM API スクレイパー（デモ版）

環境変数なしでテスト実行できるバージョン
実際のAPI呼び出しは行わず、サンプルデータで動作確認
"""

import json
import time
from typing import List, Dict, Set
from datetime import datetime

class DMMAPIScraperDemo:
    def __init__(self):
        """DMM API スクレイパー（デモ版）の初期化"""
        print("🎬 DMM API スクレイパー（デモ版）")
        print("=" * 60)
        print("⚠️  注意: これはデモ版です。実際のAPIは呼び出しません。")
        print("📋 サンプルデータで動作確認を行います。")
        print()
        
        self.collected_ids: Set[str] = set()
        
        # 検索対象キーワード（包含タグ）
        self.include_keywords = [
            'お母さん', '女将・女主人', '義母', '熟女', 
            '寝取り・寝取られ・NTR', '人妻・主婦', '未亡人', 
            'ママ友', '若妻・幼妻', '妊婦', 'ドラマ'
        ]
        
        # 除外キーワード
        self.exclude_keywords = ['ベスト・総集編', 'ベスト', '総集編']
        
        print(f"🚀 DMM API スクレイパー初期化完了")
        print(f"📋 検索キーワード: {', '.join(self.include_keywords[:3])}... (計{len(self.include_keywords)}個)")
        print(f"🚫 除外キーワード: {', '.join(self.exclude_keywords)}")

    def generate_sample_data(self, keyword: str, count: int = 10) -> List[Dict]:
        """
        サンプルデータを生成（実際のAPI呼び出しの代替）
        
        Args:
            keyword: 検索キーワード
            count: 生成するサンプル数
        
        Returns:
            サンプルビデオデータのリスト
        """
        sample_actresses = [
            '篠田ゆう', '川上ゆう（森野雫）', '風間ゆみ', '向井藍', 
            '夏目彩春', '水野優香', '水戸かな', '通野未帆', '神宮寺ナオ'
        ]
        
        sample_titles = [
            f'欲求不満の人妻が{keyword}に堕ちる物語',
            f'{keyword}の魅力に取り憑かれた美女たち',
            f'禁断の{keyword}体験 ～背徳の快楽～',
            f'{keyword}専門 高級エステサロン',
            f'秘密の{keyword}クラブ ～会員制倶楽部～'
        ]
        
        sample_data = []
        for i in range(count):
            actress = sample_actresses[i % len(sample_actresses)]
            title_template = sample_titles[i % len(sample_titles)]
            
            content_id = f"demo_{keyword}_{i:03d}"
            
            # 重複チェックは後で行う（is_valid_itemで処理）
                
            sample_data.append({
                'content_id': content_id,
                'title': title_template,
                'actress': actress,
                'actresses': [actress],
                'genres': [keyword, 'ドラマ', '単体作品'],
                'package_image': f'https://example.com/images/{content_id}_package.jpg',
                'sample_images': [
                    f'https://example.com/samples/{content_id}_01.jpg',
                    f'https://example.com/samples/{content_id}_02.jpg',
                    f'https://example.com/samples/{content_id}_03.jpg'
                ],
                'affiliate_url': f'https://example.com/affiliate/{content_id}',
                'date': f'2024-01-{(i % 30) + 1:02d}',
                'collected_at': datetime.now().isoformat()
            })
            
            # 注意: collected_idsへの追加はcollect_all_videosで行う
        
        return sample_data

    def is_valid_item(self, item: Dict) -> bool:
        """
        アイテムが取得条件を満たすかチェック（デモ版）
        
        Args:
            item: サンプルアイテムデータ
        
        Returns:
            有効な場合True
        """
        # 女優名の存在チェック
        actresses = item.get('actresses', [])
        if not actresses or len(actresses) == 0:
            return False
        
        # ジャンル情報の取得
        genres = item.get('genres', [])
        
        # 除外キーワードのチェック
        for exclude_keyword in self.exclude_keywords:
            if any(exclude_keyword in genre for genre in genres):
                print(f"🚫 除外: {item.get('title', 'Unknown')} (理由: {exclude_keyword})")
                return False
        
        return True

    def collect_all_videos(self, max_per_keyword: int = 50) -> List[Dict]:
        """
        全キーワードで動画データを収集（デモ版）
        
        Args:
            max_per_keyword: キーワードあたりの最大取得件数
        
        Returns:
            収集されたビデオデータのリスト
        """
        all_videos = []
        
        for keyword in self.include_keywords:
            print(f"\n🎯 キーワード '{keyword}' の検索開始")
            
            # デモ用の待機時間
            time.sleep(0.5)
            
            # サンプルデータの生成
            sample_items = self.generate_sample_data(keyword, min(max_per_keyword, 15))
            
            print(f"🔍 検索中: '{keyword}' (サンプル生成)")
            print(f"✅ 取得成功: {len(sample_items)}件 (デモデータ)")
            
            # アイテムの処理
            valid_items = 0
            for item in sample_items:
                content_id = item.get('content_id', '')
                
                # 重複チェック
                if content_id in self.collected_ids:
                    continue
                
                if self.is_valid_item(item):
                    all_videos.append(item)
                    self.collected_ids.add(content_id)
                    valid_items += 1
            
            print(f"📊 '{keyword}': {valid_items}件の有効なアイテムを追加 (累計: {len(all_videos)}件)")
        
        print(f"\n🎉 全検索完了! 総取得件数: {len(all_videos)}件")
        return all_videos

    def save_to_json(self, videos: List[Dict], filename: str = 'actress_videos_demo.json'):
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
                'demo_mode': True,
                'note': 'これはデモ版で生成されたサンプルデータです',
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
        
        print(f"\n📋 収集サマリー（デモ版）")
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
        print(f"\n👑 作品数上位女優 (TOP 5):")
        sorted_actresses = sorted(actress_count.items(), key=lambda x: x[1], reverse=True)
        for i, (actress, count) in enumerate(sorted_actresses[:5], 1):
            print(f"   {i:2d}. {actress}: {count}作品")
        
        # 上位ジャンル
        print(f"\n🏷️  人気ジャンル (TOP 5):")
        sorted_genres = sorted(genre_count.items(), key=lambda x: x[1], reverse=True)
        for i, (genre, count) in enumerate(sorted_genres[:5], 1):
            print(f"   {i:2d}. {genre}: {count}作品")
        
        # 最新作品
        print(f"\n🆕 最新作品 (TOP 3):")
        sorted_videos = sorted(videos, key=lambda x: x['date'], reverse=True)
        for i, video in enumerate(sorted_videos[:3], 1):
            print(f"   {i}. {video['title'][:40]}... ({video['actress']}) - {video['date']}")


def main():
    """メイン実行関数（デモ版）"""
    print("🎬 DMM API アダルト動画データ収集スクリプト（デモ版）")
    print("=" * 60)
    print("⚠️  これはデモ版です。実際のDMM APIは使用しません。")
    print("📋 サンプルデータで動作確認を行います。")
    print()
    
    try:
        # スクレイパーの初期化
        scraper = DMMAPIScraperDemo()
        
        # データ収集の実行
        print(f"\n🚀 データ収集開始...")
        videos = scraper.collect_all_videos(max_per_keyword=10)  # デモ用に少なめに設定
        
        if videos:
            # 結果の表示
            scraper.display_summary(videos)
            
            # JSONファイルに保存
            scraper.save_to_json(videos, 'actress_videos_demo.json')
            
            print(f"\n✅ デモ実行完了!")
            print(f"\n📋 次のステップ:")
            print(f"   1. 実際のDMM APIを使用する場合は .env ファイルを作成")
            print(f"   2. dmm_api_scraper.py を実行")
            print(f"   3. actress_videos_demo.json の内容を確認")
        else:
            print(f"\n⚠️  収集されたデータがありません")
            
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
