'use client'

import IframeAd from './IframeAd'

export default function MgsAd300x250() {
  // MGS広告のスクリプトコード
  const adCode = '<script type="text/javascript" src="https://www.mgstage.com/afscript/superch/300_250/N2G56Q3UYEPYWXP7P8PKPRIDC3/"></script>'
  

  return (
    <div className="bg-gradient-to-br from-[var(--elegant-bg-light)] to-[var(--elegant-bg-lighter)] rounded-xl p-4 border border-[var(--elegant-border)] shadow-lg">
      {/* PR表示 */}
      <div className="text-center mb-3">
        <span className="text-xs text-[var(--elegant-text-dark)] font-medium bg-[var(--elegant-bg)] px-3 py-1 rounded-full border border-[var(--elegant-border)]">
          PR・アフィリエイト広告
        </span>
      </div>
      
      {/* 広告コンテナ */}
      <div className="w-full bg-[var(--elegant-bg)] rounded-lg border border-[var(--elegant-border)] overflow-hidden">
        <IframeAd 
          adCode={adCode}
          width={300}
          height={250}
        />
      </div>
    </div>
  )
}