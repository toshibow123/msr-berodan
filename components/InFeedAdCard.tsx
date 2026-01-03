'use client'

import FanzaSubscriptionPromo from './FanzaSubscriptionPromo'

interface InFeedAdCardProps {
  contentId?: string
  affiliateLink?: string
}

/**
 * インフィード広告カードコンポーネント
 * 作品フィードの中に自然に配置される広告
 */
export default function InFeedAdCard({ contentId, affiliateLink }: InFeedAdCardProps) {
  return (
    <div className="my-8 rounded-2xl overflow-hidden border-2 border-amber-500/40 bg-gradient-to-b from-gray-950 to-black shadow-2xl">
      {/* PR表示 */}
      <div className="text-center pt-4 pb-2">
        <span className="text-xs text-amber-400/80 font-medium bg-amber-500/10 px-4 py-1.5 rounded-full border border-amber-500/30">
          PR・アフィリエイト広告
        </span>
      </div>
      
      {/* 広告コンテンツ */}
      <div className="px-4 pb-4">
        <FanzaSubscriptionPromo 
          singleAffiliateUrl={affiliateLink}
          contentId={contentId}
        />
      </div>
    </div>
  )
}

