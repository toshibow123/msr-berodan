# 熟女・人妻・ドラマ作品 記事生成ガイド

「艶めく物語」サイト用の記事自動生成システムの使い方

## 🎯 概要

DMM APIから熟女・人妻・ドラマ作品のランキングを取得し、Gemini APIで官能小説のような雰囲気の記事を一括生成します。

## 📋 前提条件

### 必要な環境変数

`.env`ファイルに以下を設定してください：

```bash
DMM_API_ID=your_dmm_api_id
DMM_AFFILIATE_ID=your_affiliate_id
GEMINI_API_KEY=your_gemini_api_key
```

### 必要なPythonパッケージ

```bash
pip install google-generativeai python-dotenv
```

## 🚀 基本的な使い方

### Step 1: ランキングデータの取得

DMM APIから熟女・人妻・ドラマ作品のランキングを取得します。

```bash
# 全ジャンル取得（熟女・人妻・ドラマ）
python3 scripts/fetch_mature_drama_ranking.py --genre all --hits 50

# 特定ジャンルのみ取得
python3 scripts/fetch_mature_drama_ranking.py --genre mature --hits 30
python3 scripts/fetch_mature_drama_ranking.py --genre married --hits 30
python3 scripts/fetch_mature_drama_ranking.py --genre drama --hits 30

# 既存記事と重複しない作品のみ取得
python3 scripts/fetch_mature_drama_ranking.py --genre all --hits 50 --exclude-existing

# ソート順を指定
python3 scripts/fetch_mature_drama_ranking.py --genre all --hits 50 --sort date  # 最新順
python3 scripts/fetch_mature_drama_ranking.py --genre all --hits 50 --sort rank  # ランキング順（デフォルト）
```

**取得データの保存先:**
- `data/mature_drama_all_latest.json` - 全ジャンル統合（重複除去済み）
- `data/mature_drama_mature_latest.json` - 熟女作品のみ
- `data/mature_drama_married_latest.json` - 人妻作品のみ
- `data/mature_drama_drama_latest.json` - ドラマ作品のみ

### Step 2: 記事の一括生成

取得したランキングデータから記事を生成します。

```bash
python3 scripts/bulk_generate_mature_drama_articles.py
```

実行すると以下の入力が求められます：

1. **生成する記事数**: 何本の記事を生成するか（例: 10）
2. **開始日**: 記事の公開日の開始日（例: 2025-12-31、空白で今日）

**記事の保存先:**
- `content/YYYY-MM-DD-{content_id}.md`

**生成ルール:**
- 1日1本のペースで公開日が設定されます
- 既存記事（同じcontent_id）はスキップされます
- 熟女・人妻・ドラマに該当しない作品はスキップされます

### Step 3: 個別記事の生成（オプション）

特定の作品URLから個別に記事を生成することもできます。

```bash
python3 scripts/generate_mature_drama_article.py
```

実行すると以下の入力が求められます：

1. **作品URL**: FANZAの商品ページURL
2. **公開日**: 記事の公開日（空白で今日）

## 📊 ジャンル判定の仕組み

以下のキーワードを含む作品のみが対象になります：

### 対象ジャンル
- **熟女**: 熟女、三十路、四十路、五十路、還暦
- **人妻**: 人妻、主婦、奥さん、寝取られ
- **ドラマ**: ドラマ、ストーリー、近親相姦、不倫、NTR

### 除外ジャンル
- 素人、ナンパ、マジックミラー号
- 10代、ギャル
- 企画もの

## 🎨 記事の特徴

生成される記事は以下の特徴を持ちます：

### 文体
- 官能小説のような品のある表現
- 「ｗ」「マジで」「ヤバい」などのスラングは使用しない
- 映画レビューのようなストーリー分析
- 女性読者も楽しめる洗練された文章

### 構成
1. 詩的なタイトル
2. 作品情報（パッケージ画像、動画プレーヤー）
3. 作品との出会い
4. 物語の魅力
5. 演技と演出の妙
6. 心に残るシーン（サンプル画像付き）
7. 読者への語りかけ

### メタデータ
- `genre`: 該当するジャンル（熟女、人妻、ドラマ）
- `storyScore`: ストーリー評価（4.0-5.0）
- `actingScore`: 演技評価（4.0-5.0）
- `atmosphereScore`: 雰囲気評価（4.0-5.0）

## 📝 使用例

### 例1: 初回セットアップ（50本の記事を生成）

```bash
# Step 1: ランキング取得
python3 scripts/fetch_mature_drama_ranking.py --genre all --hits 50

# Step 2: 記事生成
python3 scripts/bulk_generate_mature_drama_articles.py
# 入力: 50
# 入力: 2025-12-31
```

### 例2: 既存記事を避けて追加記事を生成

```bash
# Step 1: 既存記事と重複しない作品を取得
python3 scripts/fetch_mature_drama_ranking.py --genre all --hits 30 --exclude-existing

# Step 2: 追加記事生成
python3 scripts/bulk_generate_mature_drama_articles.py
# 入力: 30
# 入力: 2026-01-31
```

### 例3: 特定ジャンルのみ

```bash
# 熟女作品のみ30本
python3 scripts/fetch_mature_drama_ranking.py --genre mature --hits 30
python3 scripts/bulk_generate_mature_drama_articles.py
# 入力: 30
# 入力: （空白 - 今日から）
```

## ⚠️ 注意事項

### API制限
- **Gemini API**: レート制限があるため、記事生成は10秒間隔で実行されます
- **DMM API**: 連続リクエストを避けるため、1秒間隔で実行されます

### 推奨設定
- 初回は10-20本程度から始めて、記事品質を確認してください
- 大量生成（50本以上）は時間がかかります（約1時間）
- 既存記事の除外機能を使うと、重複を避けられます

### トラブルシューティング

#### エラー: `環境変数が設定されていません`
→ `.env`ファイルを確認してください

#### エラー: `ランキングファイルが見つかりません`
→ まず`fetch_mature_drama_ranking.py`を実行してください

#### エラー: `記事生成に失敗（ブロックされました）`
→ Gemini APIのセーフティ設定により、一部の作品が生成できない場合があります。スキップされます。

## 📈 生成後の確認

記事生成後、以下を確認してください：

1. **記事ファイル**: `content/`フォルダに生成されているか
2. **画像リンク**: DMM画像URLが正しく表示されるか
3. **アフィリエイトリンク**: リンクが機能するか
4. **文章品質**: 官能小説的な雰囲気が出ているか

## 🔄 定期的な更新

週1回程度、新しいランキングを取得して記事を追加することをおすすめします：

```bash
# 月曜日の朝に実行
python3 scripts/fetch_mature_drama_ranking.py --genre all --hits 20 --exclude-existing
python3 scripts/bulk_generate_mature_drama_articles.py
# 入力: 10
# 入力: （次の公開開始日）
```

## 📚 関連ファイル

- `scripts/fetch_mature_drama_ranking.py` - ランキング取得スクリプト
- `scripts/bulk_generate_mature_drama_articles.py` - 一括記事生成スクリプト
- `scripts/generate_mature_drama_article.py` - 個別記事生成スクリプト
- `docs/requirements.md` - サイト要件定義書
- `data/mature_drama_all_latest.json` - 最新ランキングデータ
- `content/` - 生成された記事

---

## 💡 ヒント

- **記事の質を上げたい**: `generate_mature_drama_article.py`で個別に生成し、プロンプトを微調整
- **特定の女優の作品**: DMM APIのキーワード検索を使って、女優名で取得
- **過去の名作**: `--sort date`で最新順にして、古い作品も取得

Happy blogging! ✨

