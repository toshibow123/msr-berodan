'use client'

import { useState, useEffect } from 'react'

interface SampleGalleryProps {
  contentId?: string
  affiliateLink?: string
}

/**
 * FANZA作品のサンプル画像ギャラリーコンポーネント
 * 1-6枚目のサンプル画像をグリッド表示
 */
export default function SampleGallery({ 
  contentId = 'h_1380pre00009',
  affiliateLink 
}: SampleGalleryProps) {
  const [selectedImage, setSelectedImage] = useState<string | null>(null)

  // サンプル画像URLを生成（1-6枚目）
  const sampleImages = Array.from({ length: 6 }, (_, i) => {
    const imageNumber = i + 1
    return `https://pics.dmm.co.jp/digital/video/${contentId}/${contentId}jp-${imageNumber}.jpg`
  })

  const openModal = (imageUrl: string) => {
    setSelectedImage(imageUrl)
    // モーダル表示時にbodyのスクロールを無効化
    document.body.style.overflow = 'hidden'
  }

  const closeModal = () => {
    setSelectedImage(null)
    // モーダル閉じる時にbodyのスクロールを有効化
    document.body.style.overflow = 'unset'
  }

  // ESCキーでモーダルを閉じる
  useEffect(() => {
    if (!selectedImage) return

    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setSelectedImage(null)
        document.body.style.overflow = 'unset'
      }
    }

    window.addEventListener('keydown', handleEscape)

    return () => {
      window.removeEventListener('keydown', handleEscape)
    }
  }, [selectedImage])

  return (
    <>
      <section className="mt-12 mb-8">
        <h2 className="text-2xl font-bold text-underground-yellow mb-6">
          サンプル画像ギャラリー
        </h2>
        
        <div className="sample-gallery-grid">
          {sampleImages.map((imageUrl, index) => (
            <div
              key={index}
              className="sample-gallery-item"
              onClick={() => openModal(imageUrl)}
            >
              <img
                src={imageUrl}
                alt={`サンプル画像 ${index + 1}`}
                className="sample-gallery-image"
                loading="lazy"
              />
            </div>
          ))}
        </div>

        {affiliateLink && (
          <div className="mt-6 text-center">
            <a
              href={affiliateLink}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block px-6 py-3 bg-underground-yellow text-black font-bold rounded-lg hover:bg-yellow-300 transition-colors"
            >
              公式サイトで全画像を見る
            </a>
          </div>
        )}
      </section>

      {/* モーダル（ライトボックス） */}
      {selectedImage && (
        <div
          className="sample-gallery-modal"
          onClick={closeModal}
        >
          <div className="sample-gallery-modal-content" onClick={(e) => e.stopPropagation()}>
            <button
              className="sample-gallery-modal-close"
              onClick={closeModal}
              aria-label="閉じる"
            >
              ×
            </button>
            <img
              src={selectedImage}
              alt="拡大画像"
              className="sample-gallery-modal-image"
            />
          </div>
        </div>
      )}
    </>
  )
}

