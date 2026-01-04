import { Suspense } from 'react'
import { getAllActresses } from '@/lib/actresses'
import TopPageContent from '@/components/TopPageContent'

export const metadata = {
  title: '艶めく物語 | 女優一覧',
  description: '大人の女性の魅力を、女優ごとに深く掘り下げた作品カタログ。',
}

function TopPageContentWrapper() {
  // Server Componentでデータを取得（fsモジュールを使用）
  const actresses = getAllActresses()
  
  return <TopPageContent initialActresses={actresses} />
}

export default function Home() {
  return (
    <Suspense fallback={
      <div className="min-h-screen flex items-center justify-center" style={{ backgroundColor: 'var(--elegant-bg)', color: 'var(--elegant-text)' }}>
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 mx-auto mb-4" style={{ borderColor: 'var(--elegant-wine)' }}></div>
          <p style={{ color: 'var(--elegant-text-light)' }}>読み込み中...</p>
        </div>
      </div>
    }>
      <TopPageContentWrapper />
    </Suspense>
  )
}
