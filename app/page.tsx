import Link from 'next/link'
import { Suspense } from 'react'
import { getAllPosts, getAllTags } from '@/lib/posts'
import YearSelect from '@/components/YearSelect'
import FanzaTvSidebarBanner from '@/components/FanzaTvSidebarBanner'
import PostList from '@/components/PostList'
import TagList from '@/components/TagList'

// FireアイコンをSVGで実装
const Fire = ({ className }: { className?: string }) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="currentColor"
    stroke="currentColor"
    strokeWidth="0"
    className={className}
  >
    <path d="M12 2C11.5 6.5 9 8.5 9 11.5C9 13.5 10.5 15 12.5 15S16 13.5 16 11.5C16 9 14 8 13 4C13 4 13 6 12 6C11 6 11 4.5 12 2ZM5 13C5 13 6.5 10 8 9C8 9 7 10 7 11C7 11.5 7.5 12 8 12C9.5 12 11.5 11 12 8C12.5 11 14.5 12 16 12C17 12 17.5 11.5 17.5 11C17.5 10 16.5 9 16.5 9C18 10 19.5 13 19.5 13C19.5 17 16 20 12 20C8 20 5 17 5 13Z" />
  </svg>
)

// Sparklesアイコン
const Sparkles = ({ className }: { className?: string }) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    className={className}
  >
    <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" />
  </svg>
)

export default async function Home() {
  const allPosts = await getAllPosts()
  const tags = await getAllTags()

  // 年代リスト（2005年〜現在）
  const years = Array.from({ length: 2025 - 2005 + 1 }, (_, i) => 2005 + i).reverse()

  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-200">
      {/* ヘッダー */}
      <header className="border-b border-neutral-800 bg-neutral-900/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <Link href="/" className="text-2xl font-bold text-yellow-500 hover:text-yellow-400 transition-colors">
              過去作・旧作大好きブログ
            </Link>
            <nav className="flex gap-6">
              <Link href="/" className="text-neutral-400 hover:text-yellow-500 transition-colors">
                ホーム
              </Link>
              <Link href="/profile" className="text-neutral-400 hover:text-yellow-500 transition-colors">
                サイトについて
              </Link>
            </nav>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* メインコンテンツ */}
          <div className="flex-1 min-w-0">
            {/* タイトル */}
            <div className="mb-8">
              <h1 className="text-5xl font-bold text-neutral-100 mb-4">
                過去作・旧作大好きブログ
              </h1>
              <p className="text-neutral-400 text-lg">
                抜ける旧作・名作を発掘します
              </p>
            </div>

            {/* 年代で絞り込む */}
            <div className="mb-8">
              <h2 className="text-xl font-bold text-neutral-100 mb-4">年代・タグで絞り込む</h2>
              <Suspense fallback={<div className="px-4 py-2 bg-neutral-900 border border-neutral-800 rounded-lg text-neutral-400">読み込み中...</div>}>
                <YearSelect years={years} />
              </Suspense>
            </div>

            {/* 全記事リスト */}
            <div className="mb-8">
              <h2 className="text-2xl font-bold text-neutral-100 mb-6">すべての作品</h2>
              <Suspense fallback={<div className="text-center py-16 text-neutral-400">読み込み中...</div>}>
                <PostList allPosts={allPosts} />
              </Suspense>
            </div>
          </div>

          {/* サイドバー */}
          <aside className="lg:w-72 flex-shrink-0">
            <div className="lg:sticky lg:top-24 space-y-6">
              {/* タグ検索 */}
              <div className="bg-neutral-900 rounded-lg border border-neutral-800 p-6">
                <h2 className="text-xl font-bold text-neutral-100 mb-4">
                  タグで検索
                </h2>
                {tags.length === 0 ? (
                  <p className="text-neutral-400 text-sm">タグがありません</p>
                ) : (
                  <Suspense fallback={<div className="text-neutral-400 text-sm">読み込み中...</div>}>
                    <TagList tags={tags} />
                  </Suspense>
                )}
              </div>

              {/* FANZA TVバナー */}
              <FanzaTvSidebarBanner
                affiliateUrl="https://al.fanza.co.jp/?lurl=https%3A%2F%2Fpremium.dmm.co.jp%2Fbenefit%2F&af_id=toshichan-002&ch=link_tool&ch_id=text"
              />

              {/* サイト説明 */}
              <div className="bg-neutral-900 rounded-lg border border-neutral-800 p-6">
                <h2 className="text-lg font-bold text-neutral-100 mb-3">
                  このサイトについて
                </h2>
                <p className="text-neutral-400 text-sm leading-relaxed mb-4">
                  抜ける旧作・名作を発掘します。
                  現代の「綺麗すぎるだけのAV」に飽きた方へ。
                </p>
                <Link 
                  href="/profile"
                  className="text-yellow-500 hover:text-yellow-400 text-sm font-medium inline-flex items-center gap-1"
                >
                  <span>詳しく見る</span>
                  <span>→</span>
                </Link>
              </div>
            </div>
          </aside>
        </div>
      </main>

      {/* フッター */}
      <footer className="border-t border-neutral-800 bg-neutral-900/50 mt-20">
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="text-center text-neutral-400 text-sm">
            <p>© 2025 過去作・旧作大好きブログ. 抜ける旧作・名作を発掘します.</p>
            <p className="mt-2 text-xs">当サイトは18歳以上の方を対象としています。</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
