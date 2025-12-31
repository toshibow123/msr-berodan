'use client'

import { useEffect, useRef, useState } from 'react'

export default function MgsBanner() {
  const containerRef = useRef<HTMLDivElement>(null)
  const iframeRef = useRef<HTMLIFrameElement>(null)
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  useEffect(() => {
    if (!mounted || !iframeRef.current || typeof window === 'undefined') {
      return
    }

    // iframeの内容を設定
    const iframe = iframeRef.current
    const iframeDoc = iframe.contentDocument || iframe.contentWindow?.document
    
    if (iframeDoc) {
      iframeDoc.open()
      iframeDoc.write(`
        <!DOCTYPE html>
        <html>
          <head>
            <meta charset="utf-8">
            <style>
              body {
                margin: 0;
                padding: 0;
                overflow: hidden;
              }
            </style>
          </head>
          <body>
            <script type="text/javascript" src="https://www.mgstage.com/afscript/superch/728_90/N2G56Q3UYEPYWXP7P8PKPRIDC3/"></script>
          </body>
        </html>
      `)
      iframeDoc.close()
    }
  }, [mounted])

  return (
    <div className="flex justify-center my-8">
      <div className="text-center mb-2">
        <span className="text-xs text-elegant-text-dark font-medium bg-elegant-bg-lighter px-3 py-1 rounded-full border border-elegant-border">
          PR・アフィリエイト広告
        </span>
      </div>
      <iframe
        ref={iframeRef}
        width="728"
        height="90"
        frameBorder="0"
        scrolling="no"
        style={{
          border: 'none',
          overflow: 'hidden'
        }}
        title="MGStage Banner Ad"
      />
    </div>
  )
}

