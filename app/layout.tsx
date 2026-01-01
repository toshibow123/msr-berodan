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
        <div className="min-h-screen flex flex-col bg-elegant-bg">
          {/* ヘッダー */}
          <header className="bg-elegant-bg-light border-b-2 border-elegant-gold/30 shadow-lg">
            <div className="max-w-5xl mx-auto px-6 py-8">
              <Link href="/" className="block">
                {/* ロゴ画像 */}
                <div className="flex flex-col items-center">
                  <img 
                    src="/images/products/unnamed11.jpg" 
                    alt="艶めく物語" 
                    className="max-w-md w-auto h-auto mx-auto shadow-xl border-2 border-elegant-gold/50"
                  />
                </div>
              </Link>
              
              {/* ナビゲーション */}
              <nav className="mt-6 flex justify-center space-x-8">
                <Link href="/" className="text-elegant-text hover:text-elegant-wine transition-colors duration-300 font-medium">
                  最新記事
                </Link>
                <Link href="/category/mature" className="text-elegant-text hover:text-elegant-wine transition-colors duration-300 font-medium">
                  熟女
                </Link>
                <Link href="/category/married" className="text-elegant-text hover:text-elegant-wine transition-colors duration-300 font-medium">
                  人妻
                </Link>
                <Link href="/category/drama" className="text-elegant-text hover:text-elegant-wine transition-colors duration-300 font-medium">
                  ドラマ
                </Link>
              </nav>
            </div>
          </header>

          {/* メインコンテンツ */}
          <main className="flex-1">
          {children}
          </main>

          {/* フッター */}
          <footer className="bg-elegant-bg-light border-t-2 border-elegant-gold/30 mt-16">
            <div className="max-w-5xl mx-auto px-6 py-12 text-center">
              <p className="text-elegant-text-light text-sm mb-4">
                &copy; 2025 艶めく物語. All rights reserved.
              </p>
              <p className="text-elegant-text-dark text-xs">
                このサイトは18歳未満の方の閲覧を禁止しています。
              </p>
            </div>
          </footer>
        </div>
      </body>
    </html>
  )
}

