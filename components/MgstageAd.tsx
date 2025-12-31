'use client'

import { useEffect, useRef, useState } from 'react'

interface MgstageAdProps {
  scriptUrl: string
  containerId?: string
}

export default function MgstageAd({ scriptUrl, containerId = 'mgstage-ad-top' }: MgstageAdProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const scriptLoadedRef = useRef(false)
  const [debugInfo, setDebugInfo] = useState<string>('')

  useEffect(() => {
    if (scriptLoadedRef.current || typeof window === 'undefined') {
      return
    }

    // コンテナが存在することを確認（少し遅延して確認）
    const checkAndLoad = () => {
      const container = document.getElementById(containerId)
      if (!container) {
        console.warn('MGStage広告コンテナが見つかりません、再試行します:', containerId)
        setTimeout(checkAndLoad, 100)
        return
      }

      console.log('MGStage広告コンポーネント初期化開始')
      setDebugInfo('初期化中...')

      // 既にスクリプトが読み込まれているかチェック
      const existingScript = document.querySelector(`script[src="${scriptUrl}"]`)
      if (existingScript) {
        console.log('MGStageスクリプトは既に読み込まれています')
        scriptLoadedRef.current = true
        setDebugInfo('スクリプト読み込み済み')
        return
      }

      console.log('MGStage広告コンテナ確認:', containerId, container)

      // スクリプトを動的に読み込む
      const script = document.createElement('script')
      script.type = 'text/javascript'
      script.src = scriptUrl
      script.async = true

      script.onload = () => {
        console.log('MGStage広告スクリプト読み込み完了')
        scriptLoadedRef.current = true
        setDebugInfo('スクリプト読み込み完了')
        
        // 広告が表示されるまで少し待つ
        setTimeout(() => {
          const adContent = container.querySelector('iframe, img, a, div[class*="mgstage"], div[id*="mgstage"]')
          if (adContent) {
            console.log('MGStage広告コンテンツ検出:', adContent)
            setDebugInfo('広告表示中')
          } else {
            console.warn('MGStage広告コンテンツが見つかりません')
            console.log('コンテナの内容:', container.innerHTML)
            setDebugInfo('広告コンテンツ未検出')
          }
        }, 2000)
      }

      script.onerror = (error) => {
        console.error('MGStage広告スクリプト読み込みエラー:', error)
        setDebugInfo('スクリプト読み込みエラー')
      }

      // bodyに追加
      document.body.appendChild(script)
      console.log('MGStageスクリプトをbodyに追加しました')
    }

    // 初回実行（少し遅延して実行）
    const timer = setTimeout(checkAndLoad, 100)

    return () => {
      clearTimeout(timer)
      // クリーンアップはしない（広告が表示されるまで）
    }
  }, [scriptUrl, containerId])

  return (
    <div className="my-8">
      <div className="text-center mb-2">
        <span className="text-xs text-elegant-text-dark font-medium bg-elegant-bg-lighter px-3 py-1 rounded-full border border-elegant-border">
          PR・アフィリエイト広告
        </span>
      </div>
      <div className="flex justify-center">
        <div 
          ref={containerRef}
          id={containerId}
          className="min-h-[90px] w-full max-w-[728px] bg-elegant-bg-lighter/30 border border-elegant-border/50 rounded"
        />
      </div>
      {/* デバッグ情報（開発時のみ、必要に応じてコメントアウト） */}
      {false && process.env.NODE_ENV === 'development' && debugInfo && (
        <div className="text-center mt-2">
          <span className="text-xs text-elegant-text-dark">
            デバッグ: {debugInfo}
          </span>
        </div>
      )}
    </div>
  )
}

