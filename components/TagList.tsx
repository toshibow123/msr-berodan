'use client'

import Link from 'next/link'
import { useSearchParams } from 'next/navigation'
import { useState } from 'react'

interface TagListProps {
  tags: { tag: string; count: number }[]
}

export default function TagList({ tags }: TagListProps) {
  const searchParams = useSearchParams()
  const selectedTag = searchParams.get('tag')?.trim()
  const selectedYear = searchParams.get('year')
  const [showAll, setShowAll] = useState(false)

  // 最初の10個と残りを分ける
  const visibleTags = tags.slice(0, 10)
  const hiddenTags = tags.slice(10)
  const displayTags = showAll ? tags : visibleTags

  return (
    <div>
      <div className="flex flex-wrap gap-2">
        {displayTags.map(({ tag, count }) => {
          const isSelected = selectedTag === tag
          return (
            <Link
              key={tag}
              href={
                isSelected
                  ? selectedYear ? `/?year=${selectedYear}` : '/'
                  : selectedYear
                  ? `/?tag=${encodeURIComponent(tag)}&year=${selectedYear}`
                  : `/?tag=${encodeURIComponent(tag)}`
              }
              className={`px-3 py-1.5 rounded-full text-sm transition-colors ${
                isSelected
                  ? 'bg-yellow-600 text-neutral-950 font-semibold border border-yellow-500'
                  : 'bg-neutral-800 text-neutral-300 border border-neutral-700 hover:border-yellow-500 hover:text-yellow-500'
              }`}
            >
              {tag} <span className={isSelected ? 'text-neutral-700' : 'text-neutral-500'}>({count})</span>
            </Link>
          )
        })}
      </div>
      {hiddenTags.length > 0 && (
        <button
          onClick={() => setShowAll(!showAll)}
          className="mt-3 text-sm text-yellow-500 hover:text-yellow-400 transition-colors"
        >
          {showAll ? '▲ 折りたたむ' : `▼ もっと見る (${hiddenTags.length}件)`}
        </button>
      )}
    </div>
  )
}

