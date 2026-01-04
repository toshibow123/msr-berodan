'use client'

import { useState, useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import Link from 'next/link'
import { ActressData } from '@/lib/actresses'
import FanzaTvSidebarBanner from './FanzaTvSidebarBanner'

interface SidebarProps {
  actresses: ActressData[]
  onFilterChange?: () => void
}

export default function Sidebar({ actresses, onFilterChange }: SidebarProps) {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState<string>('all')
  const [sortBy, setSortBy] = useState<string>('works') // works, name

  // URLパラメータから初期値を設定
  useEffect(() => {
    const categoryParam = searchParams.get('category')
    const searchParam = searchParams.get('search')
    const sortParam = searchParams.get('sort')

    if (categoryParam) {
      setSelectedCategory(categoryParam)
    }
    if (searchParam) {
      setSearchQuery(searchParam)
    }
    if (sortParam) {
      setSortBy(sortParam)
    }
  }, [searchParams])

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    const params = new URLSearchParams()
    if (searchQuery) {
      params.set('search', searchQuery)
    }
    if (selectedCategory !== 'all') {
      params.set('category', selectedCategory)
    }
    if (sortBy !== 'works') {
      params.set('sort', sortBy)
    }
    router.push(`/?${params.toString()}`)
    onFilterChange?.() // 表示数をリセット
  }

  const handleCategoryChange = (category: string) => {
    setSelectedCategory(category)
    const params = new URLSearchParams()
    if (searchQuery) {
      params.set('search', searchQuery)
    }
    if (category !== 'all') {
      params.set('category', category)
    }
    if (sortBy !== 'works') {
      params.set('sort', sortBy)
    }
    router.push(`/?${params.toString()}`)
    onFilterChange?.() // 表示数をリセット
  }

  const handleSortChange = (sort: string) => {
    setSortBy(sort)
    const params = new URLSearchParams()
    if (searchQuery) {
      params.set('search', searchQuery)
    }
    if (selectedCategory !== 'all') {
      params.set('category', selectedCategory)
    }
    if (sort !== 'works') {
      params.set('sort', sort)
    }
    router.push(`/?${params.toString()}`)
    onFilterChange?.() // 表示数をリセット
  }

  const clearFilters = () => {
    setSearchQuery('')
    setSelectedCategory('all')
    setSortBy('works')
    router.push('/')
    onFilterChange?.() // 表示数をリセット
  }

  // FANZA TV（DMMプレミアム）のアフィリエイトリンクを生成
  const affiliateId = 'toshichan-002'
  const fanzaTvUrl = `https://al.fanza.co.jp/?lurl=https%3A%2F%2Fpremium.dmm.co.jp%2Fnotice%2Ffanzatv_welcome%2F&af_id=${affiliateId}&ch=link_tool&ch_id=link`

  // 人気女優（作品数上位10名）
  const popularActresses = actresses.slice(0, 10)

  return (
    <aside className="w-full lg:w-80 space-y-6 lg:sticky lg:top-24 lg:h-fit">
      {/* FANZA TV広告 */}
      <FanzaTvSidebarBanner affiliateUrl={fanzaTvUrl} />

      {/* MGS SuperCH 広告（300x250） */}
      <div className="bg-[var(--elegant-bg-light)] rounded-xl p-4 border border-[var(--elegant-border)] shadow-lg">
        <div className="text-center mb-3">
          <span className="text-xs text-[var(--elegant-text-dark)] font-medium bg-[var(--elegant-bg)] px-3 py-1 rounded-full border border-[var(--elegant-border)]">
            PR・MGS SuperCH
          </span>
        </div>
        <iframe
          src="/ads/mgs-300x250.html"
          width={300}
          height={250}
          frameBorder="0"
          scrolling="no"
          style={{
            border: 'none',
            overflow: 'hidden'
          }}
          title="MGS SuperCH広告"
        />
      </div>

      {/* 検索バー */}
      <div className="bg-[var(--elegant-bg-light)] rounded-xl p-6 border border-[var(--elegant-border)]">
        <h3 className="text-lg font-serif text-[var(--elegant-wine)] mb-4">女優検索</h3>
        <div className="space-y-3">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => {
              const newQuery = e.target.value
              setSearchQuery(newQuery)
              
              // リアルタイム検索
              const params = new URLSearchParams()
              if (newQuery) {
                params.set('search', newQuery)
              }
              if (selectedCategory !== 'all') {
                params.set('category', selectedCategory)
              }
              if (sortBy !== 'works') {
                params.set('sort', sortBy)
              }
              
              const newUrl = newQuery || selectedCategory !== 'all' || sortBy !== 'works' 
                ? `/?${params.toString()}` 
                : '/'
              
              router.push(newUrl)
              onFilterChange?.() // 表示数をリセット
            }}
            placeholder="女優名で検索..."
            className="w-full px-4 py-2 bg-[var(--elegant-bg)] rounded border border-[var(--elegant-border)] text-[var(--elegant-text)] placeholder:text-[var(--elegant-text-dark)] focus:outline-none focus:border-[var(--elegant-wine)] transition-colors"
          />
          {searchQuery && (
            <button
              onClick={() => {
                setSearchQuery('')
                const params = new URLSearchParams()
                if (selectedCategory !== 'all') {
                  params.set('category', selectedCategory)
                }
                if (sortBy !== 'works') {
                  params.set('sort', sortBy)
                }
                const newUrl = selectedCategory !== 'all' || sortBy !== 'works' 
                  ? `/?${params.toString()}` 
                  : '/'
                router.push(newUrl)
                onFilterChange?.()
              }}
              className="w-full px-4 py-2 bg-[var(--elegant-bg-lighter)] hover:bg-[var(--elegant-bg)] text-[var(--elegant-text-light)] rounded transition-colors text-sm"
            >
              検索をクリア
            </button>
          )}
        </div>
      </div>

      {/* ソート・フィルター */}
      <div className="bg-[var(--elegant-bg-light)] rounded-xl p-6 border border-[var(--elegant-border)]">
        <h3 className="text-lg font-serif text-[var(--elegant-wine)] mb-4">並び順</h3>
        <div className="space-y-2">
          {[
            { id: 'works', label: '作品数順', icon: '📊' },
            { id: 'name', label: '名前順', icon: '🔤' },
          ].map((sort) => (
            <button
              key={sort.id}
              onClick={() => handleSortChange(sort.id)}
              className={`
                w-full text-left px-4 py-2 rounded transition-colors
                ${
                  sortBy === sort.id
                    ? 'bg-[var(--elegant-wine)] text-white'
                    : 'bg-[var(--elegant-bg)] text-[var(--elegant-text)] hover:bg-[var(--elegant-bg-lighter)]'
                }
              `}
            >
              <span className="mr-2">{sort.icon}</span>
              {sort.label}
            </button>
          ))}
        </div>
      </div>

      {/* 作品数カテゴリー */}
      <div className="bg-[var(--elegant-bg-light)] rounded-xl p-6 border border-[var(--elegant-border)]">
        <h3 className="text-lg font-serif text-[var(--elegant-wine)] mb-4">作品数で絞り込み</h3>
        <div className="space-y-2">
          {[
            { id: 'all', label: 'すべて', icon: '✨' },
            { id: '10plus', label: '10作品以上', icon: '🔥' },
            { id: '5plus', label: '5作品以上', icon: '⭐' },
            { id: '3plus', label: '3作品以上', icon: '💫' },
          ].map((category) => (
            <button
              key={category.id}
              onClick={() => handleCategoryChange(category.id)}
              className={`
                w-full text-left px-4 py-2 rounded transition-colors
                ${
                  selectedCategory === category.id
                    ? 'bg-[var(--elegant-wine)] text-white'
                    : 'bg-[var(--elegant-bg)] text-[var(--elegant-text)] hover:bg-[var(--elegant-bg-lighter)]'
                }
              `}
            >
              <span className="mr-2">{category.icon}</span>
              {category.label}
            </button>
          ))}
        </div>
      </div>

      {/* 人気女優 */}
      <div className="bg-[var(--elegant-bg-light)] rounded-xl p-6 border border-[var(--elegant-border)]">
        <h3 className="text-lg font-serif text-[var(--elegant-wine)] mb-4">人気女優 TOP10</h3>
        <div className="space-y-3">
          {popularActresses.map((actress, index) => (
            <Link
              key={actress.id}
              href={`/actresses/${actress.id}`}
              className="flex items-center gap-3 p-2 rounded hover:bg-[var(--elegant-bg-lighter)] transition-colors group"
            >
              <div className="text-[var(--elegant-gold)] font-bold text-sm w-6 text-center">
                {index + 1}
              </div>
              {actress.image && (
                <div className="relative w-8 h-8 rounded-full overflow-hidden bg-gray-700 flex-shrink-0">
                  <img
                    src={actress.image}
                    alt={actress.name}
                    className="w-full h-full object-cover"
                  />
                </div>
              )}
              <div className="flex-1 min-w-0">
                <div className="text-[var(--elegant-text)] text-sm font-medium truncate group-hover:text-[var(--elegant-wine)] transition-colors">
                  {actress.name}
                </div>
                <div className="text-[var(--elegant-text-dark)] text-xs">
                  {actress.works.length}作品
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>

      {/* 統計情報 */}
      <div className="bg-[var(--elegant-bg-light)] rounded-xl p-6 border border-[var(--elegant-border)]">
        <h3 className="text-lg font-serif text-[var(--elegant-wine)] mb-4">統計</h3>
        <div className="space-y-2 text-sm text-[var(--elegant-text-light)]">
          <div className="flex justify-between">
            <span>登録女優数</span>
            <span className="font-semibold text-[var(--elegant-wine)]">
              {actresses.length}人
            </span>
          </div>
          <div className="flex justify-between">
            <span>総作品数</span>
            <span className="font-semibold text-[var(--elegant-wine)]">
              {actresses.reduce((total, actress) => total + actress.works.length, 0)}作品
            </span>
          </div>
        </div>
      </div>

      {/* MGS SALE広告 */}
      <div className="bg-[var(--elegant-bg-light)] rounded-xl p-4 border border-[var(--elegant-border)] shadow-lg">
        <div className="text-center mb-3">
          <span className="text-xs text-[var(--elegant-text-dark)] font-medium bg-[var(--elegant-bg)] px-3 py-1 rounded-full border border-[var(--elegant-border)]">
            PR・MGS SALE
          </span>
        </div>
        <div className="flex justify-center">
          <iframe
            src="/ads/mgs-sale-234x60.html"
            width={234}
            height={60}
            frameBorder="0"
            scrolling="no"
            style={{
              border: 'none',
              overflow: 'hidden'
            }}
            title="MGS SALE広告"
          />
        </div>
      </div>

      {/* フィルターリセット */}
      {(searchQuery || selectedCategory !== 'all' || sortBy !== 'works') && (
        <button
          onClick={clearFilters}
          className="w-full px-4 py-2 bg-[var(--elegant-bg-lighter)] hover:bg-[var(--elegant-bg)] text-[var(--elegant-text-light)] rounded border border-[var(--elegant-border)] transition-colors"
        >
          フィルターをリセット
        </button>
      )}

      {/* MGS 人妻広告（234x60） */}
      <div className="bg-[var(--elegant-bg-light)] rounded-xl p-4 border border-[var(--elegant-border)] shadow-lg">
        <div className="text-center mb-3">
          <span className="text-xs text-[var(--elegant-text-dark)] font-medium bg-[var(--elegant-bg)] px-3 py-1 rounded-full border border-[var(--elegant-border)]">
            PR・MGS 人妻チャンネル
          </span>
        </div>
        <div className="flex justify-center">
          <iframe
            src="/ads/mgs-hitotuma-234x60.html"
            width={234}
            height={60}
            frameBorder="0"
            scrolling="no"
            style={{
              border: 'none',
              overflow: 'hidden'
            }}
            title="MGS人妻チャンネル広告"
          />
        </div>
      </div>
    </aside>
  )
}