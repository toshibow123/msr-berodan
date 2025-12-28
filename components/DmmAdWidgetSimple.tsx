'use client'

import { useEffect, useRef } from 'react'

interface DmmAdWidgetSimpleProps {
  adId: string
}

export default function DmmAdWidgetSimple({ adId }: DmmAdWidgetSimpleProps) {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!containerRef.current || typeof window === 'undefined') return

    // 既存の要素をクリーンアップ
    containerRef.current.innerHTML = ''

    // 少し遅延させてから広告を読み込む（DOMの準備を待つ）
    const timer = setTimeout(() => {
      if (!containerRef.current) return

      // <ins>タグを作成（ユーザー指定の形式に合わせる）
      const insElement = document.createElement('ins')
      insElement.className = 'dmm-widget-placement'
      insElement.setAttribute('data-id', adId)
      insElement.style.background = 'transparent'
      containerRef.current.appendChild(insElement)

      // スクリプトはグローバルに1回だけ読み込む
      const scriptUrl = 'https://widget-view.dmm.co.jp/js/placement.js'
      let globalScript = document.querySelector(`script[src="${scriptUrl}"]`) as HTMLScriptElement
      
      // この広告用のスクリプトタグ（data-id付き）を追加
      // DMM広告ウィジェットは、<ins>タグとdata-id付きの<script>タグの両方が必要
      const adScriptElement = document.createElement('script')
      adScriptElement.className = 'dmm-widget-scripts'
      adScriptElement.setAttribute('data-id', adId)
      containerRef.current.appendChild(adScriptElement)

      const initAds = () => {
        // この広告位置を個別に初期化
        setTimeout(() => {
          if (window.DMM && window.DMM.widget) {
            // 特定の広告IDを指定して初期化を試みる
            try {
              window.DMM.widget.init()
              console.log('DMM広告初期化完了:', adId)
              
              // この広告位置のコンテナを明示的に初期化
              const insElement = containerRef.current?.querySelector(`ins[data-id="${adId}"]`)
              if (insElement) {
                // 広告が表示されるまで少し待ってから再初期化を試みる
                setTimeout(() => {
                  if (window.DMM && window.DMM.widget) {
                    window.DMM.widget.init()
                  }
                }, 2000)
              }
            } catch (e) {
              console.error('広告初期化エラー:', adId, e)
            }
          }
        }, 1500)
      }
      
      if (!globalScript) {
        globalScript = document.createElement('script')
        globalScript.src = scriptUrl
        globalScript.async = true
        globalScript.onload = () => {
          console.log('DMM広告スクリプト読み込み完了（グローバル）')
          globalScript.setAttribute('data-loaded', 'true')
          initAds()
        }
        document.body.appendChild(globalScript)
      } else if (globalScript.getAttribute('data-loaded') === 'true') {
        // 既に読み込まれている場合は即座に初期化
        initAds()
      } else {
        // 読み込み中の場合はonloadを待つ
        const loadHandler = () => {
          globalScript.setAttribute('data-loaded', 'true')
          initAds()
          globalScript.removeEventListener('load', loadHandler)
        }
        globalScript.addEventListener('load', loadHandler)
      }

      // 広告が表示されるまで少し待つ（位置によって待機時間を調整）
      const waitTime = adId === 'f8bfa16b6ea380c9d074a49090eed3b0' ? 6000 : 4000
      setTimeout(() => {
        const adContent = containerRef.current?.querySelector('iframe, img, a, div[id*="dmm"], div[class*="dmm"], div[class*="widget"], div[class*="item"]')
        if (adContent) {
          console.log('広告コンテンツ検出:', adId)
        } else {
          console.warn('広告コンテンツが見つかりません:', adId)
          // 再度初期化を試みる
          if (window.DMM && window.DMM.widget) {
            window.DMM.widget.init()
          }
        }
      }, waitTime)
    }, 500)

    return () => {
      clearTimeout(timer)
      // クリーンアップはしない（広告が表示されるまで保持）
    }
  }, [adId])

  return (
    <div ref={containerRef} className="my-8 flex justify-center w-full" style={{ minHeight: '250px' }} />
  )
}
