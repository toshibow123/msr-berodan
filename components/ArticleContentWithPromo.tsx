'use client'

import { useEffect, useRef, useState } from 'react'
import { createRoot } from 'react-dom/client'
import FanzaSubscriptionPromo from './FanzaSubscriptionPromo'
import MgstageAd from './MgstageAd'
import MgsAd728x90 from './MgsAd728x90'

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

    // 広告位置: 本文内のh2タグの後に広告を挿入（最初の4つのh2の後）
    const h2Elements = contentRef.current.querySelectorAll('h2')
    let adInsertedCount = 0
    
    // 4つの異なる広告HTMLファイル
    const adFiles = [
      '/ads/mgs-728x90-1.html',
      '/ads/mgs-728x90-2.html',
      '/ads/mgs-728x90-3.html',
      '/ads/mgs-728x90-4.html'
    ]
    
    h2Elements.forEach((h2, index) => {
      // 最初の4つのh2タグの後に広告を挿入
      if (adInsertedCount < 4 && h2.nextElementSibling && !h2.nextElementSibling.classList.contains('affiliate-ad-inline')) {
        const adContainer = document.createElement('div')
        adContainer.className = 'affiliate-ad-inline my-8'
        
        // h2の後に挿入
        h2.parentNode?.insertBefore(adContainer, h2.nextSibling)
        
        // Reactコンポーネントをレンダリング
        const root = createRoot(adContainer)
        root.render(<MgsAd728x90 htmlFile={adFiles[adInsertedCount]} />)
        
        adInsertedCount++
      }
    })
  }, [content, affiliateLink, contentId, mounted])

  return (
    <div ref={contentRef} dangerouslySetInnerHTML={{ __html: content }} />
  )
}

