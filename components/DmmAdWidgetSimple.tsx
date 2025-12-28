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

    // リトライ管理用の変数
    let retryCount = 0
    const maxRetries = 5
    let retryTimer: NodeJS.Timeout | null = null
    let isInitialized = false

    // 少し遅延させてから広告を読み込む（DOMの準備を待つ）
    const timer = setTimeout(() => {
      if (!containerRef.current) return

      // <ins>タグを作成（ユーザー指定の形式に合わせる）
      const insElement = document.createElement('ins')
      insElement.className = 'dmm-widget-placement'
      insElement.setAttribute('data-id', adId)
      insElement.style.background = 'transparent'
      insElement.style.display = 'block'
      insElement.style.width = '100%'
      insElement.style.minHeight = '250px'
      containerRef.current.appendChild(insElement)

      // スクリプトはグローバルに1回だけ読み込む
      const scriptUrl = 'https://widget-view.dmm.co.jp/js/placement.js'
      let globalScript = document.querySelector(`script[src="${scriptUrl}"]`) as HTMLScriptElement
      
      // この広告用のスクリプトタグ（data-id付き）を追加
      // DMM広告ウィジェットは、<ins>タグとdata-id付きの<script>タグの両方が必要
      // 注意: <script>タグにはsrc属性を設定しない（グローバルスクリプトが読み込む）
      const adScriptElement = document.createElement('script')
      adScriptElement.className = 'dmm-widget-scripts'
      adScriptElement.setAttribute('data-id', adId)
      containerRef.current.appendChild(adScriptElement)

      const initAds = () => {
        // 既に初期化済みの場合はスキップ
        if (isInitialized) {
          return
        }

        // リトライ回数の上限チェック
        if (retryCount >= maxRetries) {
          console.warn('広告初期化リトライ上限に達しました:', adId, '試行回数:', retryCount)
          return
        }

        retryTimer = setTimeout(() => {
          retryCount++
          
          // window.DMMオブジェクトの準備を確認
          if (typeof window !== 'undefined' && window.DMM && window.DMM.widget && typeof window.DMM.widget.init === 'function') {
            try {
              window.DMM.widget.init()
              console.log('DMM広告初期化完了:', adId, '試行回数:', retryCount)
              isInitialized = true
              
              // 広告が表示されたか確認（少し待ってから）
              setTimeout(() => {
                const adContent = containerRef.current?.querySelector('iframe, img, a, div[id*="dmm"], div[class*="dmm"], div[class*="widget"], div[class*="item"]')
                if (!adContent && retryCount < maxRetries) {
                  console.log('広告が表示されていないため再初期化:', adId)
                  isInitialized = false
                  initAds()
                } else if (adContent) {
                  console.log('広告コンテンツ検出:', adId)
                }
              }, 3000)
            } catch (e) {
              console.error('広告初期化エラー:', adId, e)
              isInitialized = false
              if (retryCount < maxRetries) {
                initAds()
              }
            }
          } else {
            // window.DMMがまだ準備されていない場合
            if (retryCount < maxRetries) {
              console.log('DMMオブジェクトが未準備、再試行:', adId, '試行回数:', retryCount)
              initAds()
            } else {
              console.warn('DMMオブジェクトが準備されませんでした:', adId)
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
          // グローバルスクリプト読み込み後、少し待ってから初期化
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

    }, 300)

    return () => {
      clearTimeout(timer)
      // クリーンアップ時にリトライタイマーもクリア
      if (retryTimer) {
        clearTimeout(retryTimer)
      }
    }
  }, [adId])

  return (
    <div ref={containerRef} className="my-8 flex justify-center w-full" style={{ minHeight: '250px' }} />
  )
}

