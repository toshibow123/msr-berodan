'use client'

import { useEffect, useState, useRef } from 'react'

interface ArticleContentWithAdsProps {
  htmlContent: string
}

export default function ArticleContentWithAds({ htmlContent }: ArticleContentWithAdsProps) {
  const [processedContent, setProcessedContent] = useState<string>('')
  const contentRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // HTMLコンテンツを解析して、1つ目のh2タグの後に広告プレースホルダーを挿入
    let processed = htmlContent
    const h2Regex = /(<h2[^>]*>.*?<\/h2>)/g
    const h2Matches = [...processed.matchAll(h2Regex)]
    
    // 1つ目のh2タグの後に広告を直接挿入（位置3 - 作品タイトル直後）
    // 広告コードは固定値のみを使用（affiliateId, bannerIdは固定値）ため、XSSリスクは低い
    if (h2Matches.length >= 1) {
      const firstH2Match = h2Matches[0]
      if (firstH2Match.index !== undefined) {
        const insertPosition = firstH2Match.index + firstH2Match[0].length
        // 広告のHTMLコードを直接挿入（位置2と同じスタイル）
        // 固定値のみを使用しているため、XSSリスクは低い
        const dataId = '43a8eba658580aad40df9b33383be12f' // 固定値
        
        // scriptタグはuseEffectで動的に追加するため、ここでは含めない
        const adHtml = '\n\n<div class="my-8 flex justify-center gap-4 w-full flex-wrap">' +
          `<div class="flex justify-center ad-position-3" style="min-height:250px; flex: 1 1 300px" data-widget-id="${dataId}" suppresshydrationwarning="true">` +
          `<ins class="dmm-widget-placement" data-id="${dataId}" style="background:transparent"></ins>` +
          '</div>' +
          '</div>\n\n'
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
    if (!contentRef.current || typeof window === 'undefined') return
    
    // アフィリエイトリンクにtarget="_blank"を追加
    const links = contentRef.current.querySelectorAll('a[href*="al.fanza.co.jp"], a[href*="al.dmm.co.jp"], a[href*="dmm.co.jp"]')
    links.forEach((link) => {
      const anchor = link as HTMLAnchorElement
      if (!anchor.target) {
        anchor.target = '_blank'
        anchor.rel = 'noopener noreferrer sponsored'
      }
    })
    
    // 位置3の広告スクリプトを動的に読み込む
    // dangerouslySetInnerHTMLで挿入された<script>タグは実行されないため、動的に追加する必要がある
    const adContainers = contentRef.current.querySelectorAll('.ad-position-3')
    adContainers.forEach((container) => {
      const div = container as HTMLDivElement
      // 既にスクリプトが追加されている場合はスキップ
      if (div.querySelector('.dmm-widget-scripts')) return
      
      const dataId = div.getAttribute('data-widget-id') || '43a8eba658580aad40df9b33383be12f'
      const adScriptUrl = 'https://widget-view.dmm.co.jp/js/placement.js'
      
      const script = document.createElement('script')
      script.className = 'dmm-widget-scripts'
      script.setAttribute('data-id', dataId)
      script.src = adScriptUrl
      div.appendChild(script)
    })
  }, [processedContent])


  // 注意: 記事本文は信頼できるソース（自分たちが生成した記事）からのみ取得されるため、
  // XSSリスクは比較的低いが、より安全にするためにはDOMPurifyでサニタイズすることを推奨
  // npm install dompurify @types/dompurify を実行後、以下を有効化:
  // import DOMPurify from 'isomorphic-dompurify'
  // const sanitizedContent = DOMPurify.sanitize(processedContent)
  
  return (
    <div 
      ref={contentRef}
      className="text-neutral-200 leading-relaxed space-y-4"
      dangerouslySetInnerHTML={{ __html: processedContent }}
    />
  )
}
