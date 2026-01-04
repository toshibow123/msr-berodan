import AffiliateSidebar from '@/components/AffiliateSidebar'

export const metadata = {
  title: 'アフィリエイト広告テスト | 艶めく物語',
  description: 'アフィリエイト広告の表示テストページ',
}

export default function TestAdsPage() {
  return (
    <div className="min-h-screen" style={{ backgroundColor: 'var(--elegant-bg)', color: 'var(--elegant-text)' }}>
      {/* ヘッダー */}
      <header className="bg-gradient-to-b from-[var(--elegant-bg-light)] via-[var(--elegant-bg)] to-[var(--elegant-bg)] border-b-2 border-[var(--elegant-wine)]/30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 text-center">
          <h1 className="text-4xl font-bold font-serif tracking-wider mb-6" style={{ color: 'var(--elegant-wine)' }}>
            アフィリエイト広告テスト
          </h1>
          <p className="text-lg max-w-2xl mx-auto leading-relaxed" style={{ color: 'var(--elegant-text-light)' }}>
            iframe を使用したアフィリエイトバナーの表示テストページです。
          </p>
        </div>
      </header>

      {/* メインコンテンツ */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* メインコンテンツエリア */}
          <main className="flex-1">
            <div className="bg-[var(--elegant-bg-light)] rounded-xl p-8 border border-[var(--elegant-border)]">
              <h2 className="text-2xl font-serif font-bold text-[var(--elegant-wine)] mb-6">
                広告表示テスト
              </h2>
              
              <div className="space-y-6 text-[var(--elegant-text-light)]">
                <div>
                  <h3 className="text-lg font-semibold text-[var(--elegant-wine)] mb-3">実装内容</h3>
                  <ul className="space-y-2 list-disc list-inside">
                    <li><code className="bg-[var(--elegant-bg)] px-2 py-1 rounded text-sm">IframeAd</code> コンポーネントを使用</li>
                    <li><code className="bg-[var(--elegant-bg)] px-2 py-1 rounded text-sm">srcDoc</code> 属性で生のHTML/Scriptを実行</li>
                    <li>セキュリティを考慮した <code className="bg-[var(--elegant-bg)] px-2 py-1 rounded text-sm">sandbox</code> 属性を設定</li>
                    <li>Next.js の SSR/SSG と互換性のある実装</li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-lg font-semibold text-[var(--elegant-wine)] mb-3">表示される広告</h3>
                  <ul className="space-y-2 list-disc list-inside">
                    <li>FANZA バナー（ダミー）- 300x250px</li>
                    <li>MGS SuperCH 広告 - 300x250px</li>
                    <li>MGS 人妻広告 - 234x60px</li>
                    <li>サンプルバナー（ダミー）- 300x100px</li>
                  </ul>
                </div>

                <div className="bg-[var(--elegant-bg)] p-4 rounded-lg border border-[var(--elegant-border)]">
                  <h4 className="font-semibold text-[var(--elegant-wine)] mb-2">技術的なポイント</h4>
                  <p className="text-sm leading-relaxed">
                    従来の動的スクリプト読み込みではNext.jsのHydrationエラーが発生していましたが、
                    <code className="bg-[var(--elegant-bg-light)] px-1 rounded mx-1">iframe</code> + 
                    <code className="bg-[var(--elegant-bg-light)] px-1 rounded mx-1">srcDoc</code> 
                    を使用することで、アフィリエイトスクリプトを安全かつ確実に実行できるようになりました。
                  </p>
                </div>
              </div>
            </div>
          </main>

          {/* サイドバー（広告エリア） */}
          <AffiliateSidebar />
        </div>
      </div>

      {/* フッター */}
      <footer className="border-t mt-16 py-8" style={{ borderColor: 'var(--elegant-border)' }}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p style={{ color: 'var(--elegant-text-dark)' }} className="text-sm">
            アフィリエイト広告テストページ - iframe 実装版
          </p>
        </div>
      </footer>
    </div>
  )
}
