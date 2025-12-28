'use client'

import Link from 'next/link'
import { useState, useEffect } from 'react'

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

interface RelatedPostsProps {
  currentSlug: string
  currentTags?: string[]
  allPosts: Post[]
}

// タグから年代を抽出
function extractYear(tags: string[] | undefined): string {
  if (!tags) return ''
  const yearTag = tags.find(tag => tag.includes('年'))
  return yearTag ? yearTag.replace('年', '') : ''
}

export default function RelatedPosts({ currentSlug, currentTags, allPosts }: RelatedPostsProps) {
  const [relatedPosts, setRelatedPosts] = useState<Post[]>([])

  useEffect(() => {
    // 現在の記事を除外
    const otherPosts = allPosts.filter(post => post.slug !== currentSlug)
    
    // タグが一致する記事を抽出
    const related = otherPosts
      .map(post => {
        // 一致するタグの数を計算
        const matchCount = post.tags?.filter(tag => 
          currentTags?.includes(tag)
        ).length || 0
        
        return { post, matchCount }
      })
      .filter(item => item.matchCount > 0) // 1つ以上タグが一致
      .sort((a, b) => b.matchCount - a.matchCount) // 一致数で降順ソート
      .slice(0, 4) // 最大4件
      .map(item => item.post)
    
    // 関連記事が4件未満の場合、新着記事で補完
    if (related.length < 4) {
      const remaining = 4 - related.length
      const recentPosts = otherPosts
        .filter(post => !related.includes(post))
        .slice(0, remaining)
      
      setRelatedPosts([...related, ...recentPosts])
    } else {
      setRelatedPosts(related)
    }
  }, [currentSlug, currentTags, allPosts])

  if (relatedPosts.length === 0) {
    return null
  }

  return (
    <section className="mt-16 mb-8">
      <h2 className="text-2xl font-bold text-neutral-100 mb-6">
        あなたにおすすめの作品
      </h2>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {relatedPosts.map((post) => {
          const year = extractYear(post.tags)
          const rating = post.rating ? post.rating.toFixed(1) : '4.5'
          
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
              <div className="p-3">
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
                
                <h3 className="text-sm font-semibold text-neutral-100 line-clamp-2 group-hover:text-yellow-500 transition-colors">
                  {post.title}
                </h3>
              </div>
            </Link>
          )
        })}
      </div>
    </section>
  )
}

