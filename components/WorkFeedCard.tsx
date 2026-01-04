'use client'

import { useState, useEffect, useRef } from 'react'
import Image from 'next/image'
import { WorkData } from '@/lib/actresses'

interface WorkFeedCardProps {
  work: WorkData
}

/**
 * contentIdをaffiliateLinkから抽出
 */
function extractContentId(affiliateLink: string): string | null {
  if (!affiliateLink) return null
  
  // DMMのURLパターン1: lurl内のid=xxx (エンコードされたURL内)
  // 例: https://al.fanza.co.jp/?lurl=https%3A%2F%2Fvideo.dmm.co.jp%2Fav%2Fcontent%2F%3Fid%3D1dandy00932
  const decodedUrl = decodeURIComponent(affiliateLink)
  const idMatch1 = decodedUrl.match(/[?&]id=([a-z0-9_-]+)/i)
  if (idMatch1) {
    return idMatch1[1]
  }
  
  // DMMのURLパターン2: cid=xxx または id=xxx (直接)
  const cidMatch = affiliateLink.match(/[?&](?:cid|id)=([a-z0-9_-]+)/i)
  if (cidMatch) {
    return cidMatch[1]
  }
  
  // MGSのURLパターン: product_detail/XXX-XXX
  const mgsMatch = affiliateLink.match(/product_detail\/([A-Z0-9-]+)/i)
  if (mgsMatch) {
    return mgsMatch[1]
  }
  
  // image URLから直接抽出を試みる
  const imageMatch = affiliateLink.match(/pics\.dmm\.co\.jp\/digital\/video[^\/]*\/([^\/]+)\//)
  if (imageMatch) {
    return imageMatch[1]
  }
  
  return null
}

/**
 * サンプル画像URLを生成
 */
function generateSampleImageUrls(imageUrl: string, contentId: string | null, count: number = 5): string[] {
  if (!contentId || !imageUrl) {
    return []
  }

  const urls: string[] = []
  
  // DMMのパターン
  if (imageUrl.includes('pics.dmm.co.jp')) {
    // メイン画像URLからベースURLを抽出
    // 例: https://pics.dmm.co.jp/digital/videoa/xxx/xxxpl.jpg
    // → https://pics.dmm.co.jp/digital/videoa/xxx
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

export default function WorkFeedCard({ work }: WorkFeedCardProps) {
  const [selectedImageIndex, setSelectedImageIndex] = useState<number | null>(null)
  const scrollContainerRef = useRef<HTMLDivElement>(null)

  // contentIdを抽出（affiliateLinkから、またはimage URLから）
  let contentId = extractContentId(work.affiliateLink || '')
  
  // affiliateLinkから抽出できなかった場合、image URLから抽出を試みる
  if (!contentId && work.image) {
    const imageMatch = work.image.match(/pics\.dmm\.co\.jp\/digital\/video[^\/]*\/([^\/]+)\//)
    if (imageMatch) {
      contentId = imageMatch[1]
    }
  }
  
  const sampleImageUrls = generateSampleImageUrls(work.image, contentId, 5) // 5枚に変更

  // videoUrlからcontentIdを抽出（DMM Lite Video用）
  const extractVideoContentId = (videoUrl: string | null): string | null => {
    if (!videoUrl) return null
    const match = videoUrl.match(/cid=([^/]+)/)
    return match ? match[1] : null
  }

  const videoContentId = extractVideoContentId(work.videoUrl)
  
  // あらすじを取得（description または comment）
  const synopsis = work.description || work.comment || null

  // モーダルを開く
  const openModal = (imageIndex: number) => {
    setSelectedImageIndex(imageIndex)
    document.body.style.overflow = 'hidden'
  }

  // モーダルを閉じる
  const closeModal = () => {
    setSelectedImageIndex(null)
    document.body.style.overflow = 'unset'
  }

  // 前の画像に移動
  const goToPrev = () => {
    if (selectedImageIndex === null) return
    const prevIndex = selectedImageIndex > 0 ? selectedImageIndex - 1 : sampleImageUrls.length - 1
    setSelectedImageIndex(prevIndex)
  }

  // 次の画像に移動
  const goToNext = () => {
    if (selectedImageIndex === null) return
    const nextIndex = selectedImageIndex < sampleImageUrls.length - 1 ? selectedImageIndex + 1 : 0
    setSelectedImageIndex(nextIndex)
  }

  // キーボード操作（ESC、左右矢印）
  useEffect(() => {
    if (selectedImageIndex === null) return

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        closeModal()
      } else if (e.key === 'ArrowLeft') {
        goToPrev()
      } else if (e.key === 'ArrowRight') {
        goToNext()
      }
    }

    window.addEventListener('keydown', handleKeyDown)

    return () => {
      window.removeEventListener('keydown', handleKeyDown)
    }
  }, [selectedImageIndex, sampleImageUrls.length])

  // サンプル画像のスクロール操作
  const scrollLeft = () => {
    if (scrollContainerRef.current) {
      scrollContainerRef.current.scrollBy({ left: -240, behavior: 'smooth' })
    }
  }

  const scrollRight = () => {
    if (scrollContainerRef.current) {
      scrollContainerRef.current.scrollBy({ left: 240, behavior: 'smooth' })
    }
  }

  return (
    <article className="bg-gradient-to-b from-elegant-bg-light to-elegant-bg rounded-2xl border border-elegant-wine/20 shadow-2xl mb-4" style={{ overflow: 'visible' }}>
      {/* ヘッダー */}
      <div className="px-3 py-2 border-b border-elegant-wine/20">
        <div className="flex flex-col gap-1">
          <div className="flex-1">
            <h3 className="text-lg md:text-xl font-bold text-white mb-0.5 leading-tight">
              {work.title}
            </h3>
            
            {/* あらすじ */}
            {synopsis && (
              <p className="text-xs md:text-sm text-gray-300 leading-relaxed line-clamp-2 mb-1.5">
                {synopsis}
              </p>
            )}
            
            <div className="flex flex-wrap items-center gap-2 text-xs text-gray-400">
              {work.date && (
                <time className="flex items-center gap-1">
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
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
                    <line x1="16" y1="2" x2="16" y2="6" />
                    <line x1="8" y1="2" x2="8" y2="6" />
                    <line x1="3" y1="10" x2="21" y2="10" />
                  </svg>
                  {new Date(work.date).toLocaleDateString('ja-JP', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                  })}
                </time>
              )}
                     {work.actress && (
                       <span className="flex items-center gap-1 text-elegant-wine">
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
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                    <circle cx="12" cy="7" r="4" />
                  </svg>
                  {work.actress}
                </span>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* タグ表示 */}
      {work.tags && work.tags.length > 0 && (
        <div className="px-3 py-2 border-b border-elegant-wine/20">
          <div className="flex items-center gap-2 mb-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="w-4 h-4 text-elegant-wine"
            >
              <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z" />
              <line x1="7" y1="7" x2="7.01" y2="7" />
            </svg>
            <span className="text-sm font-semibold text-elegant-wine">タグ</span>
          </div>
          <div className="flex flex-wrap gap-1.5">
            {work.tags.map((tag, index) => (
              <span 
                key={index} 
                className="px-3 py-1 rounded-full bg-gradient-to-r from-elegant-wine/20 to-elegant-wine/30 border border-elegant-wine/40 text-xs text-elegant-text-light whitespace-nowrap hover:from-elegant-wine/30 hover:to-elegant-wine/40 transition-all duration-200 shadow-sm"
              >
                #{tag}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* 1. 作品写真（パッケージ画像） */}
      {work.image && (
        <div className="w-full bg-black" style={{ margin: 0, padding: 0 }}>
          <a
            href={work.affiliateLink}
            target="_blank"
            rel="noopener noreferrer sponsored"
            className="block w-full hover:opacity-90 transition-all duration-300 relative group cursor-pointer"
            title={`${work.title} - 詳細を見る`}
          >
            <Image
              src={work.image}
              alt={work.title}
              width={800}
              height={1200}
              className="w-full h-auto block group-hover:scale-[1.02] transition-transform duration-300"
              style={{ width: '100%', height: 'auto', display: 'block', margin: 0, padding: 0 }}
              sizes="100vw"
              priority={false}
            />
            
            {/* クリック可能アイコン（ホバー時表示） */}
            <div className="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
              <div className="bg-elegant-wine/90 text-white px-4 py-2 rounded-full flex items-center gap-2 shadow-lg">
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
                  <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
                  <polyline points="15 3 21 3 21 9" />
                  <line x1="10" y1="14" x2="21" y2="3" />
                </svg>
                <span className="text-sm font-semibold">詳細を見る</span>
              </div>
            </div>
          </a>
        </div>
      )}

      {/* 2. 動画プレイヤー */}
      {work.videoUrl && videoContentId && (
        <div className="relative w-full bg-black" style={{ overflow: 'visible' }}>
          <div
            className="w-full relative"
            style={{
              paddingTop: '75%', // コントロールバーを含めた高さを確保
              overflow: 'visible',
            }}
          >
            <iframe
              width="100%"
              height="100%"
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                height: '100%',
                border: 'none',
              }}
              src={work.videoUrl}
              scrolling="no"
              frameBorder="0"
              allowFullScreen
              className="w-full h-full"
            />
          </div>
        </div>
      )}

      {/* 3. サンプル画像エリア（横スクロール） - 各作品ごとに5枚表示 */}
      {work.image && contentId && (
        <div className="px-3 py-3 bg-elegant-bg-light/50 border-t border-elegant-wine/20">
                 <h4 className="text-sm font-semibold text-elegant-wine mb-2 flex items-center gap-2">
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
            {work.title} - サンプル画像
          </h4>
          {sampleImageUrls.length > 0 ? (
            <div className="relative">
              {/* 左矢印ボタン */}
              <button
                onClick={scrollLeft}
                className="absolute left-0 top-1/2 -translate-y-1/2 z-10 bg-black/70 hover:bg-black/90 text-white p-2 rounded-full transition-all shadow-lg"
                aria-label="左にスクロール"
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
                  <polyline points="15 18 9 12 15 6" />
                </svg>
              </button>

              {/* 右矢印ボタン */}
              <button
                onClick={scrollRight}
                className="absolute right-0 top-1/2 -translate-y-1/2 z-10 bg-black/70 hover:bg-black/90 text-white p-2 rounded-full transition-all shadow-lg"
                aria-label="右にスクロール"
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
                  <polyline points="9 18 15 12 9 6" />
                </svg>
              </button>

              <div
                ref={scrollContainerRef}
                className="overflow-x-auto scrollbar-hide -mx-3 px-3"
              >
                <div className="flex gap-3" style={{ width: 'max-content' }}>
                  {sampleImageUrls.map((url, index) => (
                    <div
                      key={index}
                             className="relative flex-shrink-0 rounded-lg overflow-hidden border-2 border-elegant-wine/30 bg-elegant-bg-light shadow-lg hover:shadow-elegant-wine/20 transition-all cursor-pointer"
                      style={{ width: '220px', height: '165px' }}
                      onClick={() => openModal(index)}
                    >
                      <Image
                        src={url}
                        alt={`${work.title} サンプル ${index + 1}`}
                        fill
                        className="object-cover hover:scale-110 transition-transform duration-300"
                        sizes="220px"
                        onError={(e) => {
                          // 画像が存在しない場合は非表示
                          e.currentTarget.style.display = 'none'
                        }}
                      />
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <p className="text-xs text-gray-500 text-center py-2">
              サンプル画像を読み込み中...
            </p>
          )}
        </div>
      )}

      {/* アクション：CTAボタン */}
      {work.affiliateLink && (
               <div className="px-3 py-2 bg-gradient-to-r from-elegant-bg-light to-elegant-bg border-t border-elegant-wine/20 relative z-0">
          <a
            href={work.affiliateLink}
            target="_blank"
            rel="noopener noreferrer sponsored"
                   className="flex items-center justify-center gap-2 w-full bg-gradient-to-r from-elegant-wine via-elegant-wine-light to-elegant-wine hover:from-elegant-wine-dark hover:via-elegant-wine hover:to-elegant-wine-dark text-white font-bold text-sm md:text-base py-2.5 px-5 rounded-lg transition-all shadow-lg hover:shadow-2xl hover:scale-[1.02] active:scale-[0.98] relative z-0"
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
              <circle cx="12" cy="12" r="10" />
              <polygon points="10 8 16 12 10 16 10 8" />
            </svg>
            <span>DMMで公式サイトを見る</span>
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
              <line x1="7" y1="17" x2="17" y2="7" />
              <polyline points="7 7 17 7 17 17" />
            </svg>
          </a>
        </div>
      )}

      {/* モーダル（ライトボックス） */}
      {selectedImageIndex !== null && sampleImageUrls[selectedImageIndex] && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/90 backdrop-blur-sm"
          onClick={closeModal}
          style={{ cursor: 'pointer' }}
        >
          <div
            className="relative max-w-7xl max-h-[90vh] mx-4 w-full"
            onClick={(e) => e.stopPropagation()}
            style={{ cursor: 'default' }}
          >
            {/* 閉じるボタン */}
            <button
              onClick={closeModal}
              className="absolute -top-12 right-0 text-white hover:text-amber-400 transition-colors text-4xl font-bold z-10"
              aria-label="閉じる"
            >
              ×
            </button>

            {/* 前へボタン */}
            {sampleImageUrls.length > 1 && (
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  goToPrev()
                }}
                className="absolute left-4 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-black/70 text-white p-3 rounded-full transition-all z-10"
                aria-label="前の画像"
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
                  <polyline points="15 18 9 12 15 6" />
                </svg>
              </button>
            )}

            {/* 次へボタン */}
            {sampleImageUrls.length > 1 && (
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  goToNext()
                }}
                className="absolute right-4 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-black/70 text-white p-3 rounded-full transition-all z-10"
                aria-label="次の画像"
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
                  <polyline points="9 18 15 12 9 6" />
                </svg>
              </button>
            )}
            
            {/* 拡大画像（クリックで作品ページへ） */}
            {work.affiliateLink ? (
              <a
                href={work.affiliateLink}
                target="_blank"
                rel="noopener noreferrer sponsored"
                onClick={(e) => e.stopPropagation()}
                className="block"
              >
                <img
                  src={sampleImageUrls[selectedImageIndex]}
                  alt={`${work.title} サンプル ${selectedImageIndex + 1}`}
                  className="max-w-full max-h-[90vh] object-contain rounded-lg shadow-2xl mx-auto cursor-pointer hover:opacity-90 transition-opacity"
                />
              </a>
            ) : (
              <img
                src={sampleImageUrls[selectedImageIndex]}
                alt={`${work.title} サンプル ${selectedImageIndex + 1}`}
                className="max-w-full max-h-[90vh] object-contain rounded-lg shadow-2xl mx-auto"
              />
            )}

            {/* 画像カウンター */}
            {sampleImageUrls.length > 1 && (
              <div className="absolute bottom-4 left-1/2 -translate-x-1/2 bg-black/50 text-white px-4 py-2 rounded-full text-sm">
                {selectedImageIndex + 1} / {sampleImageUrls.length}
              </div>
            )}
          </div>
        </div>
      )}

      {/* 作品区切り線 */}
      <div className="mt-4 border-b-2 border-elegant-wine/30 mx-4"></div>
    </article>
  )
}
