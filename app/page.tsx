import Link from 'next/link'
import Image from 'next/image'
import { getAllActresses } from '@/lib/actresses'

export default async function Home() {
  const actresses = getAllActresses()

  return (
    <div className="min-h-screen bg-black text-white">
      {/* ヒーローセクション */}
      <section className="bg-gradient-to-b from-gray-900 via-black to-black border-b-2 border-amber-500/30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24 text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-amber-400 mb-6 font-serif tracking-wider">
            女優別作品カタログ
          </h1>
          <p className="text-lg md:text-xl text-gray-300 max-w-2xl mx-auto leading-relaxed">
            作品をクリックすると詳細モーダルが開き、動画再生や詳細情報を確認できます。
            <br className="hidden md:block" />
            没入感のある体験をお楽しみください。
          </p>
        </div>
      </section>

      {/* 女優一覧 */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* 統計情報 */}
        <div className="mb-8 text-center">
          <p className="text-gray-400 text-sm md:text-base">
            登録女優数: <span className="text-amber-400 font-bold text-lg">{actresses.length}人</span>
          </p>
        </div>

        {/* 女優グリッド */}
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4 md:gap-6">
          {actresses.map((actress) => (
            <Link
              key={actress.id}
              href={`/actresses/${actress.id}`}
              className="group relative bg-gradient-to-b from-gray-900 to-black rounded-xl overflow-hidden border-2 border-transparent hover:border-amber-500/50 transition-all duration-300 hover:shadow-2xl hover:shadow-amber-500/20 hover:scale-105"
            >
              {/* プロフィール画像 - 縦長ポスターサイズに統一 */}
              <div className="relative aspect-[2/3] bg-gray-900 overflow-hidden">
                {actress.image ? (
                  <Image
                    src={actress.image}
                    alt={actress.name}
                    fill
                    className="object-cover object-center transition-transform duration-300 group-hover:scale-105"
                    sizes="(max-width: 640px) 50vw, (max-width: 1024px) 33vw, (max-width: 1280px) 20vw, 16vw"
                  />
                ) : (
                  <div className="w-full h-full bg-gradient-to-br from-gray-800 to-gray-900 flex items-center justify-center">
                    <span className="text-gray-500 text-xs">画像なし</span>
                  </div>
                )}

                {/* オーバーレイ（ホバー時） */}
                <div className="absolute inset-0 bg-black/70 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col items-center justify-center p-4">
                  <p className="text-white text-sm md:text-base font-bold mb-2 text-center line-clamp-2">
                    {actress.name}
                  </p>
                  <p className="text-amber-400 text-xs md:text-sm font-semibold">
                    {actress.works.length}作品
                  </p>
                </div>
              </div>

              {/* 女優名と作品数（下部） - グラデーション背景で読みやすく */}
              <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black via-black/90 to-transparent p-3 z-10">
                <p className="text-white text-xs md:text-sm font-semibold truncate mb-1 drop-shadow-lg">
                  {actress.name}
                </p>
                <p className="text-amber-400 text-xs font-medium drop-shadow-lg">
                  {actress.works.length}作品
                </p>
              </div>

              {/* 作品数バッジ（右上） */}
              <div className="absolute top-2 right-2 bg-amber-500/90 text-black text-xs font-bold px-2 py-1 rounded-full backdrop-blur-sm z-10">
                {actress.works.length}
              </div>
            </Link>
          ))}
        </div>

        {/* 空の状態（念のため） */}
        {actresses.length === 0 && (
          <div className="text-center py-24">
            <p className="text-gray-400 text-lg">女優データが見つかりませんでした。</p>
          </div>
        )}
      </main>

      {/* フッター情報 */}
      <footer className="border-t border-gray-800 mt-16 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-gray-500 text-sm">
            &copy; 2025 艶めく物語. All rights reserved.
          </p>
          <p className="text-gray-600 text-xs mt-2">
            このサイトは18歳未満の方の閲覧を禁止しています。
          </p>
        </div>
      </footer>
    </div>
  )
}
