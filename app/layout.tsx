import type { Metadata } from 'next'
import { Noto_Sans_JP, Noto_Serif_JP } from 'next/font/google'
import './globals.css'
import Link from 'next/link'

const notoSansJP = Noto_Sans_JP({ 
  subsets: ['latin'],
  weight: ['400', '500', '700'],
  variable: '--font-noto-sans-jp',
})

const notoSerifJP = Noto_Serif_JP({
  subsets: ['latin'],
  weight: ['400', '600', '700'],
  variable: '--font-noto-serif-jp',
})

export const metadata: Metadata = {
  title: {
    default: '艶めく物語 | 熟女・人妻・ドラマ作品の魅力を語る',
    template: '%s | 艶めく物語',
  },
  description: '大人の女性の色気と物語性に満ちた、熟女・人妻・ドラマ作品の魅力を、官能小説のような筆致で綴ります。ストーリー性と演技力を重視した、洗練されたレビューサイトです。',
  keywords: ['熟女', '人妻', 'ドラマ', '官能', 'レビュー', '大人の女性', 'ストーリー', '演技力', '映画評論'],
  authors: [{ name: '艶めく物語' }],
  openGraph: {
    type: 'website',
    locale: 'ja_JP',
    url: 'https://your-domain.com', // 実際のドメインに変更してください
    siteName: '艶めく物語',
    title: '艶めく物語 | 熟女・人妻・ドラマ作品の魅力を語る',
    description: '大人の女性の色気と物語性に満ちた作品の魅力を、官能小説のような筆致で綴ります。',
  },
  twitter: {
    card: 'summary_large_image',
    title: '艶めく物語 | 熟女・人妻・ドラマ作品の魅力を語る',
    description: '大人の女性の色気と物語性に満ちた作品の魅力を、官能小説のような筆致で綴ります。',
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ja">
      <head>
        {/* Google tag (gtag.js) */}
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-XZ34MB2TY4"></script>
        <script
          dangerouslySetInnerHTML={{
            __html: `
              window.dataLayer = window.dataLayer || [];
              function gtag(){dataLayer.push(arguments);}
              gtag('js', new Date());
              gtag('config', 'G-XZ34MB2TY4');
            `,
          }}
        />
      </head>
      <body className={`${notoSansJP.variable} ${notoSerifJP.variable}`}>
        <div className="min-h-screen flex flex-col bg-black">
          {/* ヘッダー */}
          <header className="bg-gradient-to-b from-gray-900 to-black border-b-2 border-amber-500/30 shadow-lg">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-8">
              <Link href="/" className="block">
                {/* ロゴ画像 */}
                <div className="flex flex-col items-center">
                  <img 
                    src="/images/products/unnamed11.jpg" 
                    alt="艶めく物語" 
                    className="max-w-md w-auto h-auto mx-auto shadow-xl border-2 border-amber-500/50"
                  />
                </div>
              </Link>
              
              {/* ナビゲーション */}
              <nav className="mt-6 flex flex-wrap justify-center gap-4 md:gap-8">
                <Link href="/" className="text-gray-300 hover:text-amber-400 transition-colors duration-300 font-medium text-sm md:text-base">
                  女優一覧
                </Link>
                <Link href="/tags" className="text-gray-300 hover:text-amber-400 transition-colors duration-300 font-medium text-sm md:text-base">
                  タグ一覧
                </Link>
              </nav>
            </div>
          </header>

          {/* メインコンテンツ */}
          <main className="flex-1">
          {children}
          </main>

          {/* フッター */}
          <footer className="bg-gradient-to-t from-gray-900 to-black border-t-2 border-amber-500/30 mt-16">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12 text-center">
              <p className="text-gray-400 text-sm mb-4">
                &copy; 2025 艶めく物語. All rights reserved.
              </p>
              <p className="text-gray-500 text-xs">
                このサイトは18歳未満の方の閲覧を禁止しています。
              </p>
            </div>
          </footer>
        </div>
      </body>
    </html>
  )
}

