'use client'

import { useEffect, useRef, useState } from 'react'
import { createRoot } from 'react-dom/client'
import FanzaSubscriptionPromo from './FanzaSubscriptionPromo'

interface ArticleContentWithPromoProps {
  content: string
  affiliateLink?: string
  contentId?: string
}

export default function ArticleContentWithPromo({
  content,
  affiliateLink,
  contentId
}: ArticleContentWithPromoProps) {
  const contentRef = useRef<HTMLDivElement>(null)
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  useEffect(() => {
    if (!contentRef.current || !mounted) return

    // マーカーを探す
    const markers = contentRef.current.querySelectorAll('[data-fanza-promo-marker="true"]')
    
    markers.forEach((marker) => {
      // 既にプロモコンポーネントが挿入されていないか確認
      if (marker.nextElementSibling?.classList.contains('fanza-promo-wrapper')) {
        return
      }

      // プロモコンポーネント用のコンテナを作成
      const promoContainer = document.createElement('div')
      promoContainer.className = 'fanza-promo-wrapper'
      
      // マーカーの後に挿入
      marker.parentNode?.insertBefore(promoContainer, marker.nextSibling)
      
      // Reactコンポーネントをレンダリング
      const root = createRoot(promoContainer)
      root.render(
        <FanzaSubscriptionPromo 
          singleAffiliateUrl={affiliateLink}
          contentId={contentId}
        />
      )
      
      // マーカーを削除
      marker.remove()
    })
  }, [content, affiliateLink, contentId, mounted])

  return (
    <div ref={contentRef} dangerouslySetInnerHTML={{ __html: content }} />
  )
}

