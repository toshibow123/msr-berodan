'use client'

import { useEffect, useRef } from 'react'

interface MgstageWidgetAdProps {
  containerClass?: string
  widgetId?: string
  affiliateId?: string
}

export default function MgstageWidgetAd({ 
  containerClass = 'dridb2ih',
  widgetId = 'mgs_Widget',
  affiliateId = 'N2G56Q3UYEPYWXP7P8PKPRIDC3'
}: MgstageWidgetAdProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const scriptLoadedRef = useRef(false)

  useEffect(() => {
    if (!containerRef.current || scriptLoadedRef.current || typeof window === 'undefined') {
      return
    }

    // 既にスクリプトが読み込まれているかチェック
    const existingScript = document.getElementById(widgetId)
    if (existingScript) {
      scriptLoadedRef.current = true
      return
    }

    // コンテナにクラスを設定
    if (containerRef.current) {
      containerRef.current.className = containerClass
    }

    // スクリプトを動的に作成
    const script = document.createElement('script')
    script.id = widgetId
    script.type = 'text/javascript'
    script.charset = 'utf-8'
    script.src = `https://www.mgstage.com/js/mgs_Widget_r.js?c=${affiliateId}&d=h&n=s&h=s&m=23&class=${containerClass}`

    script.onload = () => {
      scriptLoadedRef.current = true
    }

    script.onerror = (error) => {
      console.error('MGStage Widget広告スクリプト読み込みエラー:', error)
    }

    // bodyに追加
    document.body.appendChild(script)

    return () => {
      // クリーンアップはしない（広告が表示されるまで）
    }
  }, [containerClass, widgetId, affiliateId])

  return (
    <div className="my-8">
      <div className="text-center mb-2">
        <span className="text-xs text-elegant-text-dark font-medium bg-elegant-bg-lighter px-3 py-1 rounded-full border border-elegant-border">
          PR・アフィリエイト広告
        </span>
      </div>
      <div className="flex justify-center overflow-x-auto w-full">
        <div 
          ref={containerRef}
          className={`${containerClass} h-[90px]`}
          style={{ minWidth: '1200px', width: '100%' }}
        />
      </div>
    </div>
  )
}

