# MGStage広告表示の実装方法

## 概要
Next.jsの静的サイト生成（SSG）環境で、古いMGStageアフィリエイトタグ（`document.write`を使用するもの）を安全に表示する方法です。

## 問題点
- 古いMGStageアフィリエイトタグは`document.write`を使用するため、Next.jsのSSR/SSG環境では直接実行できない
- `next/script`コンポーネントでも正常に動作しない場合がある
- 静的エクスポート（`output: 'export'`）では、動的なスクリプト読み込みが制限される

## 解決方法
iframeの`src`属性で静的HTMLファイルを読み込む方式を使用します。これにより、`document.write`を使用するスクリプトも安全に実行できます。

## 実装手順

### 1. 静的HTMLファイルの作成

`public/ads/`フォルダを作成し、その中に`mgs.html`というファイルを作成します。

**ファイルパス**: `public/ads/mgs.html`

**内容**:
```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { margin: 0; padding: 0; display: flex; justify-content: center; background: transparent; }
    </style>
</head>
<body>
    <script type="text/javascript" src="https://www.mgstage.com/afscript/superch/728_90/N2G56Q3UYEPYWXP7P8PKPRIDC3/"></script>
</body>
</html>
```

**注意点**:
- `src`属性のURLは、MGStageから提供された実際の広告スクリプトURLに置き換えてください
- `superch/728_90`の部分は、広告の種類やサイズによって異なります
- `N2G56Q3UYEPYWXP7P8PKPRIDC3`の部分は、あなたのアフィリエイトIDに置き換えてください

### 2. Reactコンポーネントの作成

**ファイルパス**: `components/MgsBanner.tsx`

**内容**:
```tsx
'use client'

export default function MgsBanner() {
  return (
    <div className="my-8">
      <div className="flex flex-col items-center gap-2 mb-2">
        <span className="text-xs text-elegant-text-dark font-medium bg-elegant-bg-lighter px-3 py-1 rounded-full border border-elegant-border">
          PR・アフィリエイト広告
        </span>
      </div>
      <div className="flex justify-center">
        <iframe
          src="/ads/mgs.html"
          width="728"
          height="90"
          frameBorder="0"
          scrolling="no"
          style={{
            border: 'none',
            overflow: 'hidden'
          }}
          title="MGStage Banner Ad"
        />
      </div>
    </div>
  )
}
```

**カスタマイズポイント**:
- `width`と`height`は、広告のサイズに合わせて調整してください（例: 300×60、728×90など）
- スタイリング（`className`や`style`）は、サイトのデザインに合わせて調整してください
- PR表示ラベルは、サイトのポリシーに合わせて調整または削除してください

### 3. コンポーネントの使用

記事ページや任意の場所で、`MgsBanner`コンポーネントをインポートして使用します。

**使用例**:
```tsx
import MgsBanner from '@/components/MgsBanner'

export default function ArticlePage() {
  return (
    <div>
      {/* 記事のタイトルやメタ情報 */}
      
      {/* 広告を配置 */}
      <MgsBanner />
      
      {/* 記事の本文 */}
    </div>
  )
}
```

## 複数の広告を配置する場合

異なる広告スクリプトを使用する場合は、以下の方法があります：

### 方法1: 複数のHTMLファイルを作成

`public/ads/`フォルダに複数のHTMLファイルを作成します：
- `mgs-top.html`（記事上部用）
- `mgs-bottom.html`（記事下部用）
- `mgs-sidebar.html`（サイドバー用）

各HTMLファイルに異なる広告スクリプトURLを設定します。

### 方法2: コンポーネントにpropsを追加

