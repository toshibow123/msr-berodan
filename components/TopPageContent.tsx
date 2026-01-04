'use client'

import { useState, useMemo, useEffect } from 'react'
import { useSearchParams } from 'next/navigation'
import Link from 'next/link'
import Image from 'next/image'
import { ActressData } from '@/lib/actresses'
import Sidebar from '@/components/Sidebar'

interface TopPageContentProps {
  initialActresses: ActressData[]
}

export default function TopPageContent({ initialActresses }: TopPageContentProps) {
  const searchParams = useSearchParams()
  const [displayCount, setDisplayCount] = useState(12) // 初期表示数（4×3）

  // フィルタリングとソート
  const filteredAndSortedActresses = useMemo(() => {
    let filtered = [...initialActresses]
    
    // 検索フィルター
    const searchQuery = searchParams.get('search')
    if (searchQuery) {
      filtered = filtered.filter(actress => 
        actress.name.toLowerCase().includes(searchQuery.toLowerCase())
      )
    }
    
    // カテゴリーフィルター（作品数）
    const category = searchParams.get('category')
    if (category && category !== 'all') {
      switch (category) {
        case '10plus':
          filtered = filtered.filter(actress => actress.works.length >= 10)
          break
        case '5plus':
          filtered = filtered.filter(actress => actress.works.length >= 5)
          break
        case '3plus':
          filtered = filtered.filter(actress => actress.works.length >= 3)
          break
      }
    }
    
    // ソート
    const sortBy = searchParams.get('sort') || 'works'
    if (sortBy === 'name') {
      filtered.sort((a, b) => a.name.localeCompare(b.name, 'ja'))
    } else {
      filtered.sort((a, b) => b.works.length - a.works.length)
    }
    
    return filtered
  }, [initialActresses, searchParams])

  // 表示する女優リスト（ページネーション）
  const displayedActresses = filteredAndSortedActresses.slice(0, displayCount)
  const hasMore = displayCount < filteredAndSortedActresses.length
  const remainingCount = filteredAndSortedActresses.length - displayCount

  // もっと見るボタンのハンドラ
  const handleLoadMore = () => {
    setDisplayCount(prev => Math.min(prev + 12, filteredAndSortedActresses.length))
  }

  // フィルター変更時に表示数をリセット
  const resetDisplayCount = () => {
    setDisplayCount(12)
  }

  // URLパラメータが変更されたときに表示数をリセット
  useEffect(() => {
    setDisplayCount(12)
  }, [searchParams])

  return (
    <div className="min-h-screen" style={{ backgroundColor: 'var(--elegant-bg)', color: 'var(--elegant-text)' }}>
      {/* ヒーローセクション */}
      <section className="bg-gradient-to-b from-[var(--elegant-bg-light)] via-[var(--elegant-bg)] to-[var(--elegant-bg)] border-b-2 border-[var(--elegant-wine)]/30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24 text-center">
          <h1 className="text-4xl md:text-6xl font-bold font-serif tracking-wider mb-6" style={{ color: 'var(--elegant-wine)' }}>
            女優別作品カタログ
          </h1>
          <p className="text-lg md:text-xl max-w-2xl mx-auto leading-relaxed" style={{ color: 'var(--elegant-text-light)' }}>
            お気に入りの女優を見つけて、作品を探索してください。
            <br className="hidden md:block" />
            上質な大人の時間をお楽しみください。
          </p>
        </div>
      </section>

      {/* メインコンテンツ */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* サイドバー */}
          <Sidebar actresses={initialActresses} onFilterChange={resetDisplayCount} />
          
          {/* 女優一覧 */}
          <main className="flex-1">
            {/* 統計情報 */}
            <div className="mb-8 text-center lg:text-left">
              <p style={{ color: 'var(--elegant-text-light)' }} className="text-sm md:text-base">
                表示中: <span style={{ color: 'var(--elegant-wine)' }} className="font-bold text-lg">{displayedActresses.length}人</span>
                {filteredAndSortedActresses.length > displayedActresses.length && (
                  <span className="ml-2">（{filteredAndSortedActresses.length}人中）</span>
                )}
                {filteredAndSortedActresses.length !== initialActresses.length && (
                  <span className="ml-2 text-xs">フィルター適用中</span>
                )}
              </p>
            </div>

            {/* 女優グリッド */}
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 xl:grid-cols-4 gap-4 md:gap-6">
              {displayedActresses.map((actress) => (
                <Link
                  key={actress.id}
                  href={`/actresses/${actress.id}`}
                  className="group relative rounded-xl overflow-hidden border-2 border-transparent transition-all duration-300 hover:scale-105"
                  style={{ 
                    background: 'linear-gradient(to bottom, var(--elegant-bg-light), var(--elegant-bg))',
                    borderColor: 'transparent'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.borderColor = 'var(--elegant-wine)'
                    e.currentTarget.style.boxShadow = '0 25px 50px -12px rgba(139, 34, 82, 0.25)'
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.borderColor = 'transparent'
                    e.currentTarget.style.boxShadow = 'none'
                  }}
                >
                  {/* プロフィール画像 - 縦長ポスターサイズに統一 */}
                  <div className="relative aspect-[2/3] overflow-hidden" style={{ backgroundColor: 'var(--elegant-bg-light)' }}>
                    {actress.image ? (
                      <Image
                        src={actress.image}
                        alt={actress.name}
                        fill
                        className="object-cover object-center transition-transform duration-300 group-hover:scale-105"
                        sizes="(max-width: 640px) 50vw, (max-width: 1024px) 33vw, (max-width: 1280px) 25vw, 20vw"
                      />
                    ) : (
                      <div className="w-full h-full bg-gradient-to-br flex items-center justify-center" style={{ background: 'linear-gradient(to bottom right, var(--elegant-bg-light), var(--elegant-bg-lighter))' }}>
                        <span style={{ color: 'var(--elegant-text-dark)' }} className="text-xs">画像なし</span>
                      </div>
                    )}

                    {/* オーバーレイ（ホバー時） */}
                    <div className="absolute inset-0 bg-black/70 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col items-center justify-center p-4">
                      <p className="text-white text-sm md:text-base font-bold mb-2 text-center line-clamp-2">
                        {actress.name}
                      </p>
                      <p style={{ color: 'var(--elegant-gold)' }} className="text-xs md:text-sm font-semibold">
                        {actress.works.length}作品
                      </p>
                    </div>
                  </div>

                  {/* 女優名と作品数（下部） - グラデーション背景で読みやすく */}
                  <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black via-black/90 to-transparent p-3 z-10">
                    <p className="text-white text-xs md:text-sm font-semibold truncate mb-1 drop-shadow-lg">
                      {actress.name}
                    </p>
                    <p style={{ color: 'var(--elegant-gold)' }} className="text-xs font-medium drop-shadow-lg">
                      {actress.works.length}作品
                    </p>
                  </div>

                  {/* 作品数バッジ（左上） */}
                  <div className="absolute top-2 left-2 text-white text-xs font-bold px-2 py-1 rounded-full backdrop-blur-sm z-10" style={{ backgroundColor: 'var(--elegant-wine)' }}>
                    {actress.works.length}
                  </div>
                </Link>
              ))}
            </div>

            {/* もっと見るボタン */}
            {hasMore && (
              <div className="mt-12 text-center">
                <button
                  onClick={handleLoadMore}
                  className="px-8 py-4 bg-gradient-to-r from-elegant-wine via-elegant-wine-light to-elegant-wine hover:from-elegant-wine-dark hover:via-elegant-wine hover:to-elegant-wine-dark text-white font-semibold rounded-xl transition-all shadow-lg hover:shadow-xl border border-elegant-wine/30 hover:border-elegant-wine/50"
                >
                  もっと見る
                  <span className="ml-2 text-elegant-text-light">
                    （残り{remainingCount}人）
                  </span>
                </button>
              </div>
            )}

            {/* 空の状態 */}
            {filteredAndSortedActresses.length === 0 && (
              <div className="text-center py-24">
                <p style={{ color: 'var(--elegant-text-light)' }} className="text-lg">
                  {initialActresses.length === 0 ? '女優データが見つかりませんでした。' : '検索条件に一致する女優が見つかりませんでした。'}
                </p>
              </div>
            )}

            {/* 全件表示完了メッセージ */}
            {!hasMore && filteredAndSortedActresses.length > 12 && (
              <div className="mt-12 text-center">
                <p style={{ color: 'var(--elegant-text-dark)' }} className="text-sm">
                  全{filteredAndSortedActresses.length}人を表示しました
                </p>
              </div>
            )}
          </main>
        </div>
      </div>

      {/* フッター情報 */}
      <footer className="border-t mt-16 py-8" style={{ borderColor: 'var(--elegant-border)' }}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p style={{ color: 'var(--elegant-text-dark)' }} className="text-sm">
            &copy; 2025 艶めく物語. All rights reserved.
          </p>
          <p style={{ color: 'var(--elegant-text-dark)' }} className="text-xs mt-2">
            このサイトは18歳未満の方の閲覧を禁止しています。
          </p>
        </div>
      </footer>
    </div>
  )
}
