'use client'

import { useEffect, useRef, useState } from 'react'
import { createRoot } from 'react-dom/client'
import FanzaSubscriptionPromo from './FanzaSubscriptionPromo'
import MgstageAd from './MgstageAd'

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

    // マーカーを探す（FANZA TVプロモ）
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

    // 広告位置2: 本文内のh2タグの後に広告を挿入（最初の2つのh2の後）
    const h2Elements = contentRef.current.querySelectorAll('h2')
    let adInsertedCount = 0
    
    h2Elements.forEach((h2, index) => {
      // 最初の2つのh2タグの後に広告を挿入
      if (adInsertedCount < 2 && h2.nextElementSibling && !h2.nextElementSibling.classList.contains('affiliate-ad-inline')) {
        const adContainer = document.createElement('div')
        adContainer.className = 'affiliate-ad-inline my-8'
        
        // h2の後に挿入
        h2.parentNode?.insertBefore(adContainer, h2.nextSibling)
        
        // Reactコンポーネントをレンダリング
        const root = createRoot(adContainer)
        // 1つ目と2つ目で異なる広告スクリプトを使用
        const scriptUrl = adInsertedCount === 0 
          ? 'https://www.mgstage.com/afscript/prestigebb/728_90/N2G56Q3UYEPYWXP7P8PKPRIDC3/'
          : 'https://www.mgstage.com/afscript/superch/728_90/N2G56Q3UYEPYWXP7P8PKPRIDC3/'
        const containerId = `mgstage-ad-inline-${adInsertedCount + 1}`
        
        root.render(<MgstageAd scriptUrl={scriptUrl} containerId={containerId} />)
        
        adInsertedCount++
      }
    })
  }, [content, affiliateLink, contentId, mounted])

  return (
    <div ref={contentRef} dangerouslySetInnerHTML={{ __html: content }} />
  )
}

