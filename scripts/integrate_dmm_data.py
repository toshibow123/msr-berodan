#!/usr/bin/env python3
"""
DMM APIで取得したデータを既存のall_works.jsonに統合するスクリプト

機能:
- actress_videos.json から既存の all_works.json 形式に変換
- 重複チェックと新規データの追加
- 女優名の正規化とマッピング
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Set

class DMMDataIntegrator:
    def __init__(self):
        """データ統合クラスの初期化"""
        self.existing_data_path = '../data/all_works.json'
        self.dmm_data_path = 'actress_videos.json'
        self.output_path = '../data/all_works_updated.json'
        
    def load_existing_data(self) -> List[Dict]:
        """既存のall_works.jsonを読み込み"""
        if not os.path.exists(self.existing_data_path):
            print(f"⚠️  既存データファイルが見つかりません: {self.existing_data_path}")
            return []
        
        try:
            with open(self.existing_data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"✅ 既存データ読み込み完了: {len(data)}件")
            return data
        except Exception as e:
            print(f"❌ 既存データ読み込みエラー: {e}")
            return []
    
    def load_dmm_data(self) -> List[Dict]:
        """DMM APIで取得したデータを読み込み"""
        if not os.path.exists(self.dmm_data_path):
            print(f"❌ DMM データファイルが見つかりません: {self.dmm_data_path}")
            return []
        
        try:
            with open(self.dmm_data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            videos = data.get('videos', [])
            print(f"✅ DMM データ読み込み完了: {len(videos)}件")
            return videos
        except Exception as e:
            print(f"❌ DMM データ読み込みエラー: {e}")
            return []
    
    def normalize_actress_name(self, name: str) -> str:
        """女優名の正規化"""
        # 基本的な正規化
        normalized = name.strip()
        
        # 全角・半角の統一
        normalized = normalized.replace('（', '(').replace('）', ')')
        
        return normalized
    
    def convert_dmm_to_works_format(self, dmm_videos: List[Dict]) -> List[Dict]:
        """DMM形式からall_works.json形式に変換"""
        converted_works = []
        
        for video in dmm_videos:
            # 基本情報の変換
            work = {
                'title': video.get('title', ''),
                'image': video.get('package_image', ''),
                'videoUrl': None,  # DMM APIからは動画URLは取得できない
                'actress': self.normalize_actress_name(video.get('actress', '')),
                'date': video.get('date', ''),
                'affiliateLink': video.get('affiliate_url', ''),
                'description': '',  # DMM APIからは詳細説明は取得できない
                'comment': '',
                'tags': video.get('genres', []),
                'source': 'dmm_api',  # データソースを明記
                'content_id': video.get('content_id', ''),
                'sample_images': video.get('sample_images', [])
            }
            
            converted_works.append(work)
        
        print(f"✅ DMM データ変換完了: {len(converted_works)}件")
        return converted_works
    
    def find_duplicates(self, existing_works: List[Dict], new_works: List[Dict]) -> Set[str]:
        """重複する作品を検出"""
        existing_titles = set()
        existing_content_ids = set()
        
        # 既存データからタイトルとcontent_idを抽出
        for work in existing_works:
            if work.get('title'):
                existing_titles.add(work['title'])
            if work.get('content_id'):
                existing_content_ids.add(work['content_id'])
        
        duplicates = set()
        
        # 新規データで重複をチェック
        for work in new_works:
            title = work.get('title', '')
            content_id = work.get('content_id', '')
            
            if title in existing_titles or content_id in existing_content_ids:
                duplicates.add(content_id or title)
        
        print(f"🔍 重複検出: {len(duplicates)}件")
        return duplicates
    
    def merge_data(self, existing_works: List[Dict], new_works: List[Dict]) -> List[Dict]:
        """データをマージ"""
        duplicates = self.find_duplicates(existing_works, new_works)
        
        # 重複を除いた新規データ
        unique_new_works = []
        for work in new_works:
            content_id = work.get('content_id', '')
            title = work.get('title', '')
            
            if content_id not in duplicates and title not in duplicates:
                unique_new_works.append(work)
        
        # 既存データと新規データをマージ
        merged_works = existing_works + unique_new_works
        
        # 日付順でソート（新しい順）
        merged_works.sort(key=lambda x: x.get('date', ''), reverse=True)
        
        print(f"✅ データマージ完了:")
        print(f"   - 既存データ: {len(existing_works)}件")
        print(f"   - 新規データ: {len(unique_new_works)}件")
        print(f"   - 重複除外: {len(duplicates)}件")
        print(f"   - 統合後: {len(merged_works)}件")
        
        return merged_works
    
    def save_merged_data(self, merged_works: List[Dict]):
        """統合されたデータを保存"""
        try:
            # バックアップの作成
            if os.path.exists(self.existing_data_path):
                backup_path = f"{self.existing_data_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                import shutil
                shutil.copy2(self.existing_data_path, backup_path)
                print(f"📋 バックアップ作成: {backup_path}")
            
            # 新しいデータを保存
            with open(self.output_path, 'w', encoding='utf-8') as f:
                json.dump(merged_works, f, ensure_ascii=False, indent=2)
            
            print(f"💾 統合データ保存完了: {self.output_path}")
            
            # 統計情報の表示
            self.display_statistics(merged_works)
            
        except Exception as e:
            print(f"❌ データ保存エラー: {e}")
    
    def display_statistics(self, works: List[Dict]):
        """統計情報を表示"""
        print(f"\n📊 統合後の統計情報")
        print(f"{'='*50}")
        
        # 女優別の作品数
        actress_count = {}
        source_count = {'dmm_api': 0, 'existing': 0}
        
        for work in works:
            actress = work.get('actress', '不明')
            actress_count[actress] = actress_count.get(actress, 0) + 1
            
            source = work.get('source', 'existing')
            source_count[source] = source_count.get(source, 0) + 1
        
        print(f"📈 総作品数: {len(works)}件")
        print(f"👥 女優数: {len(actress_count)}人")
        print(f"🆕 DMM API取得: {source_count.get('dmm_api', 0)}件")
        print(f"📚 既存データ: {source_count.get('existing', 0)}件")
        
        # 上位女優
        print(f"\n👑 作品数上位女優 (TOP 10):")
        sorted_actresses = sorted(actress_count.items(), key=lambda x: x[1], reverse=True)
        for i, (actress, count) in enumerate(sorted_actresses[:10], 1):
            print(f"   {i:2d}. {actress}: {count}作品")
    
    def integrate(self):
        """データ統合の実行"""
        print("🔄 DMM データ統合開始")
        print("=" * 50)
        
        # データの読み込み
        existing_works = self.load_existing_data()
        dmm_videos = self.load_dmm_data()
        
        if not dmm_videos:
            print("⚠️  統合するDMMデータがありません")
            return
        
        # DMM データの変換
        new_works = self.convert_dmm_to_works_format(dmm_videos)
        
        # データのマージ
        merged_works = self.merge_data(existing_works, new_works)
        
        # 統合データの保存
        self.save_merged_data(merged_works)
        
        print(f"\n✅ データ統合完了!")


def main():
    """メイン実行関数"""
    print("🔗 DMM API データ統合スクリプト")
    print("=" * 60)
    
    try:
        integrator = DMMDataIntegrator()
        integrator.integrate()
        
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
