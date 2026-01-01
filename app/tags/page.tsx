import { getAllTags } from '@/lib/posts'
import Link from 'next/link'

export const metadata = {
  title: 'すべてのタグ | Mrs. Adult',
  description: 'すべてのタグ一覧',
}

export default async function TagsPage() {
  const allTags = await getAllTags()

  return (
    <div className="min-h-screen bg-elegant-bg">
      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* ヘッダー */}
        <div className="mb-8">
          <h1 className="text-4xl font-serif-jp text-elegant-wine mb-4">
            すべてのタグ
          </h1>
          <p className="text-elegant-text-light">
            全{allTags.length}件のタグ
          </p>
        </div>

        {/* タグ一覧 */}
        <div className="bg-elegant-bg-light rounded-xl p-6 border border-elegant-border">
          <div className="flex flex-wrap gap-2">
            {allTags.map(({ tag, count }) => (
              <Link
                key={tag}
                href={`/?tag=${encodeURIComponent(tag)}`}
                className="px-4 py-2 rounded-full text-sm transition-colors bg-elegant-bg text-elegant-text-light hover:bg-elegant-wine hover:text-white border border-elegant-border hover:border-elegant-wine"
              >
                #{tag} <span className="text-xs opacity-70">({count})</span>
              </Link>
            ))}
          </div>
        </div>

        {/* 戻るリンク */}
        <div className="mt-8">
          <Link
            href="/"
            className="inline-block px-6 py-3 bg-elegant-wine hover:bg-elegant-wine-light text-white rounded transition-colors"
          >
            ← トップページに戻る
          </Link>
        </div>
      </div>
    </div>
  )
}

