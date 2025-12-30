# 熟女・人妻・ドラマ記事 自動生成ワークフロー

## 概要

「艶めく物語」サイト用に、DMM APIから熟女・人妻・ドラマ作品を取得し、官能小説のような記事を自動生成するワークフローです。

## 必要な環境変数

`.env`ファイルに以下を設定してください：

```bash
GEMINI_API_KEY=your_gemini_api_key
DMM_API_ID=your_dmm_api_id
DMM_AFFILIATE_ID=your_dmm_affiliate_id
```

## ワークフロー

### Step 1: ランキング取得

DMM APIから熟女・人妻・ドラマ作品のランキングを取得します。

```bash
cd /Users/takahashitoshifumi/Desktop/Mrs-Adult

# 全ジャンル（熟女・人妻・ドラマ）を取得（デフォルト）
python3 scripts/fetch_mature_drama_ranking.py

# 特定ジャンルのみ取得
python3 scripts/fetch_mature_drama_ranking.py --genre mature  # 熟女のみ
python3 scripts/fetch_mature_drama_ranking.py --genre married # 人妻のみ
python3 scripts/fetch_mature_drama_ranking.py --genre drama   # ドラマのみ

# 既存記事と重複を除外
python3 scripts/fetch_mature_drama_ranking.py --exclude-existing

# 取得件数を指定
python3 scripts/fetch_mature_drama_ranking.py --hits 100

# ソート順を指定（rank: ランキング順、date: 最新順、price: 価格順）
python3 scripts/fetch_mature_drama_ranking.py --sort date
```

**出力ファイル:**
- `data/mature_drama_all_latest.json` - 全ジャンル統合（最新）
- `data/mature_drama_mature_latest.json` - 熟女専用
- `data/mature_drama_married_latest.json` - 人妻専用
- `data/mature_drama_drama_latest.json` - ドラマ専用

### Step 2: 記事一括生成

取得したランキングから記事を生成します。

```bash
# 記事生成（対話形式）
python3 scripts/bulk_generate_mature_drama_articles.py
```

**対話内容:**
1. 何本の記事を生成するか？（デフォルト: 10本）
2. 開始日（YYYY-MM-DD、空白で今日）

**生成される記事:**
- ファイル名: `content/YYYY-MM-DD-{contentId}.md`
- 1日1本のペースで公開日を設定
- 官能小説のような雰囲気で執筆
- 品のある表現で女性読者も楽しめる内容

## 記事の特徴

### 執筆スタイル
- **トーン**: 官能小説 × 映画レビュー
- **表現**: 品のある言葉遣い、詩的な表現
- **焦点**: ストーリー性、演技力、大人の女性の色気

### 記事構成
1. 詩的なタイトル
2. 作品情報
3. 作品との出会い
4. 物語の魅力
5. 演技と演出の妙
6. 心に残るシーン（サンプル画像4-5枚）
7. この作品を観るあなたへ

### Frontmatter
```yaml
title: "作品タイトル"
date: "2025-12-30"
excerpt: "作品の魅力を簡潔に"
image: "パッケージ画像URL"
tags: ["熟女", "人妻", "ドラマ", "女優名", ...]
affiliateLink: "アフィリエイトURL"
contentId: "品番"
rating: 4.5
genre: ["熟女", "人妻", "ドラマ"]
storyScore: 4.5  # ストーリー評価
actingScore: 5.0 # 演技評価
atmosphereScore: 4.0 # 雰囲気評価
```

## ジャンル判定ロジック

以下のキーワードを含む作品のみを対象とします：

### 対象キーワード
- **熟女**: 熟女、三十路、四十路、五十路、還暦、おばさん
- **人妻**: 人妻、主婦、奥さん、妻、寝取られ
- **ドラマ**: ドラマ、ストーリー、近親相姦、不倫、NTR

### 除外キーワード
- 素人、ナンパ、マジックミラー、MM号、10代、ギャル

## 推奨ワークフロー

### 毎日の更新（1日1本）
```bash
# 1. ランキング取得（既存記事を除外）
python3 scripts/fetch_mature_drama_ranking.py --exclude-existing

# 2. 記事生成（1本）
python3 scripts/bulk_generate_mature_drama_articles.py
# → 生成本数: 1
# → 開始日: （空白で今日）

# 3. 開発サーバーで確認
npm run dev
```

### まとめて生成（初期コンテンツ作成）
```bash
# 1. ランキング取得（多めに）
python3 scripts/fetch_mature_drama_ranking.py --hits 100

# 2. 記事一括生成（50本）
python3 scripts/bulk_generate_mature_drama_articles.py
# → 生成本数: 50
# → 開始日: 2025-12-30（開始したい日付）

# 3. ビルドとデプロイ
npm run build
```

## トラブルシューティング

### エラー: ランキングファイルが見つかりません
```bash
# まずランキングを取得してください
python3 scripts/fetch_mature_drama_ranking.py
```

### エラー: 環境変数が設定されていません
```bash
# .envファイルを確認
cat .env

# または環境変数を直接設定
export GEMINI_API_KEY="your_key"
export DMM_API_ID="your_id"
export DMM_AFFILIATE_ID="your_affiliate_id"
```

### エラー: コンテンツがブロックされました
- Gemini APIのセーフティフィルターが働いています
- 数秒待ってから再実行してください
- それでもダメな場合は、該当作品をスキップして次へ

### レート制限対策
- 記事生成は各作品ごとに10秒待機します
- 大量生成（50本以上）の場合は複数回に分けることを推奨

## ディレクトリ構造

```
Mrs-Adult/
├── scripts/
│   ├── fetch_mature_drama_ranking.py        # ランキング取得
│   ├── bulk_generate_mature_drama_articles.py # 一括記事生成
│   └── generate_mature_drama_article.py      # 単体記事生成（URL指定）
├── data/
│   ├── mature_drama_all_latest.json          # 全ジャンル統合ランキング
│   ├── mature_drama_mature_latest.json       # 熟女ランキング
│   ├── mature_drama_married_latest.json      # 人妻ランキング
│   └── mature_drama_drama_latest.json        # ドラマランキング
├── content/
│   ├── 2025-12-30-contentid1.md
│   ├── 2025-12-31-contentid2.md
│   └── ...
└── docs/
    └── requirements.md                       # 要件定義書
```

## 参考

- 要件定義: `docs/requirements.md`
- 単体記事生成（URL指定）: `scripts/generate_mature_drama_article.py`
- デザイン実装: `tailwind.config.ts`, `app/globals.css`

## Tips

### 特定の女優の作品を取得したい場合
```bash
# DMM APIのキーワードを変更して直接取得
# fetch_mature_drama_ranking.pyのキーワードを編集
```

### 記事の文字数を増やしたい場合
- プロンプトの「最低2,500文字以上」を「最低3,500文字以上」に変更
- `bulk_generate_mature_drama_articles.py`の`create_article_prompt()`を編集

### 公開日を調整したい場合
```bash
# 記事生成時に開始日を指定
python3 scripts/bulk_generate_mature_drama_articles.py
# → 開始日: 2025-12-15（希望の日付）
```

---

**制作**: 2025-12-30
**対象サイト**: 艶めく物語（熟女・人妻・ドラマ専門ブログ）

