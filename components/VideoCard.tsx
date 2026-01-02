import Link from 'next/link'
import Image from 'next/image'
import { PostData } from '@/lib/posts'

interface VideoCardProps {
  post: PostData
}

export default function VideoCard({ post }: VideoCardProps) {
  // 画質バッジを判定（4K、ハイビジョンなどのタグから）
  const getQualityBadge = () => {
    const tags = post.tags || []
    const title = post.title || ''
    const allText = [...tags, title].join(' ')
    
    if (allText.includes('4K') || allText.includes('4k')) {
      return { label: '4K', color: 'bg-elegant-wine' }
    }
    if (allText.includes('ハイビジョン') || allText.includes('HD')) {
      return { label: 'HD', color: 'bg-elegant-gold' }
    }
    if (allText.includes('フルHD') || allText.includes('FHD')) {
      return { label: 'FHD', color: 'bg-elegant-wine-light' }
    }
    return null
  }

  const qualityBadge = getQualityBadge()

  return (
    <Link 
      href={`/posts/${post.slug}`}
      className="group block"
    >
      <div className="bg-elegant-bg-light rounded-lg overflow-hidden border border-elegant-border hover:border-elegant-wine/50 transition-all duration-300 hover:shadow-lg w-full">
        {/* サムネイルエリア（16:9） */}
        <div className="relative w-full aspect-video overflow-hidden bg-elegant-bg-lighter">
          {post.image ? (
            <Image
              src={post.image}
              alt={post.title}
              fill
              className="object-cover transition-all duration-300 group-hover:scale-110 group-hover:brightness-110"
              sizes="(max-width: 768px) 50vw, 25vw"
            />
          ) : (
            <div className="w-full h-full bg-elegant-bg-lighter flex items-center justify-center">
              <span className="text-elegant-text-dark text-sm">画像なし</span>
            </div>
          )}
          
          {/* 画質バッジ */}
          {qualityBadge && (
            <div className={`absolute top-2 right-2 ${qualityBadge.color} text-white text-xs font-bold px-2 py-1 rounded backdrop-blur-sm z-10`}>
              {qualityBadge.label}
            </div>
          )}
          
          {/* 評価バッジ（左上） */}
          {post.rating && (
            <div className="absolute top-2 left-2 bg-elegant-gold/90 text-elegant-bg px-2 py-1 rounded-full backdrop-blur-sm z-10">
              <span className="text-xs font-bold">★ {post.rating}</span>
            </div>
          )}
        </div>

        {/* コンテンツエリア */}
        <div className="p-3">
          {/* タイトル（2行で省略） */}
          <h3 className="text-sm font-medium text-elegant-text group-hover:text-elegant-wine transition-colors duration-300 line-clamp-2 mb-2 leading-snug">
            {post.title}
          </h3>

          {/* メタ情報（日付） */}
          {post.date && (
            <time className="text-xs text-elegant-text-dark block mb-1">
              {new Date(post.date).toLocaleDateString('ja-JP', {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
              })}
            </time>
          )}

          {/* ジャンルタグ（小さく表示） */}
          {post.genre && post.genre.length > 0 && (
            <div className="flex flex-wrap gap-1 mt-2">
              {post.genre.slice(0, 2).map((g) => (
                <span
                  key={g}
                  className="text-xs px-2 py-0.5 bg-elegant-wine/20 text-elegant-wine rounded-full"
                >
                  {g}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </Link>
  )
}

