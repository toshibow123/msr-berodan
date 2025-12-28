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
    
    // 2つ目のh2タグの後に広告を直接挿入（位置3）
    if (h2Matches.length >= 2) {
      const secondH2Match = h2Matches[1]
      if (secondH2Match.index !== undefined) {
        const insertPosition = secondH2Match.index + secondH2Match[0].length
        // 広告のHTMLコードを直接挿入
        const adHtml = '<div class="my-8 flex justify-center w-full" style="min-height:250px"><ins class="dmm-widget-placement" data-id="43a8eba658580aad40df9b33383be12f" style="background:transparent"></ins><script src="https://widget-view.dmm.co.jp/js/placement.js" class="dmm-widget-scripts" data-id="43a8eba658580aad40df9b33383be12f"></script></div>'
        processed = processed.slice(0, insertPosition) + adHtml + processed.slice(insertPosition)
      }
    }
    
    // 「今すぐチェックする」リンクを削除
    // <div className="affiliate-link">...</div> のパターンを削除
    processed = processed.replace(/<div[^>]*class="affiliate-link"[^>]*>[\s\S]*?<\/div>/gi, '')
    // または <a>タグで「今すぐチェックする」を含むものを削除
    processed = processed.replace(/<a[^>]*>今すぐチェックする<\/a>/gi, '')
    
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


  return (
    <div 
      ref={contentRef}
      className="text-neutral-200 leading-relaxed space-y-6"
      dangerouslySetInnerHTML={{ __html: processedContent }}
    />
  )
}
