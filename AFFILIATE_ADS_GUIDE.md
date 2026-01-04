# アフィリエイト広告表示ガイド

## 概要

Next.jsアプリケーションでMGSなどのアフィリエイト広告を確実に表示するための実装方法とトラブルシューティングガイドです。

## 🎯 成功した実装方式

### 基本原則
- **シンプルなiframe + 静的HTMLファイル方式**を採用
- 複雑なReactコンポーネントは使用しない
- 既存の成功実装を参考にする

## 📁 ファイル構成

```
public/ads/
├── fanza-300.html          # FANZA広告（300x250）
├── mgs-300.html            # MGS SuperCH（300x250）- 新規作成版
├── mgs-300x250.html        # MGS SuperCH（300x250）- 既存成功版 ⭐
├── mgs-728x90-1.html       # MGS 728x90（既存成功版）⭐
├── mgs-728x90-2.html       # MGS 728x90 バリエーション
├── mgs-728x90-3.html       # MGS 728x90 バリエーション
├── mgs-728x90-4.html       # MGS 728x90 バリエーション
├── mgs-hitotsuma.html      # MGS人妻（234x60）- 新規作成版
└── mgs.html                # MGS 728x90（既存成功版）⭐

components/
├── AffiliateSidebar.tsx    # 独立したアフィリエイト専用サイドバー
├── Sidebar.tsx             # メインページのサイドバー（広告含む）
├── MgsBanner.tsx           # 成功実装の参考コンポーネント ⭐
└── MgsAd728x90.tsx         # 成功実装の参考コンポーネント ⭐
```

## ✅ 成功した実装パターン

### 1. 静的HTMLファイル（推奨）

**ファイル例: `/public/ads/mgs-300x250.html`**
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
    <script type="text/javascript" src="https://www.mgstage.com/afscript/mgstvch/300_250/N2G56Q3UYEPYWXP7P8PKPRIDC3/"></script>
</body>
</html>
```

### 2. Reactコンポーネントでの読み込み

**基本パターン:**
```typescript
<iframe
  src="/ads/mgs-300x250.html"
  width={300}
  height={250}
  frameBorder="0"
  scrolling="no"
  style={{
    border: 'none',
    overflow: 'hidden'
  }}
  title="MGS SuperCH広告"
/>
```

**完全なコンポーネント例:**
```typescript
export default function MgsAd300x250() {
  return (
    <div className="bg-[var(--elegant-bg-light)] rounded-xl p-4 border border-[var(--elegant-border)] shadow-lg">
      {/* PR表示 */}
      <div className="text-center mb-3">
        <span className="text-xs text-[var(--elegant-text-dark)] font-medium bg-[var(--elegant-bg)] px-3 py-1 rounded-full border border-[var(--elegant-border)]">
          PR・MGS SuperCH
        </span>
      </div>
      
      {/* 広告iframe */}
      <div className="flex justify-center">
        <iframe
          src="/ads/mgs-300x250.html"
          width={300}
          height={250}
          frameBorder="0"
          scrolling="no"
          style={{
            border: 'none',
            overflow: 'hidden'
          }}
          title="MGS SuperCH広告"
        />
      </div>
    </div>
  )
}
```

## 🚫 失敗したパターン（避けるべき）

### 1. 複雑なReactコンポーネント
```typescript
// ❌ 動作しない
<IsolatedScriptAd 
  scriptSrc="https://www.mgstage.com/afscript/..."
  width={300}
  height={250}
  adName="MGS SuperCH"
  adType="superch"
/>

// ❌ フォールバックが表示される
<IframeAd 
  adCode='<script src="..."></script>'
  width={300}
  height={250}
/>
```

### 2. 動的スクリプト読み込み
```typescript
// ❌ Hydrationエラーが発生
useEffect(() => {
  const script = document.createElement('script')
  script.src = 'https://www.mgstage.com/afscript/...'
  document.body.appendChild(script)
}, [])
```

### 3. srcDocを使ったiframe
```typescript
// ❌ セキュリティ制限で動作しない
<iframe
  srcDoc='<script src="https://www.mgstage.com/afscript/..."></script>'
  width={300}
  height={250}
/>
```

## 🔧 トラブルシューティング

### 問題1: "Static Fallback"が表示される
**原因:** `IframeAd`コンポーネントのフォールバック機能が動作している
**解決策:** シンプルなiframe方式に変更

```typescript
// Before（問題）
<IframeAd adCode="..." width={300} height={250} />

