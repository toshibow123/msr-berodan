'use client'

import Image from 'next/image'
import Link from 'next/link'
import { useState } from 'react'

interface FanzaTvSidebarBannerProps {
  affiliateUrl: string
}

export default function FanzaTvSidebarBanner({ affiliateUrl }: FanzaTvSidebarBannerProps) {
  const [imageError, setImageError] = useState(false)

  return (
    <div className="bg-elegant-bg-light rounded-xl border-2 border-elegant-wine/40 overflow-hidden shadow-lg">
      {/* PR表示 */}
      <div className="text-center pt-3 pb-2">
        <span className="text-xs text-elegant-text-dark font-medium bg-elegant-bg-lighter px-3 py-1 rounded-full border border-elegant-border">PR・アフィリエイト広告</span>
      </div>

      {/* 画像ボタンエリア */}
      <Link
        href={affiliateUrl}
        target="_blank"
        rel="noopener noreferrer sponsored"
        className="block w-full active:scale-95 transition-transform"
      >
        <div className="relative w-full aspect-[3/1] bg-elegant-bg-lighter flex items-center justify-center">
          {!imageError ? (
            <Image
              src="/images/fanza_tv_btn.png"
              alt="FANZA TV"
              fill
              className="object-contain"
              onError={() => setImageError(true)}
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-elegant-wine/40 to-elegant-wine-dark/40">
              <span className="text-elegant-wine font-serif-jp font-bold text-lg">FANZA TV</span>
            </div>
          )}
        </div>
      </Link>

      {/* 訴求テキストエリア */}
      <div className="p-4 bg-gradient-to-br from-elegant-wine/20 to-elegant-wine-dark/20 border-t-2 border-elegant-wine/30">
        <p className="text-elegant-text-light text-sm mb-2 text-center">
          DMMプレミアムなら<strong className="text-elegant-wine">追加料金なし</strong>！
        </p>
        <p className="text-center mb-2">
          <span className="text-elegant-wine font-bold text-lg">
            <strong className="text-elegant-wine">14日間無料</strong>
          </span>
          <span className="text-elegant-text-light mx-1">＆</span>
          <span className="text-elegant-wine font-bold text-lg">
            <strong className="text-elegant-wine">550pt</strong>即時付与
          </span>
        </p>
        <p className="text-elegant-text-dark text-xs text-center">
          登録後すぐに新作も買える！
        </p>
      </div>
    </div>
  )
}

