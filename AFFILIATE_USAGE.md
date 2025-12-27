# アフィリエイト収益化ガイド

このドキュメントでは、アフィリエイト収益化のためのUI/UX機能の使い方を説明します。

## 1. サイドバー（Sidebar）

### 配置場所
- **PC表示**: 記事ページの右側に固定表示（Sticky）
- **モバイル表示**: 記事の下に配置

### 使用方法
`app/posts/[slug]/page.tsx`のサイドバーセクションに、バナー画像を配置してください。

```tsx
<a
  href="アフィリエイトURL"
  target="_blank"
  rel="noopener noreferrer"
  className="affiliate-card"
>
  <img
    src="バナー画像URL"
    alt="商品名"
  />
  <p className="text-center text-underground-yellow text-sm mt-2 hover:text-yellow-300 transition-colors">
    公式サイトで見る
  </p>
</a>
```

### 推奨サイズ
- **バナー画像**: 300x250px（レクタングルバナー）
- **その他**: 300x600px（スカイスクレイパー）も使用可能

## 2. 記事内アフィリエイト画像カード（Inline Ads）

### 使用方法
記事のMarkdown本文内に、以下のHTMLを直接記述してください：

```html
<a
  href="アフィリエイトURL"
  target="_blank"
  rel="noopener noreferrer"
  className="affiliate-card"
>
  <img
    src="商品画像URL"
    alt="商品名"
  />
  <span className="affiliate-link-text">公式サイトで見る</span>
</a>
```

### スタイル特徴
- **中央揃え**: 画像は自動的に中央に配置されます
- **影付き**: `box-shadow`でクリック可能な要素であることを強調
- **ホバー効果**: マウスオーバーで少し拡大し、ボーダーが黄色に変化
- **レスポンシブ**: モバイルでも適切に表示されます

### 使用例（Markdown内）

```markdown
## ここがエモい！演技と演出

古東まりこさんの演技力、これだけでご飯3杯いけるわ。

<a
  href="https://al.fanza.co.jp/?lurl=..."
  target="_blank"
  rel="noopener noreferrer"
  className="affiliate-card"
>
  <img
    src="https://pics.dmm.co.jp/digital/video/..."
    alt="商品名"
  />
  <span className="affiliate-link-text">公式サイトで見る</span>
</a>

特に師範が唸ったのは、**カラオケの個室で歌うフリをしながら...**
```

## 3. リンクの挙動

### 必須属性
すべてのアフィリエイトリンクには、以下の属性を必ず設定してください：

```html
target="_blank" rel="noopener noreferrer"
```

- **`target="_blank"`**: 新しいタブで開く
- **`rel="noopener noreferrer"`**: セキュリティ対策（新しいタブからの情報漏洩を防止）

### 自動設定
記事生成スクリプト（`scripts/process_gemini.py`）で生成されるリンクは、自動的にこれらの属性が設定されます。

## 4. ベストプラクティス

### アフィリエイトリンクの配置
1. **記事の冒頭**: 読者の興味が高いタイミング
2. **セクションの終わり**: 各セクションの内容を読んだ後
3. **記事の最後**: まとめの後

### 画像の選定
- **高品質な画像**: クリック率が向上します
- **適切なサイズ**: 読み込み速度を考慮
- **関連性**: 記事内容と関連する商品を推奨

### テキストリンク
- **明確なCTA**: 「公式サイトで見る」「詳細を確認する」など
- **視認性**: 黄色で目立つスタイルが適用されます

## 5. トラブルシューティング

### リンクが開かない
- `target="_blank"`が設定されているか確認
- ブラウザのポップアップブロックを確認

### 画像が表示されない
- 画像URLが正しいか確認
- `next.config.js`で外部ドメインが許可されているか確認

### スタイルが適用されない
- `className`属性が正しく設定されているか確認
- CSSファイルが正しく読み込まれているか確認

