'use client'

import { useRouter, useSearchParams } from 'next/navigation'

interface YearSelectProps {
  years: number[]
}

export default function YearSelect({ years }: YearSelectProps) {
  const router = useRouter()
  const searchParams = useSearchParams()
  const selectedYear = searchParams.get('year') || ''
  const selectedTag = searchParams.get('tag')

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const year = e.target.value
    const params = new URLSearchParams()
    
    if (year) {
      params.set('year', year)
    }
    if (selectedTag) {
      params.set('tag', selectedTag)
    }
    
    const queryString = params.toString()
    router.push(queryString ? `/?${queryString}` : '/')
  }

  return (
    <select
      value={selectedYear}
      onChange={handleChange}
      className="w-full md:w-auto px-4 py-2 bg-neutral-900 border border-neutral-800 rounded-lg text-neutral-200 focus:outline-none focus:border-yellow-500 focus:ring-1 focus:ring-yellow-500 cursor-pointer"
    >
      <option value="">すべての年代</option>
      {years.map((year) => (
        <option key={year} value={year}>
          {year}年
        </option>
      ))}
    </select>
  )
}

