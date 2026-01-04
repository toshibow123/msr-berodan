#!/bin/bash

# DMM API スクレイパー実行スクリプト

echo "🎬 DMM API データ収集・統合スクリプト"
echo "======================================"

# スクリプトのディレクトリに移動
cd "$(dirname "$0")"

# 環境変数ファイルの確認
if [ ! -f ".env" ]; then
    echo "❌ .env ファイルが見つかりません"
    echo "📋 env_sample.txt を参考に .env ファイルを作成してください"
    exit 1
fi

# Python環境の確認
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 が見つかりません"
    echo "📋 Python3 をインストールしてください"
    exit 1
fi

# 依存関係のインストール確認
echo "🔧 依存関係を確認中..."
pip3 install -r requirements.txt

# DMM API データ収集の実行
echo ""
echo "🚀 DMM API データ収集を開始..."
python3 dmm_api_scraper.py

# 収集結果の確認
if [ -f "actress_videos.json" ]; then
    echo ""
    echo "✅ データ収集完了"
    
    # ファイルサイズを表示
    file_size=$(du -h actress_videos.json | cut -f1)
    echo "📊 収集データサイズ: $file_size"
    
    # データ統合の実行確認
    echo ""
    read -p "🔗 既存データと統合しますか？ (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🔄 データ統合を開始..."
        python3 integrate_dmm_data.py
        
        if [ -f "../data/all_works_updated.json" ]; then
            echo ""
            echo "✅ データ統合完了"
            echo "📁 統合結果: ../data/all_works_updated.json"
            
            # 統合後のファイルサイズ
            updated_size=$(du -h ../data/all_works_updated.json | cut -f1)
            echo "📊 統合後データサイズ: $updated_size"
            
            echo ""
            echo "⚠️  注意: 統合結果を確認後、手動で all_works.json を更新してください"
            echo "   cp ../data/all_works_updated.json ../data/all_works.json"
        else
            echo "❌ データ統合に失敗しました"
        fi
    else
        echo "ℹ️  データ統合をスキップしました"
    fi
else
    echo "❌ データ収集に失敗しました"
    exit 1
fi

echo ""
echo "🎉 処理完了!"
echo ""
echo "📋 次のステップ:"
echo "   1. actress_videos.json の内容を確認"
echo "   2. 必要に応じて all_works.json を更新"
echo "   3. サイトを再ビルド: npm run build"
