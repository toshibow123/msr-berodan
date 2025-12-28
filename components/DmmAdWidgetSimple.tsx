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
        // この広告位置を個別に初期化
        const retryInit = (attempt: number = 0) => {
          if (attempt > 3) {
            console.warn('広告初期化リトライ上限に達しました:', adId)
            return
          }

          setTimeout(() => {
            if (window.DMM && window.DMM.widget) {
              try {
                window.DMM.widget.init()
                console.log('DMM広告初期化完了:', adId, '試行回数:', attempt + 1)
                
                // 広告が表示されたか確認
                setTimeout(() => {
                  const adContent = containerRef.current?.querySelector('iframe, img, a, div[id*="dmm"], div[class*="dmm"], div[class*="widget"], div[class*="item"]')
                  if (!adContent && attempt < 3) {
                    console.log('広告が表示されていないため再初期化:', adId)
                    retryInit(attempt + 1)
                  } else if (adContent) {
                    console.log('広告コンテンツ検出:', adId)
                  }
                }, 2000)
              } catch (e) {
                console.error('広告初期化エラー:', adId, e)
                if (attempt < 3) {
                  retryInit(attempt + 1)
                }
              }
            } else if (attempt < 3) {
              console.log('DMMオブジェクトが未準備、再試行:', adId)
              retryInit(attempt + 1)
            }
          }, 1000 + (attempt * 1000))
        }
        
        retryInit()
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
          }, 500)
        }
        globalScript.onerror = () => {
          console.error('DMM広告スクリプト読み込みエラー')
        }
        document.body.appendChild(globalScript)
      } else if (globalScript.getAttribute('data-loaded') === 'true') {
        // 既に読み込まれている場合は即座に初期化
        setTimeout(() => {
          initAds()
        }, 500)
      } else {
        // 読み込み中の場合はonloadを待つ
        const loadHandler = () => {
          globalScript.setAttribute('data-loaded', 'true')
          setTimeout(() => {
            initAds()
          }, 500)
          globalScript.removeEventListener('load', loadHandler)
        }
        globalScript.addEventListener('load', loadHandler)
      }

    }, 300)

    return () => {
      clearTimeout(timer)
      // クリーンアップはしない（広告が表示されるまで保持）
    }
  }, [adId])

  return (
    <div ref={containerRef} className="my-8 flex justify-center w-full" style={{ minHeight: '250px' }} />
  )
}
