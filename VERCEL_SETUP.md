# Vercelデプロイ設定ガイド

## エラー: "Could not access the repository" の対処法

### 1. GitHubリポジトリにコードがプッシュされているか確認

まず、GitHubリポジトリにコードがプッシュされているか確認してください：

1. ブラウザで https://github.com/toshibow123/adult-afi にアクセス
2. ファイルが表示されているか確認

### 2. リポジトリが空の場合

リポジトリが空の場合は、以下のコマンドでコードをプッシュしてください：

```bash
cd /Users/takahashitoshifumi/Desktop/Adult-affi

# Gitリポジトリを初期化（まだの場合）
git init

# すべてのファイルをステージング
git add .

# 初回コミット
git commit -m "Initial commit: 過去作・旧作大好きブログ"

# メインブランチに名前を変更
git branch -M main

# リモートリポジトリを追加
git remote add origin https://github.com/toshibow123/adult-afi.git

# GitHubにプッシュ
git push -u origin main
```

### 3. プライベートリポジトリの場合

プライベートリポジトリを使用している場合、Vercelがアクセスできるようにする必要があります：

1. **GitHubでPersonal Access Tokenを作成**
   - GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - "Generate new token" をクリック
   - スコープ: `repo` にチェック
   - トークンをコピー

2. **VercelでGitHubアカウントを接続**
   - Vercelの設定 → Git → GitHub
   - GitHubアカウントを接続（必要に応じてPersonal Access Tokenを使用）

### 4. Vercelでのプロジェクト作成手順

1. **Vercelにログイン**
   - https://vercel.com にアクセス
   - GitHubアカウントでログイン

2. **New Projectをクリック**

3. **GitHubリポジトリを選択**
   - `toshibow123/adult-afi` を選択
   - リポジトリが見つからない場合:
     - "Configure GitHub App" をクリック
     - リポジトリへのアクセス権限を付与

4. **プロジェクト設定**
   - **Framework Preset**: Next.js（自動検出されるはず）
   - **Root Directory**: `./`（そのまま）
   - **Build Command**: `npm run build`（デフォルト）
   - **Output Directory**: `.next`（デフォルト）
   - **Install Command**: `npm install`（デフォルト）

5. **環境変数の設定**
   - "Environment Variables" セクションで以下を追加：
     ```
     DMM_API_ID=your_api_id_here
     DMM_AFFILIATE_ID=your_affiliate_id_here
     GEMINI_API_KEY=your_gemini_api_key_here
     NEXT_PUBLIC_SITE_URL=https://your-app.vercel.app
     ```
   - カスタムドメイン使用時は、そのドメインを `NEXT_PUBLIC_SITE_URL` に設定

6. **Deployをクリック**

## トラブルシューティング

### リポジトリが見つからない場合

1. **GitHubアカウントの確認**
   - Vercelに接続しているGitHubアカウントが `toshibow123` か確認
   - 異なるアカウントの場合は、正しいアカウントでログイン

2. **リポジトリの権限確認**
   - GitHubでリポジトリの設定を確認
   - Settings → Collaborators でアクセス権限を確認

3. **GitHub Appの再認証**
   - Vercelの設定 → Git → GitHub
   - "Reinstall" または "Configure" をクリック
   - リポジトリへのアクセス権限を再付与

### ビルドエラーが出る場合

1. **環境変数の確認**
   - すべての環境変数が正しく設定されているか確認
   - `NEXT_PUBLIC_SITE_URL` が設定されているか確認

2. **ビルドログの確認**
   - Vercelのデプロイページでビルドログを確認
   - エラーメッセージを確認して対処

## 次のステップ

デプロイが成功したら：

1. **カスタムドメインの設定**（オプション）
   - Vercelのプロジェクト設定 → Domains
   - カスタムドメインを追加
   - DNS設定を案内に従って設定

2. **環境変数の更新**
   - カスタムドメイン使用時は `NEXT_PUBLIC_SITE_URL` を更新
   - 再デプロイを実行

3. **動作確認**
   - トップページが表示されるか確認
   - 記事詳細ページが表示されるか確認
   - 画像が正しく表示されるか確認
   - アフィリエイトリンクが動作するか確認

