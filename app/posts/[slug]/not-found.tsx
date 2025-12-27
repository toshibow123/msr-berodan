import Link from 'next/link'

export default function NotFound() {
  return (
    <div className="max-w-4xl mx-auto text-center py-16">
      <div className="bg-gray-900 border border-gray-800 rounded-lg p-12">
        <h1 className="text-6xl font-bold text-underground-yellow mb-4">
          404
        </h1>
        <h2 className="text-2xl font-bold text-underground-white mb-6">
          記事が見つかりません
        </h2>
        <p className="text-gray-400 mb-8">
          お探しの記事は存在しないか、削除された可能性があります。
        </p>
        <Link 
          href="/"
          className="inline-block bg-underground-yellow text-black font-bold px-6 py-3 rounded-lg hover:bg-yellow-300 transition-colors"
        >
          記事一覧に戻る
        </Link>
      </div>
    </div>
  )
}

