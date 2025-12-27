# DMM APIスクリプト

## 概要

このディレクトリには、DMM（FANZA）APIからアダルト動画のランキング情報を取得するPythonスクリプトが含まれています。

## スクリプト一覧

### fetch_dmm_ranking.py

アダルト動画のデイリーランキングTOP10を取得し、JSON形式で保存します。

**機能:**
- DMM API (FANZA) からデイリーランキングを取得
- TOP10の詳細情報（タイトル、URL、画像、価格、女優、ジャンルなど）を抽出
- JSON形式で保存（タイムスタンプ付き + 最新版）
- 環境変数から認証情報を読み込み

**使い方:**

```bash
# 環境変数を設定して実行
export DMM_API_ID="your_api_id"
export DMM_AFFILIATE_ID="your_affiliate_id"
python3 scripts/fetch_dmm_ranking.py

# または.envファイルを使用
export $(cat .env | xargs) && python3 scripts/fetch_dmm_ranking.py
```

**必要な環境変数:**
- `DMM_API_ID`: DMM APIのID
- `DMM_AFFILIATE_ID`: アフィリエイトID

**出力先:**
- `data/dmm_ranking_YYYYMMDD_HHMMSS.json` - 実行時のタイムスタンプ付き
- `data/dmm_ranking_latest.json` - 最新データ（常に上書き）

## 依存関係

Python 3.7以上が必要です。標準ライブラリのみを使用しているため、追加のパッケージインストールは不要です。

使用している標準ライブラリ:
- `os` - 環境変数の読み込み
- `json` - JSONの処理
- `urllib` - HTTP通信
- `datetime` - 日時処理

## エラー対応

### 環境変数が設定されていない
```
エラー: 環境変数 DMM_API_ID が設定されていません
```
→ 環境変数を正しく設定してください

### APIエラー
```
HTTPエラーが発生しました: 403 Forbidden
```
→ API IDまたはアフィリエイトIDが正しいか確認してください

### JSON出力エラー
```
ファイルの保存に失敗しました
```
→ `data/` ディレクトリへの書き込み権限を確認してください

## データの活用

取得したJSONデータは以下のような用途で活用できます:

1. **ブログ記事の自動生成** - ランキング情報をMarkdown記事に変換
2. **データ分析** - トレンド分析、人気ジャンルの調査
3. **アフィリエイトサイト** - 自動的に最新ランキングを表示
4. **定期実行** - cronやGitHub Actionsで自動取得

## 注意事項

- DMM APIの利用規約を遵守してください
- APIの呼び出し回数制限に注意してください
- アフィリエイトリンクの使用ルールを確認してください
- 取得したデータの二次利用については、DMM側の規約を確認してください

