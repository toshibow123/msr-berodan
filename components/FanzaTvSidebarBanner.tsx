'use client'

interface FanzaTvSidebarBannerProps {
  affiliateUrl: string
}

export default function FanzaTvSidebarBanner({ affiliateUrl }: FanzaTvSidebarBannerProps) {
  return (
    <div className="bg-gradient-to-br from-[var(--elegant-wine)] via-[var(--elegant-wine-dark)] to-[var(--elegant-wine)] rounded-xl p-6 border border-[var(--elegant-wine)]/50 shadow-2xl">
      <div className="text-center space-y-4">
        <div className="text-white text-2xl font-bold tracking-wider font-serif">
          FANZA TV
        </div>
        <div className="text-[var(--elegant-text-light)] text-sm leading-relaxed">
          月額見放題で<br />
          人気作品を無制限視聴
        </div>
        <div className="text-xl font-bold text-[var(--elegant-champagne)] mb-2">
          初回 14日間無料
        </div>
        <a
          href={affiliateUrl}
          target="_blank"
          rel="noopener noreferrer sponsored"
          className="block w-full bg-[var(--elegant-wine-dark)] hover:bg-[var(--elegant-wine)] text-white font-bold py-3 px-4 rounded-lg transition-all duration-300 hover:scale-105 shadow-lg border border-[var(--elegant-wine)]/30"
        >
          今すぐ無料で試す
        </a>
        <div className="text-[var(--elegant-text-dark)] text-xs">
          ※18歳未満利用禁止
        </div>
      </div>
    </div>
  )
}