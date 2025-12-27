'use client'

import { useEffect, useRef } from 'react'

interface DmmCampaignBannerProps {
  affiliateId?: string
  bannerId: string
}

export default function DmmCampaignBanner({ 
  affiliateId = 'toshichan-002',
  bannerId 
}: DmmCampaignBannerProps) {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!containerRef.current || typeof window === 'undefined') return

    // 既存の要素をクリーンアップ
    containerRef.current.innerHTML = ''

    // <ins>タグを作成
    const insElement = document.createElement('ins')
    insElement.className = 'widget-banner'

    // <script>タグを作成
    const scriptElement = document.createElement('script')
    scriptElement.className = 'widget-banner-script'
    scriptElement.src = `https://widget-view.dmm.co.jp/js/banner_placement.js?affiliate_id=${affiliateId}&banner_id=${bannerId}`

    // 順番に追加（insの後にscript）
    containerRef.current.appendChild(insElement)
    containerRef.current.appendChild(scriptElement)

    return () => {
      if (containerRef.current) {
        containerRef.current.innerHTML = ''
      }
    }
  }, [affiliateId, bannerId])

  return (
    <div ref={containerRef} className="my-6 flex justify-center w-full" />
  )
}

