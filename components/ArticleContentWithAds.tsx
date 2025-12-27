'use client'

import { useEffect, useState, useRef } from 'react'

interface ArticleContentWithAdsProps {
  htmlContent: string
}

export default function ArticleContentWithAds({ htmlContent }: ArticleContentWithAdsProps) {
  const [processedContent, setProcessedContent] = useState<string>('')
  const contentRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // HTMLコンテンツを解析して、2つ目のh2タグの後に広告プレースホルダーを挿入
    let processed = htmlContent
    const h2Regex = /(<h2[^>]*>.*?<\/h2>)/g
    const h2Matches = [...processed.matchAll(h2Regex)]
    
    // 2つ目のh2タグの後に広告プレースホルダーを挿入（位置3）
    if (h2Matches.length >= 2) {
      const secondH2Match = h2Matches[1]
      if (secondH2Match.index !== undefined) {
        const insertPosition = secondH2Match.index + secondH2Match[0].length
        // 広告のプレースホルダーを挿入
        const adPlaceholder = '<div id="ad-position-3-marker" class="ad-marker"></div>'
        processed = processed.slice(0, insertPosition) + adPlaceholder + processed.slice(insertPosition)
      }
    }
    
    setProcessedContent(processed)
  }, [htmlContent])

  useEffect(() => {
    // 広告を実際に挿入
    if (contentRef.current && typeof window !== 'undefined') {
      const marker = contentRef.current.querySelector('#ad-position-3-marker')
      if (marker && !marker.nextElementSibling?.classList.contains('ad-widget-container')) {
        const adContainer = document.createElement('div')
        adContainer.className = 'ad-widget-container my-8'
        marker.parentNode?.insertBefore(adContainer, marker.nextSibling)
        
        // <ins>タグを直接挿入
        const insElement = document.createElement('ins')
        insElement.className = 'dmm-widget-placement'
        insElement.setAttribute('data-id', '43a8eba658580aad40df9b33383be12f')
        insElement.style.background = 'transparent'
        adContainer.appendChild(insElement)

        // <script>タグを動的に追加
        const scriptElement = document.createElement('script')
        scriptElement.src = 'https://widget-view.dmm.co.jp/js/placement.js'
        scriptElement.className = 'dmm-widget-scripts'
        scriptElement.setAttribute('data-id', '43a8eba658580aad40df9b33383be12f')
        adContainer.appendChild(scriptElement)
      }
    }
  }, [processedContent])

  return (
    <div 
      ref={contentRef}
      className="text-neutral-200 leading-relaxed space-y-6"
      dangerouslySetInnerHTML={{ __html: processedContent }}
    />
  )
}
