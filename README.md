# 艶めく物語 - 熟女・人妻・ドラマ専門ブログ

> 大人の女性の魅力を、官能小説のように綴るレビューサイト

![Next.js](https://img.shields.io/badge/Next.js-14-black)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-3-38bdf8)
![Python](https://img.shields.io/badge/Python-3.11-3776ab)

## 🎨 コンセプト

熟女・人妻・ドラマ作品に特化した、官能小説のような雰囲気を持つアダルトコンテンツレビューブログ。

### 特徴
- **ラグジュアリーデザイン**: ワインレッド、ゴールド、アイボリーの上品な配色
- **官能小説的な文体**: 品のある表現で、うっとりするような読後感
- **女性も楽しめる**: 下品さを感じさせない、洗練されたUI
- **映画レビューのような視点**: ストーリー分析と演技評価を重視

## 🚀 クイックスタート

### 1. インストール

```bash
npm install
```

### 2. 環境変数の設定

`.env`ファイルを作成：

```bash
# DMM API
DMM_API_ID=your_dmm_api_id
DMM_AFFILIATE_ID=your_affiliate_id

# Gemini API
GEMINI_API_KEY=your_gemini_api_key

# Google Analytics
NEXT_PUBLIC_GA_ID=your_ga_id
```

### 3. Pythonパッケージのインストール

```bash
pip install -r requirements.txt
```

### 4. 開発サーバー起動

```bash
npm run dev
```

ブラウザで http://localhost:3000 を開く

## 📝 記事生成の流れ

### Step 1: ランキング取得

```bash
python3 scripts/fetch_mature_drama_ranking.py --genre all --hits 50
```

### Step 2: 記事生成

```bash
python3 scripts/bulk_generate_mature_drama_articles.py
```

詳細は [記事生成ガイド](scripts/MATURE_DRAMA_USAGE.md) を参照

## 🏗️ プロジェクト構成

```
Mrs-Adult/
├── app/                          # Next.js App Router
│   ├── layout.tsx               # サイト全体のレイアウト
│   ├── page.tsx                 # トップページ
│   ├── posts/[slug]/           # 記事詳細ページ
│   └── globals.css             # グローバルスタイル
│
├── components/                  # Reactコンポーネント
│   ├── ElegantPostCard.tsx     # 記事カード（ラグジュアリーデザイン）
│   ├── ElegantPostList.tsx     # 記事一覧
│   ├── CategoryFilter.tsx      # カテゴリーフィルター
│   └── ...                     # その他コンポーネント
│
├── content/                     # Markdown記事
│   └── YYYY-MM-DD-{id}.md     # 日付付き記事ファイル
│
├── scripts/                     # 記事生成スクリプト
│   ├── fetch_mature_drama_ranking.py          # ランキング取得
│   ├── bulk_generate_mature_drama_articles.py # 一括記事生成
│   ├── generate_mature_drama_article.py       # 個別記事生成
│   └── MATURE_DRAMA_USAGE.md                  # 使い方ガイド
│
├── data/                        # APIから取得したデータ
│   └── mature_drama_all_latest.json # 最新ランキング
│
├── docs/                        # ドキュメント
│   └── requirements.md         # 要件定義書
│
├── lib/                         # ユーティリティ
│   └── posts.ts                # 記事読み込みロジック
│
└── public/                      # 静的ファイル
    └── images/                 # 画像ファイル
```

## 🎯 対象ジャンル

以下のいずれかに該当する作品のみを扱います：

### ✅ 対象
- **熟女作品**: 30代以上の女優、大人の色気
- **人妻作品**: 人妻・主婦設定、背徳感
- **ドラマ作品**: ストーリー性の高い作品、NTR、不倫

### ❌ 除外
- 企画もの（ナンパ、マジックミラー号）
- ハード系（SM、スカトロ）
- 若い女優のみの単体作品（ドラマ性がない場合）

## 📊 記事の特徴

### 文体
```
❌ NG例（従来のスタイル）:
「マジでヤバいｗ」「抜けるわｗ」

✅ OK例（新スタイル）:
「この作品は、大人の女性の色気を存分に堪能できる一本です」
「彼女の演技は、見る者の心を静かに揺さぶります」
```

### 構成
1. **詩的なタイトル** - 心を揺さぶる、禁断の物語
2. **作品との出会い** - 官能小説のような語り出し
3. **物語の魅力** - 映画レビューのような分析
4. **演技と演出の妙** - 女優の演技力を評価
5. **心に残るシーン** - 官能的な描写（品のある範囲で）
6. **読者への語りかけ** - 余韻を残す締めくくり

## 🎨 デザインシステム

### カラーパレット

```css
/* メインカラー */
--elegant-wine: #8B2252;          /* 深みのあるワインレッド */
--elegant-wine-dark: #722F37;     /* ダークワインレッド */
--elegant-gold: #D4AF37;          /* ゴールド */
--elegant-champagne: #F0E68C;     /* シャンパンゴールド */

/* 背景 */
--elegant-ivory: #FFF8E7;         /* アイボリー */
--elegant-beige: #F5F5DC;         /* ベージュ */
--elegant-cream: #FFFEF0;         /* クリーム */

/* テキスト */
--elegant-charcoal: #2F2F2F;      /* チャコールグレー */
--elegant-brown: #3E2723;         /* 深い茶色 */
```

### タイポグラフィ

- **見出し**: Noto Serif JP（明朝体）- 優雅で読みやすい
- **本文**: Noto Sans JP（ゴシック体）- 可読性重視
- **行間**: 1.9〜2.0 - 余白を活かす
- **文字サイズ**: 17px以上 - 読みやすさ優先

## 🛠️ 技術スタック

### フロントエンド
- **Next.js 14** - React フレームワーク
- **TypeScript** - 型安全な開発
- **Tailwind CSS** - ユーティリティファーストCSS
- **React** - UIライブラリ

### バックエンド（記事生成）
- **Python 3.11+** - スクリプト言語
- **Gemini API** - AI記事生成
- **DMM API** - 作品情報取得
- **BeautifulSoup4** - Webスクレイピング

### デプロイ
- **Vercel** - 推奨デプロイ先
- **Cloudflare Pages** - 代替デプロイ先

## 📈 KPI・成功指標

### コンテンツKPI
- 記事数: 100本以上（3ヶ月）
- 平均文字数: 2,500文字以上
- 記事品質スコア: 4.0以上

### ユーザーKPI
- 平均滞在時間: 3分以上
- 直帰率: 60%以下
- ページ/セッション: 2.5以上

## 📚 ドキュメント

- [要件定義書](docs/requirements.md) - サイトの詳細仕様
- [記事生成ガイド](scripts/MATURE_DRAMA_USAGE.md) - スクリプトの使い方
- [デプロイガイド](DEPLOY.md) - 本番環境へのデプロイ方法

## 🔐 セキュリティ

- **18歳未満の閲覧制限** - 必須の明記
- **プライバシーポリシー** - 整備必須
- **利用規約** - 整備必須
- **DMM API利用規約** - 遵守

## 🤝 コントリビューション

このプロジェトはプライベートプロジェクトですが、改善提案は歓迎します。

## 📄 ライセンス

© 2025 艶めく物語. All rights reserved.

---

## 🎯 次のステップ

1. **記事生成**: [記事生成ガイド](scripts/MATURE_DRAMA_USAGE.md)を参照
2. **デザイン調整**: `tailwind.config.ts`でカラーを微調整
3. **SEO対策**: メタデータの最適化
4. **アクセス解析**: Google Analytics設定
5. **デプロイ**: Vercelへのデプロイ

---

**艶めく物語で、大人の女性の魅力を語りましょう ✨**