// After（解決）
<iframe src="/ads/mgs-300x250.html" width={300} height={250} />
```

### 問題2: 広告が全く表示されない
**原因:** 複雑なReactコンポーネントやDOM操作エラー
**解決策:** 既存の成功実装を参考にする

**参考にすべきファイル:**
- `components/MgsBanner.tsx`
- `components/MgsAd728x90.tsx`
- `public/ads/mgs-300x250.html`
- `public/ads/mgs-728x90-1.html`

### 問題3: Next.js Hydrationエラー
**原因:** クライアントサイドでの動的スクリプト読み込み
**解決策:** 静的HTMLファイル + iframe方式

## 📋 実装チェックリスト

### ✅ 新しい広告を追加する場合

1. **HTMLファイルを作成**
   ```bash
   # public/ads/ フォルダに新しいHTMLファイルを作成
   touch public/ads/new-ad.html
   ```

2. **HTMLファイルの内容**
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
       <script type="text/javascript" src="アフィリエイトスクリプトURL"></script>
   </body>
   </html>
   ```

3. **Reactコンポーネントで読み込み**
   ```typescript
   <iframe
     src="/ads/new-ad.html"
     width={広告の幅}
     height={広告の高さ}
     frameBorder="0"
     scrolling="no"
     style={{ border: 'none', overflow: 'hidden' }}
     title="広告のタイトル"
   />
   ```

4. **テストページで確認**
   - `/test-ads` ページで表示確認
   - ブラウザの開発者ツールでエラーチェック

### ✅ 既存の広告を修正する場合

1. **既存のHTMLファイルを確認**
   ```bash
   ls public/ads/
   ```

2. **成功している実装を参考**
   - `mgs-300x250.html`（300x250サイズ）
   - `mgs-728x90-1.html`（728x90サイズ）

3. **コンポーネントのiframe部分を修正**
   ```typescript
   // src属性を正しいHTMLファイルに変更
   <iframe src="/ads/正しいファイル名.html" ... />
   ```

## 🎯 推奨される広告サイズ

| サイズ | 用途 | ファイル例 |
|--------|------|------------|
| 300x250 | サイドバー大 | `mgs-300x250.html` |
| 728x90 | ヘッダー・フッター | `mgs-728x90-1.html` |
| 234x60 | サイドバー小 | 728x90を縮小表示 |
| 300x100 | カスタムサイズ | 独自作成 |

## 🔍 デバッグ方法

### 1. HTMLファイルを直接確認
```bash
# ブラウザで直接HTMLファイルを開く
open http://localhost:3000/ads/mgs-300x250.html
```

### 2. ネットワークタブでスクリプト読み込み確認
- ブラウザの開発者ツール → Network タブ
- MGSスクリプトが正常に読み込まれているか確認

### 3. コンソールエラーチェック
- ブラウザの開発者ツール → Console タブ
- JavaScript エラーがないか確認

## 📚 参考実装

### 成功している既存コンポーネント

**`components/MgsBanner.tsx`**
```typescript
export default function MgsBanner() {
  return (
    <div className="my-8">
      <div className="flex justify-center">
        <iframe
          src="/ads/mgs.html"
          width="728"
          height="90"
          frameBorder="0"
          scrolling="no"
          style={{ border: 'none', overflow: 'hidden' }}
          title="MGStage Banner Ad"
        />
      </div>
    </div>
  )
}
```

**`components/MgsAd728x90.tsx`**
```typescript
export default function MgsAd728x90({ htmlFile = '/ads/mgs-728x90-1.html' }) {
  return (
    <div className="my-8">
      <div className="flex justify-center">
        <iframe
          src={htmlFile}
          width="728"
          height="90"
          frameBorder="0"
          scrolling="no"
          style={{ border: 'none', overflow: 'hidden' }}
          title="MGStage Ad 728x90"
        />
      </div>
    </div>
  )
}
```

## 🚀 今後の拡張

### 1. 新しいアフィリエイトパートナー追加
- 同じパターンでHTMLファイルを作成
- iframe方式で読み込み

### 2. A/Bテスト実装
- 複数のHTMLファイルを用意
- ランダムまたは条件に応じて切り替え

### 3. 広告ローテーション
- 時間やページビューに応じて広告を切り替え
- `useState`で管理

## 📝 まとめ

**成功の鍵:**
1. **シンプルなiframe + 静的HTMLファイル**
2. **既存の成功実装を参考にする**
3. **複雑なReactコンポーネントは避ける**
4. **段階的にテストしながら実装**

この方式により、Next.jsの制約を回避しつつ、確実にアフィリエイト広告を表示できます。
