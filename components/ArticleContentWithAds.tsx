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
          insElement.style.display = 'block'
          insElement.style.width = '100%'
          insElement.style.minHeight = '250px'
          adContainer.appendChild(insElement)

          // スクリプトはグローバルに1回だけ読み込む
          const scriptUrl = 'https://widget-view.dmm.co.jp/js/placement.js'
          let globalScript = document.querySelector(`script[src="${scriptUrl}"]`) as HTMLScriptElement
          
          // この広告用のスクリプトタグ（data-id付き）を追加
          const adScriptElement = document.createElement('script')
          adScriptElement.className = 'dmm-widget-scripts'
          adScriptElement.setAttribute('data-id', '43a8eba658580aad40df9b33383be12f')
          adContainer.appendChild(adScriptElement)

          // リトライ管理用の変数
          let retryCount = 0
          const maxRetries = 5
          let retryTimer: NodeJS.Timeout | null = null
          let isInitialized = false
          let cleanupFn: (() => void) | null = null

          const initAds = () => {
            // 既に初期化済みの場合はスキップ
            if (isInitialized) {
              return
            }

            // リトライ回数の上限チェック
            if (retryCount >= maxRetries) {
              console.warn('広告初期化リトライ上限に達しました: 位置3', '試行回数:', retryCount)
              return
            }

            retryTimer = setTimeout(() => {
              retryCount++
              
              // window.DMMオブジェクトの準備を確認
              if (typeof window !== 'undefined' && window.DMM && window.DMM.widget && typeof window.DMM.widget.init === 'function') {
                try {
                  window.DMM.widget.init()
                  console.log('DMM広告初期化完了: 位置3', '試行回数:', retryCount)
                  isInitialized = true
                  
                  // 広告が表示されたか確認（少し待ってから）
                  setTimeout(() => {
                    const adContent = adContainer.querySelector('iframe, img, a, div[id*="dmm"], div[class*="dmm"], div[class*="widget"], div[class*="item"]')
                    if (!adContent && retryCount < maxRetries) {
                      console.log('広告が表示されていないため再初期化: 位置3')
                      isInitialized = false
                      initAds()
                    } else if (adContent) {
                      console.log('広告コンテンツ検出: 位置3')
                    }
                  }, 3000)
                } catch (e) {
                  console.error('広告初期化エラー: 位置3', e)
                  isInitialized = false
                  if (retryCount < maxRetries) {
                    initAds()
                  }
                }
              } else {
                // window.DMMがまだ準備されていない場合
                if (retryCount < maxRetries) {
                  console.log('DMMオブジェクトが未準備、再試行: 位置3', '試行回数:', retryCount)
                  initAds()
                } else {
                  console.warn('DMMオブジェクトが準備されませんでした: 位置3')
                }
              }
            }, 2000 + (retryCount * 1000)) // 2秒、3秒、4秒...と段階的に延長
          }
          
          if (!globalScript) {
            globalScript = document.createElement('script')
            globalScript.src = scriptUrl
            globalScript.async = true
            globalScript.onload = () => {
              console.log('DMM広告スクリプト読み込み完了（グローバル）')
              globalScript.setAttribute('data-loaded', 'true')
              setTimeout(() => {
                initAds()
              }, 1000)
            }
            globalScript.onerror = () => {
              console.error('DMM広告スクリプト読み込みエラー')
            }
            document.body.appendChild(globalScript)
          } else if (globalScript.getAttribute('data-loaded') === 'true') {
            // 既に読み込まれている場合は即座に初期化
            setTimeout(() => {
              initAds()
            }, 1000)
          } else {
            // 読み込み中の場合はonloadを待つ
            const loadHandler = () => {
              globalScript.setAttribute('data-loaded', 'true')
              setTimeout(() => {
                initAds()
              }, 1000)
              globalScript.removeEventListener('load', loadHandler)
            }
            globalScript.addEventListener('load', loadHandler)
          }
          
          // クリーンアップ関数を設定
          cleanupFn = () => {
            if (retryTimer) {
              clearTimeout(retryTimer)
            }
          }
        }
      }, 300)
      
      let cleanupFn: (() => void) | null = null
      
      return () => {
        clearTimeout(timer)
        if (cleanupFn) {
          cleanupFn()
        }
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
