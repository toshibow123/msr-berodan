'use client'

import { useEffect, useRef } from 'react'

interface DmmAdWidgetProps {
  pcId: string
  mobileId: string
}

export default function DmmAdWidget({ pcId, mobileId }: DmmAdWidgetProps) {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!containerRef.current) return

    // 既存のスクリプトをクリーンアップ
    const existingScripts = containerRef.current.querySelectorAll('.dmm-widget-scripts')
    existingScripts.forEach(script => script.remove())

    // 画面サイズに応じてIDを決定
    const isMobile = window.innerWidth < 768
    const adId = isMobile ? mobileId : pcId

    // <ins>タグを作成
    const insElement = containerRef.current.querySelector('.dmm-widget-placement') as HTMLElement
    if (insElement) {
      insElement.setAttribute('data-id', adId)
    }

    // スクリプトを動的に読み込む
    const script = document.createElement('script')
    script.src = 'https://widget-view.dmm.com/js/placement.js'
    script.className = 'dmm-widget-scripts'
    script.setAttribute('data-id', adId)
    script.async = true

    containerRef.current.appendChild(script)

    // リサイズ時の処理
    const handleResize = () => {
      const currentIsMobile = window.innerWidth < 768
      const currentAdId = currentIsMobile ? mobileId : pcId
      
      if (insElement) {
        insElement.setAttribute('data-id', currentAdId)
      }
      
      // スクリプトを再読み込み
      const oldScript = containerRef.current?.querySelector('.dmm-widget-scripts')
      if (oldScript) {
        oldScript.remove()
      }
      
      const newScript = document.createElement('script')
      newScript.src = 'https://widget-view.dmm.com/js/placement.js'
      newScript.className = 'dmm-widget-scripts'
      newScript.setAttribute('data-id', currentAdId)
      newScript.async = true
      
      if (containerRef.current) {
        containerRef.current.appendChild(newScript)
      }
    }

    window.addEventListener('resize', handleResize)

    return () => {
      window.removeEventListener('resize', handleResize)
      const scripts = containerRef.current?.querySelectorAll('.dmm-widget-scripts')
      scripts?.forEach(s => s.remove())
    }
  }, [pcId, mobileId])

  return (
    <div ref={containerRef} className="my-8 flex justify-center">
      <ins
        className="dmm-widget-placement"
        data-id={typeof window !== 'undefined' && window.innerWidth < 768 ? mobileId : pcId}
        style={{ background: 'transparent' }}
      />
    </div>
  )
}
