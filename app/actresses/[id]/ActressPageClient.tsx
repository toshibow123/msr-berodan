'use client'

import { useState } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { type ActressData, type WorkData } from '@/lib/actresses'
import WorkFeedCard from '@/components/WorkFeedCard'
import InFeedAdCard from '@/components/InFeedAdCard'
import FanzaSubscriptionPromo from '@/components/FanzaSubscriptionPromo'
import VitalityPromoSection from '@/components/VitalityPromoSection'

interface ActressPageClientProps {
  actress: ActressData
  works: WorkData[]
}

const INITIAL_DISPLAY_COUNT = 5
const LOAD_MORE_COUNT = 5
const AD_INTERVAL = 4 // 4作品に1回広告を表示（3〜5作品の間）

/**
 * contentIdをaffiliateLinkから抽出（広告用）
 */
function extractContentId(affiliateLink: string): string | null {
  const cidMatch = affiliateLink.match(/[?&](?:cid|id)=([a-z0-9_]+)/i)
  if (cidMatch) {
    return cidMatch[1]
  }
  const mgsMatch = affiliateLink.match(/product_detail\/([A-Z0-9-]+)/i)
  if (mgsMatch) {
    return mgsMatch[1]
  }
  return null
}

/**
 * サンプル画像URLを生成
 */
