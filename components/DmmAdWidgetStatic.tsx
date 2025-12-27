'use client'

import { useEffect, useRef } from 'react'

interface DmmAdWidgetStaticProps {
  adId: string
}

// グローバルにスクリプトが読み込まれているかチェック
const loadedScripts = new Set<string>()

export default function DmmAdWidgetStatic({ adId }: DmmAdWidgetStaticProps) {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!containerRef.current || typeof window === 'undefined') return

    console.log('DmmAdWidgetStatic初期化開始:', adId)

    // 既存の要素をクリーンアップ
    containerRef.current.innerHTML = ''

    // 少し遅延させてから広告を読み込む
    const timer = setTimeout(() => {
      if (!containerRef.current) return

      console.log('広告要素作成開始:', adId)

      // <ins>タグを作成
      const insElement = document.createElement('ins')
      insElement.className = 'dmm-widget-placement'
      insElement.setAttribute('data-id', adId)
      insElement.style.background = 'transparent'
      insElement.style.display = 'block'
      insElement.style.width = '100%'
      insElement.style.minHeight = '250px'

      containerRef.current.appendChild(insElement)

      // スクリプトは一度だけ読み込む（グローバルに管理）
      const scriptUrl = 'https://widget-view.dmm.co.jp/js/placement.js'
      if (!loadedScripts.has(scriptUrl)) {
        const scriptElement = document.createElement('script')
        scriptElement.src = scriptUrl
        scriptElement.className = 'dmm-widget-scripts'
        scriptElement.async = true
        
        scriptElement.onload = () => {
          console.log('DMM広告スクリプト読み込み完了（グローバル）')
          loadedScripts.add(scriptUrl)
        }

        scriptElement.onerror = () => {
          console.error('DMM広告スクリプト読み込みエラー')
        }

        // bodyに追加（グローバルに1つだけ）
        document.body.appendChild(scriptElement)
        loadedScripts.add(scriptUrl)
      } else {
        console.log('スクリプトは既に読み込まれています')
      }

      // この広告用のスクリプトタグ（data-id付き）を追加
      const adScriptElement = document.createElement('script')
      adScriptElement.className = 'dmm-widget-scripts'
      adScriptElement.setAttribute('data-id', adId)
      adScriptElement.textContent = `
        if (window.DMM && window.DMM.widget) {
          window.DMM.widget.init();
        }
      `

      containerRef.current.appendChild(adScriptElement)

      console.log('広告要素追加完了:', adId)

      // 広告が表示されるまで少し待つ
      setTimeout(() => {
        const adContent = containerRef.current?.querySelector('iframe, img, a, div[id*="dmm"], div[class*="dmm"]')
        if (adContent) {
          console.log('広告コンテンツ検出:', adId, adContent)
        } else {
          console.warn('広告コンテンツが見つかりません:', adId)
          // デバッグ用：コンテナの内容を表示
          console.log('コンテナの内容:', containerRef.current?.innerHTML)
        }
      }, 3000)
    }, 200)

    return () => {
      clearTimeout(timer)
      // コンテナの内容はクリーンアップしない（広告が表示されるまで）
    }
  }, [adId])

  return (
    <div ref={containerRef} className="my-8 flex justify-center w-full" style={{ minHeight: '250px' }} />
  )
}