```tsx
'use client'

interface MgsBannerProps {
  htmlFile?: string
  width?: number
  height?: number
}

export default function MgsBanner({ 
  htmlFile = '/ads/mgs.html',
  width = 728,
  height = 90 
}: MgsBannerProps) {
  return (
    <div className="my-8">
      <div className="flex flex-col items-center gap-2 mb-2">
        <span className="text-xs text-elegant-text-dark font-medium bg-elegant-bg-lighter px-3 py-1 rounded-full border border-elegant-border">
          PR・アフィリエイト広告
        </span>
      </div>
      <div className="flex justify-center">
        <iframe
          src={htmlFile}
          width={width}
          height={height}
          frameBorder="0"
          scrolling="no"
          style={{
            border: 'none',
            overflow: 'hidden'
          }}
          title="MGStage Banner Ad"
        />
      </div>
    </div>
  )
}
```

使用例：
```tsx
<MgsBanner htmlFile="/ads/mgs-top.html" width={728} height={90} />
<MgsBanner htmlFile="/ads/mgs-bottom.html" width={300} height={250} />
```

## メリット

1. **安全性**: iframe内で実行されるため、メインサイトに影響を与えない
2. **互換性**: `document.write`を使用する古いスクリプトでも動作する
3. **静的エクスポート対応**: Next.jsの静的エクスポート（`output: 'export'`）でも正常に動作する
4. **シンプル**: 実装が簡単で、メンテナンスが容易

## 注意事項

1. **広告スクリプトURL**: MGStageから提供された正しい広告スクリプトURLを使用してください
2. **アフィリエイトID**: あなたのアフィリエイトIDに置き換えてください
3. **広告サイズ**: 広告の実際のサイズに合わせて`width`と`height`を調整してください
4. **PR表示**: アフィリエイト広告であることを明示するラベルを表示してください（法的要件）

## トラブルシューティング

### 広告が表示されない場合

1. **HTMLファイルのパスを確認**: `public/ads/mgs.html`が正しく配置されているか確認
2. **広告スクリプトURLを確認**: MGStageから提供されたURLが正しいか確認
3. **ブラウザのコンソールを確認**: エラーメッセージがないか確認
4. **広告ブロッカーを確認**: ブラウザの広告ブロッカーが有効になっていないか確認

### 広告のサイズが合わない場合

- `width`と`height`を広告の実際のサイズに合わせて調整
- レスポンシブ対応が必要な場合は、CSSで調整

## DMMアフィリエイト広告の実装方法

DMMアフィリエイト広告も、MGStageと同じiframe方式で実装できます。DMMには主に2つのタイプの広告があります：

### 1. DMMウィジェット広告（推奨）

DMMウィジェット広告は、記事内に自然に表示される広告です。

#### 静的HTMLファイルの作成

**ファイルパス**: `public/ads/dmm-widget.html`

**内容**:
```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { margin: 0; padding: 0; display: flex; justify-content: center; background: transparent; }
    </style>
</head>
<body>
    <ins class="dmm-widget-placement" data-id="YOUR_DATA_ID" style="background:transparent"></ins>
    <script src="https://widget-view.dmm.co.jp/js/placement.js" class="dmm-widget-scripts" data-id="YOUR_DATA_ID"></script>
</body>
</html>
```

**注意点**:
- `YOUR_DATA_ID`は、DMMアフィリエイト管理画面から取得した広告IDに置き換えてください
- 例: `43a8eba658580aad40df9b33383be12f`

#### Reactコンポーネントの作成

**ファイルパス**: `components/DmmWidget.tsx`

**内容**:
```tsx
'use client'

interface DmmWidgetProps {
  htmlFile?: string
  width?: number
  height?: number
}

export default function DmmWidget({ 
  htmlFile = '/ads/dmm-widget.html',
  width = 300,
  height = 250 
}: DmmWidgetProps) {
  return (
    <div className="my-8">
      <div className="flex flex-col items-center gap-2 mb-2">
        <span className="text-xs text-elegant-text-dark font-medium bg-elegant-bg-lighter px-3 py-1 rounded-full border border-elegant-border">
          PR・アフィリエイト広告
        </span>
      </div>
      <div className="flex justify-center">
        <iframe
          src={htmlFile}
          width={width}
          height={height}
          frameBorder="0"
          scrolling="no"
          style={{
            border: 'none',
            overflow: 'hidden'
          }}
          title="DMM Widget Ad"
        />
      </div>
    </div>
  )
}
```

