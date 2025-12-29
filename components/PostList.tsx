'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { useSearchParams } from 'next/navigation'
import PostTagButton from './PostTagButton'

// StarアイコンをSVGで実装
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

interface Post {
  slug: string
  title: string
  excerpt?: string
  image?: string
  tags?: string[]
  date?: string
  rating?: number
}

interface PostListProps {
  allPosts: Post[]
}

// タグから年代を抽出
function extractYear(tags: string[] | undefined): string {
  if (!tags) return ''
  const yearTag = tags.find(tag => tag.includes('年'))
  return yearTag ? yearTag.replace('年', '') : ''
}

// 評価を取得（記事のratingを使用、なければデフォルト値）
function getRating(post: Post): string {
  if (post.rating && typeof post.rating === 'number') {
    return post.rating.toFixed(1)
  }
  // デフォルト値（4.5）
  return '4.5'
}

export default function PostList({ allPosts }: PostListProps) {
  const searchParams = useSearchParams()
  const [selectedTag, setSelectedTag] = useState<string | undefined>(undefined)
  const [selectedYear, setSelectedYear] = useState<string | undefined>(undefined)
  const [showAllPosts, setShowAllPosts] = useState(false)

  useEffect(() => {
    const tag = searchParams.get('tag')
    const year = searchParams.get('year')
    setSelectedTag(tag ? tag.trim() : undefined)
    setSelectedYear(year || undefined)
  }, [searchParams])

  // フィルタリング
  let posts = allPosts
  if (selectedTag) {
    posts = posts.filter((post) => {
      if (!post.tags || !Array.isArray(post.tags)) {
        return false
      }
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

  // 最初の10個と残りを分ける
  const visiblePosts = posts.slice(0, 10)
  const hiddenPosts = posts.slice(10)
  const displayPosts = showAllPosts ? posts : visiblePosts

  return (
    <>
      {/* フィルタリング表示 */}
      {(selectedTag || selectedYear) && (
        <div className="mb-6 p-4 bg-neutral-900 rounded-lg border border-neutral-800">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-neutral-400 text-sm">フィルター:</span>
            {selectedTag && (
              <span className="px-3 py-1 bg-yellow-600 text-neutral-950 font-semibold rounded-full text-sm">
                {selectedTag}
              </span>
            )}
            {selectedYear && (
              <span className="px-3 py-1 bg-yellow-600 text-neutral-950 font-semibold rounded-full text-sm">
                {selectedYear}年
              </span>
            )}
            <Link
              href="/"
              className="ml-auto text-sm text-neutral-400 hover:text-yellow-500 transition-colors"
            >
              フィルターをクリア
            </Link>
          </div>
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
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {displayPosts.map((post) => {
            const year = extractYear(post.tags)
            const rating = getRating(post)
            
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
                          key={tag}
                          tag={tag}
                          selectedTag={selectedTag}
                          selectedYear={selectedYear}
                        />
                      ))}
                      {post.tags.length > 3 && (
                        <span className="px-2 py-0.5 rounded-full text-xs bg-neutral-800 text-neutral-400 border border-neutral-700">
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
          {hiddenPosts.length > 0 && (
            <div className="mt-8 text-center">
              <button
                onClick={() => setShowAllPosts(!showAllPosts)}
                className="px-6 py-3 bg-neutral-800 hover:bg-neutral-700 text-neutral-300 hover:text-yellow-500 border border-neutral-700 hover:border-yellow-500 rounded-lg transition-colors"
              >
                {showAllPosts ? '▲ 折りたたむ' : `▼ もっと見る (${hiddenPosts.length}件)`}
              </button>
            </div>
          )}
        </>
      )}
    </>
  )
}