function generateSampleImageUrls(imageUrl: string, contentId: string | null, count: number = 6): string[] {
  if (!contentId || !imageUrl) {
    return []
  }

  const urls: string[] = []
  
  // DMMのパターン
  if (imageUrl.includes('pics.dmm.co.jp')) {
    const baseUrl = imageUrl.replace(/\/[^/]+\.jpg$/, '')
    for (let i = 1; i <= count; i++) {
      urls.push(`${baseUrl}/${contentId}jp-${i}.jpg`)
    }
  }
  // MGSのパターン
  else if (imageUrl.includes('image.mgstage.com')) {
    const match = imageUrl.match(/https:\/\/image\.mgstage\.com\/images\/(.+?)\/(.+?)\/(.+?)\//)
    if (match) {
      const [, maker, series, idPart] = match
      const contentIdLower = contentId.toLowerCase()
      for (let i = 1; i <= count; i++) {
        urls.push(`https://image.mgstage.com/images/${maker}/${series}/${idPart}/cap_e_${i}_${contentIdLower}.jpg`)
      }
    }
  }
  
  return urls
}

export default function ActressPageClient({ actress, works }: ActressPageClientProps) {
  const [displayCount, setDisplayCount] = useState(INITIAL_DISPLAY_COUNT)
  const [selectedTag, setSelectedTag] = useState<string | null>(null)
  
  // 全作品からタグを抽出（重複除去）
  const allTags = [...new Set(works.flatMap(work => work.tags || []))].sort()
  
  // タグでフィルタリングされた作品リスト
  const filteredWorks = selectedTag 
    ? works.filter(work => work.tags?.includes(selectedTag))
    : works
  
  // タグが変更されたら表示数をリセット
  const handleTagChange = (tag: string | null) => {
    setSelectedTag(tag)
    setDisplayCount(INITIAL_DISPLAY_COUNT)
  }

  // 表示する作品（フィルタリング済み、最新順）
  const displayedWorks = filteredWorks.slice(0, displayCount)
  const hasMore = displayCount < filteredWorks.length
  const remainingCount = filteredWorks.length - displayCount

  const handleLoadMore = () => {
    setDisplayCount((prev) => Math.min(prev + LOAD_MORE_COUNT, filteredWorks.length))
  }

  // 広告を挿入するかどうかを判定
  const shouldShowAd = (index: number): boolean => {
    // 最初の作品の後は広告を表示しない
    if (index === 0) return false
    // AD_INTERVALごとに広告を表示（例: 4, 8, 12...）
    return (index + 1) % AD_INTERVAL === 0
  }

  // ヘッダー用のサンプル画像を生成（最新の3作品から）
  const headerSampleImages: string[] = []
  const topWorks = works.slice(0, 3) // 最新3作品
  topWorks.forEach((work) => {
    const contentId = extractContentId(work.affiliateLink)
    if (work.image && contentId) {
      const sampleUrls = generateSampleImageUrls(work.image, contentId, 2) // 各作品から2枚ずつ
      headerSampleImages.push(...sampleUrls)
    }
  })
  // 最大6枚まで
  const displayHeaderSamples = headerSampleImages.slice(0, 6)

  return (
    <div className="min-h-screen bg-elegant-bg text-elegant-text">
      {/* ヘッダー：女優プロフィール */}
      <header className="bg-gradient-to-b from-elegant-bg-light via-elegant-bg to-elegant-bg border-b-2 border-elegant-wine/30">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex flex-col md:flex-row items-center md:items-start gap-6">
                     {/* プロフィール画像 */}
                   {actress.image && (
                     <div className="relative w-40 h-40 md:w-56 md:h-56 rounded-full overflow-hidden border-4 border-elegant-wine/50 shadow-2xl flex-shrink-0">
                <Image
                  src={actress.image}
                  alt={actress.name}
                  fill
                  className="object-cover"
                  sizes="(max-width: 768px) 160px, 224px"
                />
              </div>
            )}

            {/* 女優情報 */}
            <div className="flex-1 text-center md:text-left">
              <h1 className="text-3xl md:text-4xl font-bold text-elegant-wine mb-2 font-serif">
                {actress.name}
              </h1>
              <p className="text-lg text-elegant-text-light mb-2">
                作品数: <span className="text-elegant-wine font-bold">{actress.works.length}件</span>
              </p>
              <p className="text-xs text-elegant-text-dark mb-3">
                下へスクロールして作品を閲覧
              </p>
              <Link
                href="/"
                className="inline-flex items-center gap-2 text-elegant-text-dark hover:text-elegant-wine transition-colors text-xs"
              >
                <span>←</span>
                <span>トップページに戻る</span>
              </Link>
            </div>
          </div>

          {/* サンプル画像（横スクロール） */}
          {displayHeaderSamples.length > 0 && (
            <div className="mt-6">
                     <h2 className="text-sm font-semibold text-elegant-wine mb-3 flex items-center gap-2">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  className="w-4 h-4"
                >
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                  <circle cx="8.5" cy="8.5" r="1.5" />
                  <polyline points="21 15 16 10 5 21" />
                </svg>
                サンプル画像
              </h2>
              <div className="overflow-x-auto scrollbar-hide -mx-4 px-4">
                <div className="flex gap-3" style={{ width: 'max-content' }}>
                  {displayHeaderSamples.map((url, index) => (
                    <div
                      key={index}
                             className="relative flex-shrink-0 rounded-lg overflow-hidden border border-elegant-wine/20 bg-elegant-bg-light"
                      style={{ width: '180px', height: '135px' }}
                    >
                      <Image
                        src={url}
                        alt={`${actress.name} サンプル ${index + 1}`}
                        fill
                        className="object-cover hover:scale-105 transition-transform duration-300"
                        sizes="180px"
                        onError={(e) => {
                          e.currentTarget.style.display = 'none'
                        }}
                      />
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </header>

      {/* メインコンテンツ：タイムライン（フィード型） */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* タグフィルター */}
        {allTags.length > 0 && (
          <div className="mb-8">
            <h2 className="text-sm font-semibold text-elegant-wine mb-4 flex items-center gap-2">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="w-4 h-4"
              >
                <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z" />
                <line x1="7" y1="7" x2="7.01" y2="7" />
              </svg>
              タグで絞り込み
            </h2>
            <div className="overflow-x-auto scrollbar-hide">
              <div className="flex gap-2 pb-2" style={{ width: 'max-content' }}>
                {/* 全て表示ボタン */}
                <button
                  onClick={() => handleTagChange(null)}
                  className={`
                    px-4 py-2 rounded-full text-sm font-medium transition-all duration-300 whitespace-nowrap
                    ${selectedTag === null
                      ? 'bg-elegant-wine text-white shadow-lg'
                      : 'bg-elegant-bg-light text-elegant-text-light border border-elegant-border hover:bg-elegant-bg-lighter hover:text-elegant-text'
                    }
                  `}
                >
                  全て表示 ({works.length})
                </button>
                
                {/* タグボタン */}
                {allTags.map((tag) => {
                  const tagCount = works.filter(work => work.tags?.includes(tag)).length
                  return (
                    <button
                      key={tag}
                      onClick={() => handleTagChange(tag)}
                      className={`
                        px-4 py-2 rounded-full text-sm font-medium transition-all duration-300 whitespace-nowrap
                        ${selectedTag === tag
                          ? 'bg-elegant-wine text-white shadow-lg'
                          : 'bg-elegant-bg-light text-elegant-text-light border border-elegant-border hover:bg-elegant-bg-lighter hover:text-elegant-text'
                        }
                      `}
                    >
                      {tag} ({tagCount})
                    </button>
                  )
                })}
              </div>
            </div>
          </div>
        )}

        {/* 作品フィード */}
        <div className="space-y-4">
          {displayedWorks.map((work, index) => {
            const contentId = extractContentId(work.affiliateLink)
            
            return (
              <div key={`${work.title}-${index}`}>
                {/* 作品カード */}
                <WorkFeedCard work={work} />
                
                {/* インフィード広告（条件付きレンダリング） */}
                {shouldShowAd(index) && (
                  <InFeedAdCard 
                    contentId={contentId || undefined}
                    affiliateLink={work.affiliateLink}
                  />
                )}
              </div>
            )
          })}
        </div>

        {/* Load More ボタン */}
        {hasMore && (
          <div className="mt-12 text-center">
                   <button
                     onClick={handleLoadMore}
                     className="px-8 py-4 bg-gradient-to-r from-elegant-bg-light to-elegant-bg-lighter hover:from-elegant-bg-lighter hover:to-elegant-bg text-white font-semibold rounded-xl transition-all shadow-lg hover:shadow-xl border border-elegant-wine/30 hover:border-elegant-wine/50"
                   >
                     次の{Math.min(LOAD_MORE_COUNT, remainingCount)}作品を表示
                     <span className="ml-2 text-elegant-wine">
                       ({remainingCount}件残り)
                     </span>
            </button>
          </div>
        )}

        {/* 全作品表示完了メッセージ */}
        {!hasMore && filteredWorks.length > 0 && (
          <div className="mt-12 text-center">
            <p className="text-elegant-text-dark text-sm">
              {selectedTag 
                ? `「${selectedTag}」タグの全${filteredWorks.length}作品を表示しました`
                : `全${filteredWorks.length}作品を表示しました`
              }
            </p>
          </div>
        )}

        {/* フィルタリング結果が0件の場合 */}
        {filteredWorks.length === 0 && selectedTag && (
          <div className="mt-12 text-center">
            <p className="text-elegant-text-dark text-lg mb-4">
              「{selectedTag}」タグの作品が見つかりませんでした
            </p>
            <button
              onClick={() => handleTagChange(null)}
              className="px-6 py-3 bg-elegant-wine hover:bg-elegant-wine-light text-white font-semibold rounded-lg transition-all"
            >
              全ての作品を表示
            </button>
          </div>
        )}

        {/* 一番下：FANZA TVボックス */}
        {!hasMore && (
          <div className="mt-16 mb-8">
            <FanzaSubscriptionPromo />
          </div>
        )}

        {/* 一番下：トップページへ戻るボタン */}
        {!hasMore && (
          <div className="mt-8 mb-12 text-center">
            <Link
              href="/"
              className="inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-gray-800 to-gray-900 hover:from-gray-700 hover:to-gray-800 text-white font-semibold rounded-xl transition-all shadow-lg hover:shadow-xl border border-amber-500/30 hover:border-amber-500/50"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="w-5 h-5"
              >
                <polyline points="18 15 12 9 6 15" />
              </svg>
              <span>トップページへ戻る</span>
            </Link>
          </div>
        )}

        {/* 固定：ページトップに戻るボタン（スクロール中も表示） */}
        <div className="fixed bottom-8 right-8 z-30">
                 <button
                   onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
                   className="w-12 h-12 bg-elegant-wine/90 hover:bg-elegant-wine text-white rounded-full flex items-center justify-center shadow-lg transition-all hover:scale-110"
                   aria-label="ページトップに戻る"
                 >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="w-6 h-6"
            >
              <polyline points="18 15 12 9 6 15" />
            </svg>
          </button>
        </div>

        {/* Vitality Promo Section */}
        <VitalityPromoSection />

        {/* TOPページへ戻るボタン */}
        <div className="flex justify-center py-12">
          <Link
            href="/"
            className="group flex items-center gap-3 bg-elegant-wine/90 hover:bg-elegant-wine text-white px-8 py-4 rounded-full font-semibold transition-all duration-300 hover:scale-105 hover:shadow-lg hover:shadow-elegant-wine/25"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="w-5 h-5 group-hover:-translate-x-1 transition-transform duration-300"
            >
              <path d="M19 12H5" />
              <polyline points="12 19 5 12 12 5" />
            </svg>
            <span>TOPページへ戻る</span>
          </Link>
        </div>
      </main>
    </div>
  )
}
