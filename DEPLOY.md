# 本番環境デプロイ手順

## 📋 デプロイ前チェックリスト

### 1. 環境変数の設定

本番環境用の環境変数を設定してください。デプロイ先に応じて設定方法が異なります。

#### 必要な環境変数

```bash
# DMM API認証情報
DMM_API_ID=your_api_id_here
DMM_AFFILIATE_ID=your_affiliate_id_here

# Google Gemini API認証情報（記事生成スクリプト用）
GEMINI_API_KEY=your_gemini_api_key_here

# サイトURL（SEO用・必須）
NEXT_PUBLIC_SITE_URL=https://your-domain.com
```

⚠️ **重要**: `NEXT_PUBLIC_SITE_URL` は本番環境の実際のドメインに設定してください。
これが正しく設定されていないと、OGP画像やsitemap.xmlのURLが正しく生成されません。

### 2. ビルドテスト

ローカルでビルドが成功することを確認：

```bash
npm run build
```

ビルドが成功したら、ローカルで本番モードを起動して動作確認：

```bash
npm start
```

### 3. デプロイ先の選択

#### 推奨: Vercel（Next.js最適化）

**メリット:**
- Next.jsに最適化されている
- 自動デプロイ（GitHub連携）
- 無料プランで十分
- 環境変数の設定が簡単

**手順:**
1. [Vercel](https://vercel.com) にアカウント作成
2. GitHubリポジトリを連携
3. 環境変数を設定（上記の変数を全て設定）
4. デプロイ実行

**注意点:**
- `NEXT_PUBLIC_SITE_URL` は Vercel が自動で設定する `VERCEL_URL` を使用するか、カスタムドメインを設定
- カスタムドメイン使用時は `NEXT_PUBLIC_SITE_URL` にそのドメインを設定

#### その他の選択肢

- **Netlify**: Vercelと同様の機能
- **自社サーバー**: Node.js環境が必要、PM2等でプロセス管理

### 4. デプロイ後の確認事項

- [ ] トップページが正常に表示される
- [ ] 記事詳細ページが正常に表示される
- [ ] 画像が正しく表示される（DMM画像、商品画像）
- [ ] アフィリエイトリンクが正しく動作する
- [ ] DMM広告ウィジェットが表示される
- [ ] OGP画像が正しく生成される（SNSでシェアして確認）
- [ ] sitemap.xml がアクセス可能（`/sitemap.xml`）
- [ ] robots.txt がアクセス可能（`/robots.txt`）

### 5. SEO確認

以下のURLでメタデータが正しく設定されているか確認：

```bash
# 開発者ツールで確認
curl -I https://your-domain.com
curl -I https://your-domain.com/posts/記事のスラッグ
```

または、以下のツールで確認：
- [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)
- [Twitter Card Validator](https://cards-dev.twitter.com/validator)

## 🚀 Vercelデプロイ詳細手順

### Step 1: GitHubにプッシュ

```bash
git init  # まだの場合
git add .
git commit -m "Initial commit"
git remote add origin your-github-repo-url
git push -u origin main
```

### Step 2: Vercelでプロジェクト作成

1. Vercelにログイン
2. "New Project" をクリック
3. GitHubリポジトリを選択
4. プロジェクト設定：
   - Framework Preset: Next.js（自動検出）
   - Root Directory: `./`（そのまま）
   - Build Command: `npm run build`（デフォルト）
   - Output Directory: `.next`（デフォルト）

### Step 3: 環境変数の設定

Vercelのプロジェクト設定 > Environment Variables で以下を設定：

```
DMM_API_ID=your_api_id_here
DMM_AFFILIATE_ID=your_affiliate_id_here
GEMINI_API_KEY=your_gemini_api_key_here
NEXT_PUBLIC_SITE_URL=https://your-vercel-domain.vercel.app
```

カスタムドメイン使用時は、そのドメインを `NEXT_PUBLIC_SITE_URL` に設定。

### Step 4: デプロイ実行

"Deploy" ボタンをクリック。数分でデプロイが完了します。

### Step 5: カスタムドメイン設定（オプション）

1. Vercelプロジェクト設定 > Domains
2. カスタムドメインを追加
3. DNS設定を案内に従って設定
4. `NEXT_PUBLIC_SITE_URL` をカスタムドメインに更新して再デプロイ

## 📝 注意事項

### ファイルサイズ

- `public/images/` 内の画像ファイルが大きい場合、最適化を検討
- Next.jsの `next/image` を使用している箇所は自動最適化されます

### セキュリティ

- 環境変数は絶対にGitにコミットしない
- `.env` ファイルは `.gitignore` に含まれていることを確認

### パフォーマンス

- 静的生成（SSG）を使用しているため、初回ビルド後は高速
- 新しい記事を追加した場合は再ビルドが必要

## 🔧 トラブルシューティング

### ビルドエラー

```bash
# 依存関係を再インストール
rm -rf node_modules package-lock.json
npm install
npm run build
```

### 環境変数が反映されない

- `NEXT_PUBLIC_` プレフィックスが必要な変数は正しく設定されているか確認
- デプロイ後に環境変数を変更した場合は再デプロイが必要

### 画像が表示されない

- `next.config.js` の `remotePatterns` 設定を確認
- 画像URLが正しいか確認

## 📞 サポート

問題が発生した場合は、エラーログを確認して対処してください。