### 2. DMMバナー広告

DMMバナー広告は、固定サイズのバナー広告です。

#### 静的HTMLファイルの作成

**ファイルパス**: `public/ads/dmm-banner.html`

**内容**:
```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { margin: 0; padding: 0; display: flex; justify-content: center; background: transparent; }
    </style>
</head>
<body>
    <ins class="widget-banner"></ins>
    <script class="widget-banner-script" src="https://widget-view.dmm.co.jp/js/banner_placement.js?affiliate_id=YOUR_AFFILIATE_ID&banner_id=YOUR_BANNER_ID"></script>
</body>
</html>
```

**注意点**:
- `YOUR_AFFILIATE_ID`は、あなたのDMMアフィリエイトIDに置き換えてください（例: `toshichan-002`）
- `YOUR_BANNER_ID`は、バナー広告のIDに置き換えてください（例: `1760_300_250`、`1298_300_250`）

#### Reactコンポーネントの作成

**ファイルパス**: `components/DmmBanner.tsx`

**内容**:
```tsx
'use client'

interface DmmBannerProps {
  htmlFile?: string
  width?: number
  height?: number
}

export default function DmmBanner({ 
  htmlFile = '/ads/dmm-banner.html',
  width = 300,
  height = 250 
}: DmmBannerProps) {
  return (
    <div className="my-8">
      <div className="flex flex-col items-center gap-2 mb-2">
        <span className="text-xs text-elegant-text-dark font-medium bg-elegant-bg-lighter px-3 py-1 rounded-full border border-elegant-border">
          PR・アフィリエイト広告
        </span>
      </div>
      <div className="flex justify-center">
        <iframe
          src={htmlFile}
          width={width}
          height={height}
          frameBorder="0"
          scrolling="no"
          style={{
            border: 'none',
            overflow: 'hidden'
          }}
          title="DMM Banner Ad"
        />
      </div>
    </div>
  )
}
```

### DMM広告の使用方法

```tsx
import DmmWidget from '@/components/DmmWidget'
import DmmBanner from '@/components/DmmBanner'

export default function ArticlePage() {
  return (
    <div>
      {/* 記事のタイトルやメタ情報 */}
      
      {/* DMMウィジェット広告を配置 */}
      <DmmWidget htmlFile="/ads/dmm-widget.html" width={300} height={250} />
      
      {/* 記事の本文 */}
      
      {/* DMMバナー広告を配置 */}
      <DmmBanner htmlFile="/ads/dmm-banner.html" width={300} height={250} />
    </div>
  )
}
```

### DMM広告の注意事項

1. **広告IDの取得**: DMMアフィリエイト管理画面から正しい広告IDを取得してください
2. **アフィリエイトID**: あなたのDMMアフィリエイトIDを正しく設定してください
3. **広告サイズ**: 広告の実際のサイズに合わせて`width`と`height`を調整してください
4. **複数の広告**: 異なる広告IDを使用する場合は、複数のHTMLファイルを作成してください

### DMM広告のトラブルシューティング

#### 広告が表示されない場合

1. **HTMLファイルのパスを確認**: `public/ads/dmm-widget.html`が正しく配置されているか確認
2. **広告IDを確認**: DMMアフィリエイト管理画面で取得したIDが正しいか確認
3. **ブラウザのコンソールを確認**: エラーメッセージがないか確認
4. **広告ブロッカーを確認**: ブラウザの広告ブロッカーが有効になっていないか確認

#### 広告のサイズが合わない場合

- `width`と`height`を広告の実際のサイズに合わせて調整
- DMMアフィリエイト管理画面で指定されているサイズを確認

## 参考

- MGStageアフィリエイト: https://www.mgstage.com/
- DMMアフィリエイト: https://affiliate.dmm.com/
- Next.js Static Export: https://nextjs.org/docs/app/building-your-application/deploying/static-exports

