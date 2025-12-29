# Cloudflare Pages デプロイ設定

## 📋 ビルド設定

Cloudflare Pagesのダッシュボードで以下の設定を行ってください：

### Build settings

- **Build command**: `npm run build`
- **Build output directory**: `out`
- **Root directory**: `/` (プロジェクトルート)
- **Deploy command**: `echo "Deploying..."` ⚠️ 必須項目の場合

### ⚠️ 重要な注意点

**Deploy commandが必須項目の場合:**

Cloudflare Pagesでは、ビルドが成功すると自動的にデプロイされます。
デプロイコマンドは通常不要ですが、必須項目として設定されている場合は、以下のいずれかを設定してください：

1. **推奨**: `echo "Deploying..."` （何もしないコマンド）
2. **代替**: `npx wrangler pages deploy out` （手動デプロイ用、自動デプロイでは実行されない）

⚠️ **絶対に設定してはいけないコマンド:**
- `npx wrangler deploy` ❌ （Workers用のコマンドでエラーになる）

### エラーが発生した場合

ログに以下のようなエラーが表示される場合：

```
✘ [ERROR] It looks like you've run a Workers-specific command in a Pages project.
For Pages, please run `wrangler pages deploy` instead.
```

**解決方法:**
1. Cloudflareダッシュボードにログイン
2. 「Workers & Pages」→ プロジェクトを選択
3. 「Settings」→ 「Builds & deployments」
4. 「Deploy command」フィールドに `echo "Deploying..."` を設定
5. 「Save」をクリック
6. 再デプロイを実行

## 🔧 環境変数の設定

Cloudflare Pagesのダッシュボードで環境変数を設定：

1. 「Settings」→ 「Environment variables」
2. 以下の変数を追加：

```
DMM_API_ID=your_api_id_here
DMM_AFFILIATE_ID=your_affiliate_id_here
GEMINI_API_KEY=your_gemini_api_key_here
NEXT_PUBLIC_SITE_URL=https://your-pages-domain.pages.dev
```

⚠️ **注意**: `NEXT_PUBLIC_SITE_URL`は実際のCloudflare Pagesのドメインに設定してください。

## 📝 wrangler.toml

`wrangler.toml`は以下のように設定されています：

```toml
name = "adult-affi"
compatibility_date = "2025-12-28"
pages_build_output_dir = "out"
```

この設定は、Cloudflare Pagesが自動的に読み込みます。

## 🚀 デプロイ方法

### 方法1: GitHub連携による自動デプロイ（推奨）

1. GitHubにプッシュ
2. Cloudflare Pagesが自動的にビルドを開始
3. `npm run build`が実行される
4. `out`ディレクトリに静的ファイルが生成される
5. 自動的にデプロイされる

### 方法2: ローカルからWrangler CLIでデプロイ

#### Step 1: Wrangler CLIの認証

初回のみ、Cloudflareにログインする必要があります：

```bash
npx wrangler login
```

ブラウザが開き、Cloudflareアカウントでログインします。

#### Step 2: ビルドとデプロイ

以下のコマンドでビルドとデプロイを一括実行：

```bash
npm run deploy
```

または、個別に実行：

```bash
# 1. ビルド
npm run build

# 2. デプロイ
npx wrangler pages deploy out
```

#### Step 3: デプロイ確認

デプロイが成功すると、以下のようなメッセージが表示されます：

```
✨ Deployment complete! Take a sneak peek at your worker:
  https://adult-affi.pages.dev
```

⚠️ **注意**: 初回デプロイ時は、Cloudflare Pagesのダッシュボードでプロジェクトを作成する必要がある場合があります。

## 🔍 トラブルシューティング

### 「No build command specified」エラー

ログに以下のエラーが表示される場合：

```
No build command specified. Skipping build step.
Error: Output directory "out" not found.
```

**原因:**
Cloudflare Pagesのダッシュボードで「Build command」が設定されていません。

**解決方法:**
1. [Cloudflareダッシュボード](https://dash.cloudflare.com)にログイン
2. 「Workers & Pages」→ プロジェクト「adult-affi」を選択
3. 「Settings」タブをクリック
4. 「Builds & deployments」セクションを開く
5. 「Build command」フィールドに `npm run build` を入力
6. 「Build output directory」フィールドに `out` を入力
7. 「Save」をクリック
8. 自動的に再デプロイが開始されます

⚠️ **重要**: `wrangler.toml`にはビルドコマンドを書けません。必ずCloudflareダッシュボードで設定してください。

### ビルドは成功するがデプロイが失敗する

- 「Deploy command」が設定されていないか確認
- 設定されている場合は削除

### 環境変数が反映されない

- 環境変数の設定を確認
- `NEXT_PUBLIC_`プレフィックスが必要な変数は正しく設定されているか確認
- 環境変数を変更した場合は再デプロイが必要

### 画像が表示されない

- `next.config.js`の`remotePatterns`設定を確認
- 画像URLが正しいか確認

