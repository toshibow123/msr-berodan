'use client'

interface AffiliateAdMockProps {
  position: 'top' | 'inline' | 'bottom' | 'sidebar' | 'sticky'
  size?: '300x250' | '728x90' | 'responsive'
}

export default function AffiliateAdMock({ position, size = 'responsive' }: AffiliateAdMockProps) {
  // サイズに応じたクラス
  const sizeClasses = {
    '300x250': 'w-[300px] h-[250px]',
    '728x90': 'w-[728px] h-[90px]',
    'responsive': 'w-full max-w-[300px] h-[250px] md:max-w-[728px] md:h-[90px]'
  }

  // 位置に応じたスタイル
  const positionStyles = {
    top: 'my-8',
    inline: 'my-12',
    bottom: 'my-12',
    sidebar: 'mb-6',
    sticky: 'fixed top-0 left-0 right-0 z-40 lg:hidden'
  }

  return (
    <div className={`${positionStyles[position]} ${position === 'sticky' ? 'bg-elegant-bg-light border-t-2 border-elegant-wine/30 p-4 shadow-lg' : ''}`}>
      {/* PR表示 */}
      <div className="text-center mb-2">
        <span className="text-xs text-elegant-text-dark font-medium bg-elegant-bg-lighter px-3 py-1 rounded-full border border-elegant-border">
          PR・アフィリエイト広告
        </span>
      </div>
      
      {/* 広告モック */}
      <div className={`
        ${sizeClasses[size]}
        bg-gradient-to-br from-elegant-wine/20 to-elegant-wine-dark/20
        border-2 border-elegant-wine/40
        rounded-lg
        flex items-center justify-center
        ${position === 'sticky' ? 'w-full' : 'mx-auto'}
      `}>
        <div className="text-center p-4">
          <div className="text-elegant-wine font-serif-jp font-bold text-lg mb-2">
            {position === 'top' && '広告位置: 記事上部'}
            {position === 'inline' && '広告位置: 本文内'}
            {position === 'bottom' && '広告位置: 記事末尾'}
            {position === 'sidebar' && '広告位置: サイドバー'}
            {position === 'sticky' && '広告位置: 追従バナー（モバイル）'}
          </div>
          <div className="text-elegant-text-light text-sm">
            {size === '300x250' && '300×250'}
            {size === '728x90' && '728×90'}
            {size === 'responsive' && 'レスポンシブ'}
          </div>
        </div>
      </div>
    </div>
  )
}

