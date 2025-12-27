import Link from 'next/link'
import { getAllPosts, getAllTags } from '@/lib/posts'
import YearSelect from '@/components/YearSelect'
import FanzaTvSidebarBanner from '@/components/FanzaTvSidebarBanner'
import PostTagButton from '@/components/PostTagButton'
// StarアイコンをSVGで実装（React 19互換性のため）
const Star = ({ className }: { className?: string }) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="currentColor"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    className={className}
  >
    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
  </svg>
)

interface HomeProps {
  searchParams: Promise<{ tag?: string; year?: string }>
}

// タグから年代を抽出
function extractYear(tags: string[] | undefined): string {
  if (!tags) return ''
  const yearTag = tags.find(tag => tag.includes('年'))
  return yearTag ? yearTag.replace('年', '') : ''
}

// 平均評価を計算（デフォルト値）
function getDefaultRating(): string {
  return '4.5'
}

export default async function Home({ searchParams }: HomeProps) {
  const allPosts = await getAllPosts()
  const tags = await getAllTags()
  const params = await searchParams
  
  // searchParamsの処理（Next.js 15+では自動デコードされる）
  const selectedTag = params.tag 
    ? String(params.tag).trim()
    : undefined
  const selectedYear = params.year
  
  // フィルタリング
  let posts = allPosts
  if (selectedTag) {
    posts = posts.filter((post) => {
      if (!post.tags || !Array.isArray(post.tags)) {
        return false
      }
      // タグを正規化して完全一致で比較
      return post.tags.some((tag) => {
        const tagStr = String(tag).trim()
        return tagStr === selectedTag
      })
    })
  }
  if (selectedYear) {
    posts = posts.filter((post) => {
      const year = extractYear(post.tags)
      return year === selectedYear
    })
  }

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
                埋もれた名作・旧作を発掘し、ビデオ黄金時代の熱量を再発見する
              </p>
            </div>

            {/* 年代プルダウン */}
            <div className="mb-8">
              <label htmlFor="year-select" className="block text-sm font-medium text-neutral-300 mb-2">
                年代で絞り込む
              </label>
              <YearSelect 
                years={years}
                selectedYear={selectedYear}
                selectedTag={selectedTag}
              />
            </div>

            {/* フィルタ表示 */}
            {(selectedTag || selectedYear) && (
              <div className="mb-6 flex items-center gap-3 flex-wrap">
                <span className="text-neutral-400 text-sm">フィルタ中:</span>
                {selectedTag && (
                  <span className="px-3 py-1 bg-neutral-900 border border-neutral-800 rounded-full text-sm">
                    {selectedTag}
                  </span>
                )}
                {selectedYear && (
                  <span className="px-3 py-1 bg-neutral-900 border border-neutral-800 rounded-full text-sm">
                    {selectedYear}年
                  </span>
                )}
                <Link 
                  href="/"
                  className="text-yellow-500 hover:text-yellow-400 text-sm underline"
                >
                  すべて表示
                </Link>
              </div>
            )}

            {/* 記事グリッド */}
            {posts.length === 0 ? (
              <div className="text-center py-16">
                <p className="text-neutral-400 text-lg">
                  {selectedTag || selectedYear ? '記事が見つかりませんでした' : 'まだ記事がありません'}
                </p>
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {posts.map((post) => {
                  const year = extractYear(post.tags)
                  const rating = getDefaultRating()
                  
                  return (
                    <Link
                      key={post.slug}
                      href={`/posts/${post.slug}`}
                      className="group bg-neutral-900 rounded-lg overflow-hidden border border-neutral-800 hover:border-yellow-500 transition-all hover:shadow-xl hover:shadow-yellow-500/10"
                    >
                      {/* 画像 */}
                      {post.image && (
                        <div className="aspect-[3/4] overflow-hidden bg-neutral-800">
                          <img
                            src={post.image}
                            alt={post.title}
                            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                          />
                        </div>
                      )}
                      
                      {/* メタ情報 */}
                      <div className="p-4">
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex items-center gap-1 text-yellow-500">
                            <Star className="w-4 h-4 fill-yellow-500" />
                            <span className="text-sm font-bold">{rating}</span>
                          </div>
                          {year && (
                            <span className="text-xs text-neutral-400 bg-neutral-800 px-2 py-1 rounded">
                              {year}年
                            </span>
                          )}
                        </div>
                        
                        <h3 className="text-sm font-semibold text-neutral-100 line-clamp-2 group-hover:text-yellow-500 transition-colors mb-2">
                          {post.title}
                        </h3>
                        
                        {/* タグボタン */}
                        {post.tags && post.tags.length > 0 && (
                          <div className="flex flex-wrap gap-1.5 mb-2">
                            {post.tags.slice(0, 3).map((tag: string) => (
                              <PostTagButton
                                key={String(tag).trim()}
                                tag={tag}
                                selectedTag={selectedTag}
                                selectedYear={selectedYear}
                              />
                            ))}
                            {post.tags.length > 3 && (
                              <span className="text-xs text-neutral-500 px-2 py-0.5">
                                +{post.tags.length - 3}
                              </span>
                            )}
                          </div>
                        )}
                        
                        {post.excerpt && (
                          <p className="text-xs text-neutral-400 mt-2 line-clamp-2">
                            {post.excerpt}
                          </p>
                        )}
                      </div>
                    </Link>
                  )
                })}
              </div>
            )}
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
                  <div className="flex flex-wrap gap-2">
                    {tags.map(({ tag, count }) => {
                      const isSelected = selectedTag === tag
                      return (
                        <Link
                          key={tag}
                          href={
                            isSelected
                              ? selectedYear ? `/?year=${selectedYear}` : '/'
                              : selectedYear
                              ? `/?tag=${encodeURIComponent(tag)}&year=${selectedYear}`
                              : `/?tag=${encodeURIComponent(tag)}`
                          }
                          className={`px-3 py-1.5 rounded-full text-sm transition-colors ${
                            isSelected
                              ? 'bg-yellow-600 text-neutral-950 font-semibold border border-yellow-500'
                              : 'bg-neutral-800 text-neutral-300 border border-neutral-700 hover:border-yellow-500 hover:text-yellow-500'
                          }`}
                        >
                          {tag} <span className={isSelected ? 'text-neutral-700' : 'text-neutral-500'}>({count})</span>
                        </Link>
                      )
                    })}
                  </div>
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
                  埋もれた名作・旧作を発掘し、再評価する。
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
                <p>© 2025 過去作・旧作大好きブログ. 埋もれた名作を再発見.</p>
                <p className="mt-2 text-xs">当サイトは18歳以上の方を対象としています。</p>
              </div>
        </div>
      </footer>
    </div>
  )
}
