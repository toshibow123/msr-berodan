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
    // アフィリエイトリンクにtarget="_blank"を追加
    if (contentRef.current && typeof window !== 'undefined') {
      const links = contentRef.current.querySelectorAll('a[href*="al.fanza.co.jp"], a[href*="al.dmm.co.jp"], a[href*="dmm.co.jp"]')
      links.forEach((link) => {
        const anchor = link as HTMLAnchorElement
        if (!anchor.target) {
          anchor.target = '_blank'
          anchor.rel = 'noopener noreferrer sponsored'
        }
      })
    }
  }, [processedContent])

  useEffect(() => {
    // 広告を実際に挿入
    if (contentRef.current && typeof window !== 'undefined') {
      const timer = setTimeout(() => {
        const marker = contentRef.current?.querySelector('#ad-position-3-marker')
        if (marker && !marker.nextElementSibling?.classList.contains('ad-widget-container')) {
          const adContainer = document.createElement('div')
          adContainer.className = 'ad-widget-container my-8 flex justify-center w-full'
          adContainer.style.minHeight = '250px'
          marker.parentNode?.insertBefore(adContainer, marker.nextSibling)
          
          // <ins>タグを直接挿入
          const insElement = document.createElement('ins')
          insElement.className = 'dmm-widget-placement'
          insElement.setAttribute('data-id', '43a8eba658580aad40df9b33383be12f')
          insElement.style.background = 'transparent'
          adContainer.appendChild(insElement)

          // スクリプトはグローバルに1回だけ読み込む
          const scriptUrl = 'https://widget-view.dmm.co.jp/js/placement.js'
          let globalScript = document.querySelector(`script[src="${scriptUrl}"]`) as HTMLScriptElement
          
          if (!globalScript) {
            globalScript = document.createElement('script')
            globalScript.src = scriptUrl
            globalScript.async = true
            document.body.appendChild(globalScript)
          }

          // この広告用のスクリプトタグ（data-id付き）を追加
          const adScriptElement = document.createElement('script')
          adScriptElement.className = 'dmm-widget-scripts'
          adScriptElement.setAttribute('data-id', '43a8eba658580aad40df9b33383be12f')
          adContainer.appendChild(adScriptElement)

          // 広告の初期化を試みる
          globalScript.onload = () => {
            setTimeout(() => {
              if (window.DMM && window.DMM.widget) {
                window.DMM.widget.init()
              }
            }, 1000)
          }
        }
      }, 500)

      return () => clearTimeout(timer)
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
