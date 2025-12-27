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
    <div className="bg-neutral-900 rounded-lg border border-neutral-800 overflow-hidden">
      {/* 画像ボタンエリア */}
      <Link
        href={affiliateUrl}
        target="_blank"
        rel="noopener noreferrer sponsored"
        className="block w-full active:scale-95 transition-transform"
      >
        <div className="relative w-full aspect-[3/1] bg-neutral-800 flex items-center justify-center">
          {!imageError ? (
            <Image
              src="/images/fanza_tv_btn.png"
              alt="FANZA TV"
              fill
              className="object-contain"
              onError={() => setImageError(true)}
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-yellow-600 to-yellow-500">
              <span className="text-neutral-950 font-bold text-lg">FANZA TV</span>
            </div>
          )}
        </div>
      </Link>

      {/* 訴求テキストエリア */}
      <div className="p-4 bg-neutral-800 border-t-2 border-yellow-600">
        <p className="text-neutral-200 text-sm mb-2 text-center">
          DMMプレミアムなら<strong className="text-yellow-500">追加料金なし</strong>！
        </p>
        <p className="text-center mb-2">
          <span className="text-yellow-500 font-bold text-lg">
            <strong className="text-yellow-500">14日間無料</strong>
          </span>
          <span className="text-neutral-300 mx-1">＆</span>
          <span className="text-yellow-500 font-bold text-lg">
            <strong className="text-yellow-500">550pt</strong>即時付与
          </span>
        </p>
        <p className="text-neutral-400 text-xs text-center">
          登録後すぐに新作も買える！
        </p>
      </div>
    </div>
  )
}

