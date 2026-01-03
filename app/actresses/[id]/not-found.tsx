import Link from 'next/link'

export default function NotFound() {
  return (
    <div className="min-h-screen bg-black text-white flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4 text-amber-400">女優が見つかりません</h1>
        <p className="text-gray-400 mb-8">指定された女優のページは存在しません。</p>
        <Link
          href="/"
          className="inline-flex items-center gap-2 px-6 py-3 bg-amber-600 hover:bg-amber-700 text-white font-semibold rounded-xl transition-all"
        >
          <span>←</span>
          <span>トップページに戻る</span>
        </Link>
      </div>
    </div>
  )
}

