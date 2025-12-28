'use client'

import Link from 'next/link'
import { useSearchParams } from 'next/navigation'

interface TagListProps {
  tags: { tag: string; count: number }[]
}

export default function TagList({ tags }: TagListProps) {
  const searchParams = useSearchParams()
  const selectedTag = searchParams.get('tag')?.trim()
  const selectedYear = searchParams.get('year')

  return (
    <div className="flex flex-wrap gap-2">
      {tags.map(({ tag, count }) => {
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
  )
}

