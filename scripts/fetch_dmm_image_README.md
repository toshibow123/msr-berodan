# DMM商品画像取得スクリプト

DMM APIを使用して、検索キーワードから商品画像URLを自動取得するPythonスクリプトです。

## 機能

- キーワード検索（商品名、女優名など）
- 検索結果の1件目の大サイズ画像URLを取得
- エラーハンドリング完備

## セットアップ

### 1. API認証情報の取得

DMMアフィリエイトサイト（https://affiliate.dmm.com/）から以下を取得：

- **API ID**: DMM Webサービス利用登録後に発行されるID
- **アフィリエイトID**: アフィリエイト登録時に設定したID

### 2. 認証情報の設定方法

#### 方法1: 環境変数で設定（推奨）

`.env`ファイルに設定：

```bash
DMM_API_ID=your_api_id
DMM_AFFILIATE_ID=your_affiliate_id
```

実行時に読み込み：

```bash
export $(cat .env | grep -v '^#' | xargs) && python3 scripts/fetch_dmm_image.py キーワード
```

#### 方法2: スクリプト内で直接設定

`scripts/fetch_dmm_image.py`の冒頭を編集：

```python
API_ID = "your_actual_api_id"
AFFILIATE_ID = "your_actual_affiliate_id"
```

## 使い方

### 基本的な使い方

```bash
python3 scripts/fetch_dmm_image.py <検索キーワード>
```

### 使用例

```bash
# 女優名で検索
python3 scripts/fetch_dmm_image.py 河北彩花

# 商品名で検索
python3 scripts/fetch_dmm_image.py "キングオブエロ痴女優"

# 環境変数と組み合わせて実行
export $(cat .env | grep -v '^#' | xargs) && python3 scripts/fetch_dmm_image.py 神木麗
```

### 出力例

```
🔍 キーワード「河北彩花」で検索中...

✅ 画像URLを取得しました:
https://pics.dmm.co.jp/digital/video/ofje00512/ofje00512pl.jpg
```

## エラー処理

スクリプトは以下のエラーに対応しています：

- **商品が見つからない場合**: 警告メッセージを表示
- **API認証エラー**: エラーメッセージを表示
- **通信エラー**: ネットワークエラーを表示
- **JSONパースエラー**: データ構造エラーを表示

## 技術仕様

- **使用ライブラリ**: Python標準ライブラリのみ（`urllib`, `json`, `ssl`）
- **APIエンドポイント**: `https://api.dmm.com/affiliate/v3/ItemList`
- **取得画像サイズ**: `imageURL.large`（大サイズ）
- **検索対象**: FANZA動画（アダルト動画）

## 注意事項

- 無料枠のAPIにはレート制限があります
- 検索結果が0件の場合、空文字列が返されます
- SSL証明書の検証をスキップしています（macOS対応）

## トラブルシューティング

### 「API_IDが設定されていません」エラー

→ 環境変数またはスクリプト内でAPI_IDを設定してください

### 「商品が見つかりませんでした」警告

→ 検索キーワードを変更して再試行してください

### 「HTTPエラー 400」エラー

→ API IDまたはアフィリエイトIDが正しいか確認してください

