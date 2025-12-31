'use client'

import { useEffect, useState, useRef } from 'react'
import Link from 'next/link'
import { PostData } from '@/lib/posts'

interface EditorialRecommendationsProps {
  currentPost: PostData
  allPosts: PostData[]
}

export default function EditorialRecommendations({
  currentPost,
  allPosts
}: EditorialRecommendationsProps) {
  const [isVisible, setIsVisible] = useState(false)
  const [shouldStick, setShouldStick] = useState(false)
  const containerRef = useRef<HTMLDivElement>(null)
  const footerRef = useRef<HTMLDivElement>(null)

  // ジャンル判定
  const getGenreType = (): 'hitozuma' | 'jukujyo' | null => {
    const genres = currentPost.genre || []
    const genreStr = genres.join(' ').toLowerCase()
    
    // 人妻判定
    if (genreStr.includes('人妻') || genreStr.includes('主婦') || genreStr.includes('奥さん')) {
      return 'hitozuma'
    }
    
    // 熟女判定
    if (genreStr.includes('熟女') || genreStr.includes('三十路') || genreStr.includes('四十路') || genreStr.includes('五十路')) {
      return 'jukujyo'
    }
    
    return null
  }

  // おすすめ記事を取得
  const getRecommendedPosts = (): PostData[] => {
    const genreType = getGenreType()
    const currentSlug = currentPost.slug
    
    // 現在の記事を除外
    let filtered = allPosts.filter(post => post.slug !== currentSlug)
    
    if (genreType === 'hitozuma') {
      // 人妻ジャンルでフィルタリング
      filtered = filtered.filter(post => {
        const genres = post.genre || []
        const genreStr = genres.join(' ').toLowerCase()
        return genreStr.includes('人妻') || genreStr.includes('主婦') || genreStr.includes('奥さん')
      })
    } else if (genreType === 'jukujyo') {
      // 熟女ジャンルでフィルタリング
      filtered = filtered.filter(post => {
        const genres = post.genre || []
        const genreStr = genres.join(' ').toLowerCase()
        return genreStr.includes('熟女') || genreStr.includes('三十路') || genreStr.includes('四十路') || genreStr.includes('五十路')
      })
    }
    
    // 評価順（rating）でソート、なければ日付順
    filtered.sort((a, b) => {
      const ratingA = a.rating || 0
      const ratingB = b.rating || 0
      if (ratingB !== ratingA) {
        return ratingB - ratingA
      }
      // 評価が同じ場合は日付順
      return new Date(b.date).getTime() - new Date(a.date).getTime()
    })
    
    return filtered.slice(0, 3)
  }

  const recommendedPosts = getRecommendedPosts()
  const genreType = getGenreType()
  
  // タイトルを決定
  const getTitle = (): string => {
    if (genreType === 'hitozuma') {
      return '人妻おすすめ3選'
    } else if (genreType === 'jukujyo') {
      return '熟女おすすめ3選'
    }
    return '今読まれているおすすめ'
  }

  // スクロール監視
  useEffect(() => {
    const handleScroll = () => {
      const scrollY = window.scrollY
      
      // 300px以上スクロールしたら表示
      if (scrollY > 300) {
        setIsVisible(true)
      } else {
        setIsVisible(false)
      }

      // フッター直前で追従解除
      if (footerRef.current && containerRef.current) {
        const footerTop = footerRef.current.getBoundingClientRect().top + window.scrollY
        const containerHeight = containerRef.current.offsetHeight
        const windowHeight = window.innerHeight
        const scrollBottom = scrollY + windowHeight
        
        // フッターが近づいたら追従解除
        if (scrollBottom >= footerTop - 100) {
          setShouldStick(false)
        } else {
          setShouldStick(true)
        }
      }
    }

    window.addEventListener('scroll', handleScroll)
    handleScroll() // 初回実行

    return () => {
      window.removeEventListener('scroll', handleScroll)
    }
  }, [])

  // フッター要素を探す
  useEffect(() => {
    const findFooter = () => {
      // 関連記事セクションを探す
      const relatedSection = document.querySelector('[data-related-posts]')
      if (relatedSection) {
        footerRef.current = relatedSection as HTMLDivElement
      }
    }

    // 初回実行
    findFooter()
    
    // 少し遅延して再試行（コンテンツが読み込まれるまで待つ）
    const timer1 = setTimeout(findFooter, 500)
    const timer2 = setTimeout(findFooter, 1000)
    
    return () => {
      clearTimeout(timer1)
      clearTimeout(timer2)
    }
  }, [currentPost.slug])

  if (recommendedPosts.length === 0) {
    return null
  }

  // 15文字以内のコピーを生成
  const getShortCopy = (post: PostData): string => {
    const title = post.title || ''
    if (title.length <= 15) {
      return title
    }
    return title.substring(0, 14) + '…'
  }

  return (
    <>
      <div
        ref={containerRef}
        className={`
          hidden lg:block
          w-80
          flex-shrink-0
          ${isVisible ? 'opacity-100' : 'opacity-0 pointer-events-none'}
          transition-opacity duration-300
          z-30
        `}
        style={{
          position: shouldStick && isVisible ? 'sticky' : 'relative',
          top: shouldStick && isVisible ? '6rem' : 'auto'
        }}
      >
        <div className="bg-elegant-bg-light rounded-xl p-6 border border-elegant-border shadow-lg">
          <h3 className="text-xl font-serif-jp text-elegant-wine mb-4 font-semibold">
            {getTitle()}
          </h3>
          
          <div className="space-y-4">
            {recommendedPosts.map((post, index) => (
              <Link
                key={post.slug}
                href={`/posts/${post.slug}`}
                className="block group hover:opacity-90 transition-opacity"
              >
                <div className="flex gap-3">
                  {/* サムネイル */}
                  {post.image && (
                    <div className="flex-shrink-0 w-24 h-24 rounded-lg overflow-hidden border border-elegant-border">
                      <img
                        src={post.image}
                        alt={post.title}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                      />
                    </div>
                  )}
                  
                  {/* テキスト部分 */}
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-elegant-text-light leading-relaxed mb-2 line-clamp-2">
                      {getShortCopy(post)}
                    </p>
                    {post.affiliateLink ? (
                      <span 
                        className="text-xs text-elegant-wine hover:text-elegant-wine-light underline decoration-elegant-wine/50 group-hover:decoration-elegant-wine transition-colors"
                        onClick={(e) => {
                          e.preventDefault()
                          e.stopPropagation()
                          window.open(post.affiliateLink, '_blank', 'noopener,noreferrer')
                        }}
                      >
                        詳細を見る →
                      </span>
                    ) : (
                      <span className="text-xs text-elegant-wine hover:text-elegant-wine-light underline decoration-elegant-wine/50 group-hover:decoration-elegant-wine transition-colors">
                        詳細を見る →
                      </span>
                    )}
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </>
  )
}

