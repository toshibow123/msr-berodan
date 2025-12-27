import type { Metadata } from 'next'
import { Noto_Sans_JP } from 'next/font/google'
import './globals.css'
import Link from 'next/link'

const notoSansJP = Noto_Sans_JP({ 
  subsets: ['latin'],
  weight: ['400', '500', '700'],
  variable: '--font-noto-sans-jp',
})

export const metadata: Metadata = {
  title: {
    default: '過去作・旧作大好きブログ | 埋もれた名作を再発見',
    template: '%s | 過去作・旧作大好きブログ',
  },
  description: 'ビデオ黄金時代を知る愛好家による、埋もれた名作・旧作AVの発掘と再評価。現代では作れない企画、女優の魂、生々しい映像美を再発見する。',
  keywords: ['旧作AV', '名作AV', '平成AV', 'ビデオ黄金時代', 'AVレビュー', '旧作発掘'],
  authors: [{ name: '過去作・旧作大好きブログ' }],
  openGraph: {
    type: 'website',
    locale: 'ja_JP',
    url: 'https://your-domain.com', // 実際のドメインに変更してください
    siteName: '過去作・旧作大好きブログ',
    title: '過去作・旧作大好きブログ | 埋もれた名作を再発見',
    description: 'ビデオ黄金時代を知る愛好家による、埋もれた名作・旧作AVの発掘と再評価。',
  },
  twitter: {
    card: 'summary_large_image',
    title: '過去作・旧作大好きブログ | 埋もれた名作を再発見',
    description: 'ビデオ黄金時代を知る愛好家による、埋もれた名作・旧作AVの発掘と再評価。',
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
      <body className={notoSansJP.variable}>
        <div className="min-h-screen flex flex-col bg-neutral-950">
          {children}
        </div>
      </body>
    </html>
  )
}

