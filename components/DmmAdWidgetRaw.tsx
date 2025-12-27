'use client'

import { useEffect, useRef } from 'react'

interface DmmAdWidgetRawProps {
  adId: string
}

export default function DmmAdWidgetRaw({ adId }: DmmAdWidgetRawProps) {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!containerRef.current || typeof window === 'undefined') return

    // 既存の要素をクリーンアップ
    containerRef.current.innerHTML = ''

    // 少し遅延させてから広告を読み込む（DOMの準備を待つ）
    const timer = setTimeout(() => {
      if (!containerRef.current) return

      // <ins>タグを作成
      const insElement = document.createElement('ins')
      insElement.className = 'dmm-widget-placement'
      insElement.setAttribute('data-id', adId)
      insElement.style.background = 'transparent'
      insElement.style.display = 'block'
      insElement.style.width = '100%'
      insElement.style.minHeight = '250px'

      // <script>タグを作成
      const scriptElement = document.createElement('script')
      scriptElement.src = 'https://widget-view.dmm.co.jp/js/placement.js'
      scriptElement.className = 'dmm-widget-scripts'
      scriptElement.setAttribute('data-id', adId)
      scriptElement.async = true

      // 順番に追加（insの後にscript）
      containerRef.current.appendChild(insElement)
      containerRef.current.appendChild(scriptElement)

      // スクリプトが読み込まれた後に広告を初期化
      scriptElement.onload = () => {
        console.log('DMM広告スクリプト読み込み完了:', adId)
        // 広告が表示されるまで少し待つ
        setTimeout(() => {
          const adContent = containerRef.current?.querySelector('iframe, img, a')
          if (adContent) {
            console.log('広告コンテンツ検出:', adId)
          } else {
            console.warn('広告コンテンツが見つかりません:', adId)
          }
        }, 2000)
      }

      scriptElement.onerror = () => {
        console.error('DMM広告スクリプト読み込みエラー:', adId)
      }
    }, 100)

    return () => {
      clearTimeout(timer)
      if (containerRef.current) {
        containerRef.current.innerHTML = ''
      }
    }
  }, [adId])

  return (
    <div ref={containerRef} className="my-8 flex justify-center w-full" style={{ minHeight: '250px' }} />
  )
}
