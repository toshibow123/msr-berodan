'use client'

import { useState, useEffect } from 'react'

interface ContentWithSampleImagesProps {
  htmlContent: string
  contentId: string
  affiliateLink?: string
}

/**
 * 記事コンテンツに見出しごとにサンプル画像を散らして配置するコンポーネント
 */
export default function ContentWithSampleImages({
  htmlContent,
  contentId,
  affiliateLink
}: ContentWithSampleImagesProps) {
  const [selectedImage, setSelectedImage] = useState<string | null>(null)
  const [processedContent, setProcessedContent] = useState<string>('')

  useEffect(() => {
    // HTMLコンテンツを解析して、h2タグの後にサンプル画像を挿入
    let processed = htmlContent
    const h2Regex = /(<h2[^>]*>.*?<\/h2>)/g
    const h2Matches = [...processed.matchAll(h2Regex)]
    
    // サンプル画像URLを生成（1-6枚目）
    const images = Array.from({ length: 6 }, (_, i) => {
      const imageNumber = i + 1
      return `https://pics.dmm.co.jp/digital/video/${contentId}/${contentId}jp-${imageNumber}.jpg`
    })
    
    // 見出しの数と画像の数を考慮して、適切に配置
    let imageIndex = 0
    
    // 後ろから挿入することで、インデックスのずれを防ぐ
    for (let i = h2Matches.length - 1; i >= 0 && imageIndex < images.length; i--) {
      const match = h2Matches[i]
      if (match.index !== undefined) {
        const insertPosition = match.index + match[0].length
        const imageUrl = images[imageIndex]
        // アフィリエイトリンクがある場合は、画像を<a>タグで囲む
        const imageHtml = affiliateLink ? `
          <div class="sample-image-inline" data-image-url="${imageUrl}">
            <a href="${affiliateLink}" target="_blank" rel="noopener noreferrer" class="block">
              <img 
                src="${imageUrl}" 
                alt="サンプル画像 ${imageIndex + 1}" 
                class="sample-image-inline-img cursor-pointer"
                loading="lazy"
              />
            </a>
          </div>
        ` : `
          <div class="sample-image-inline" data-image-url="${imageUrl}">
            <img 
              src="${imageUrl}" 
              alt="サンプル画像 ${imageIndex + 1}" 
              class="sample-image-inline-img"
              loading="lazy"
            />
          </div>
        `
        processed = processed.slice(0, insertPosition) + imageHtml + processed.slice(insertPosition)
        imageIndex++
      }
    }
    
    setProcessedContent(processed)
  }, [htmlContent, contentId])

  // 画像右クリック時のモーダル表示（左クリックはアフィリエイトリンクに飛ぶ）
  useEffect(() => {
    const handleImageRightClick = (e: MouseEvent) => {
      const target = e.target as HTMLElement
      if (target.classList.contains('sample-image-inline-img')) {
        // 右クリック（contextmenu）でモーダルを開く
        e.preventDefault()
        const container = target.closest('.sample-image-inline')
        if (container) {
          const imageUrl = container.getAttribute('data-image-url')
          if (imageUrl) {
            setSelectedImage(imageUrl)
            document.body.style.overflow = 'hidden'
          }
        }
      }
    }

    document.addEventListener('contextmenu', handleImageRightClick)
    return () => {
      document.removeEventListener('contextmenu', handleImageRightClick)
    }
  }, [])

  const closeModal = () => {
    setSelectedImage(null)
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

  // 注意: 記事本文は信頼できるソース（自分たちが生成した記事）からのみ取得されるため、
  // XSSリスクは比較的低いが、より安全にするためにはDOMPurifyでサニタイズすることを推奨
  // npm install dompurify @types/dompurify を実行後、以下を有効化:
  // import DOMPurify from 'isomorphic-dompurify'
  // const sanitizedContent = DOMPurify.sanitize(processedContent)
  
  return (
    <>
      <div 
        className="prose prose-invert max-w-none"
        dangerouslySetInnerHTML={{ __html: processedContent }}
      />
      
      {affiliateLink && (
        <div className="mt-8 text-center">
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

