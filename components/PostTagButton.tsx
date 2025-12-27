'use client'

import { useRouter } from 'next/navigation'

interface PostTagButtonProps {
  tag: string
  selectedTag?: string
  selectedYear?: string
  isSelected?: boolean
}

export default function PostTagButton({ 
  tag, 
  selectedTag, 
  selectedYear,
  isSelected 
}: PostTagButtonProps) {
  const router = useRouter()
  const tagStr = String(tag).trim()
  const isTagSelected = isSelected ?? (selectedTag === tagStr)

  const href = isTagSelected
    ? selectedYear ? `/?year=${selectedYear}` : '/'
    : selectedYear
    ? `/?tag=${encodeURIComponent(tagStr)}&year=${selectedYear}`
    : `/?tag=${encodeURIComponent(tagStr)}`

  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.stopPropagation()
    e.preventDefault()
    router.push(href)
  }

  return (
    <button
      type="button"
      onClick={handleClick}
      className={`px-2 py-0.5 rounded-full text-xs transition-colors ${
        isTagSelected
          ? 'bg-yellow-600 text-neutral-950 font-semibold'
          : 'bg-neutral-800 text-neutral-400 border border-neutral-700 hover:border-yellow-500 hover:text-yellow-500'
      }`}
    >
      {tagStr}
    </button>
  )
}

