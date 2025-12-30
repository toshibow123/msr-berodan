import { Suspense } from 'react'
import { getAllPosts, getAllTags } from '@/lib/posts'
import ElegantPostList from '@/components/ElegantPostList'
import CategoryFilter from '@/components/CategoryFilter'
import Sidebar from '@/components/Sidebar'
import FilteredPostList from '@/components/FilteredPostList'


export default async function Home() {
  const allPosts = await getAllPosts()
  const allTags = await getAllTags()

  return (
    <>
      {/* ヒーローセクション */}
      <section className="bg-gradient-to-b from-elegant-bg-light to-elegant-bg py-16 border-b-2 border-elegant-gold/20">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <h2 className="text-5xl font-serif-jp text-elegant-wine mb-6 tracking-wider leading-relaxed">
            大人の女性の魅力を、<br className="md:hidden" />
            官能小説のように
          </h2>
          <p className="text-lg text-elegant-text-light leading-relaxed max-w-2xl mx-auto">
            熟女・人妻・ドラマ作品の魅力を、ストーリー性と演技力を重視した視点で綴ります。
            <br />
            品のある言葉で、心を揺さぶる物語をお届けします。
          </p>
        </div>
      </section>

      {/* カテゴリーフィルター */}
      <Suspense fallback={<div className="h-24 bg-elegant-bg-light animate-pulse"></div>}>
        <CategoryFilter />
      </Suspense>

      {/* メインコンテンツエリア（サイドバー + 記事一覧） */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* サイドバー */}
          <aside className="w-full lg:w-80 flex-shrink-0 order-2 lg:order-1">
            <Suspense fallback={<div className="h-96 bg-elegant-bg-light animate-pulse rounded-xl"></div>}>
              <Sidebar allPosts={allPosts} tags={allTags} />
            </Suspense>
          </aside>

          {/* 記事一覧 */}
          <main className="flex-1 min-w-0 order-1 lg:order-2">
            <Suspense fallback={
              <div className="text-center text-elegant-text-light">
                読み込み中...
              </div>
            }>
              <FilteredPostList allPosts={allPosts} />
            </Suspense>
          </main>
        </div>
      </div>
    </>
  )
}
