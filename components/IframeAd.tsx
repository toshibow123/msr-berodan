'use client'

import React, { useEffect, useRef } from 'react'

interface IframeAdProps {
  adCode: string
  width?: number
  height?: number
}

export default function IframeAd({ adCode, width = 300, height = 250 }: IframeAdProps) {
  const iframeRef = useRef<HTMLIFrameElement>(null)

  useEffect(() => {
    const iframe = iframeRef.current
    if (!iframe) return

    const doc = iframe.contentDocument || iframe.contentWindow?.document
    if (!doc) return

    // 一度中身をリセットして、強制的に書き込む
    doc.open()
    doc.write(`
      <html>
        <head>
          <base target="_blank" />
          <style>body { margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; background-color: transparent; }</style>
        </head>
        <body>
          ${adCode}
        </body>
      </html>
    `)
    doc.close()
  }, [adCode])

  return (
    <div style={{ width, height }} className="overflow-hidden bg-transparent">
      <iframe
        ref={iframeRef}
        width={width}
        height={height}
        scrolling="no"
        frameBorder="0"
        style={{ border: 'none', overflow: 'hidden' }}
        title="Advertisement"
      />
    </div>
  )
}