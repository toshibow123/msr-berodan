import Link from 'next/link';
import Image from 'next/image';

interface ElegantPostCardProps {
  slug: string;
  title: string;
  excerpt: string;
  image: string;
  date: string;
  tags: string[];
  genre?: string[];
  rating?: number;
  storyScore?: number;
  actingScore?: number;
}

export default function ElegantPostCard({
  slug,
  title,
  excerpt,
  image,
  date,
  tags,
  genre = [],
  rating,
  storyScore,
  actingScore,
}: ElegantPostCardProps) {
  return (
    <article className="article-card group">
      <Link href={`/posts/${slug}`} className="block">
        {/* 画像エリア */}
        <div className="relative overflow-hidden h-64 bg-elegant-bg-lighter">
          <Image
            src={image}
            alt={title}
            fill
            className="object-cover transition-transform duration-500 group-hover:scale-105"
            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
          />
          
          {/* 評価（画像上、左側） */}
          {rating && (
            <div className="absolute top-4 left-4 bg-elegant-gold/90 text-elegant-bg px-3 py-1 rounded-full backdrop-blur-sm z-10">
              <span className="text-sm font-bold">★ {rating}</span>
            </div>
          )}
          
          {/* ジャンルタグ（画像上、評価の下） */}
          {genre.length > 0 && (
            <div className={`absolute ${rating ? 'top-16' : 'top-4'} left-4 flex gap-2 z-10`}>
              {genre.slice(0, 2).map((g) => (
                <span
                  key={g}
                  className="px-3 py-1 bg-elegant-wine/90 text-white text-xs font-medium rounded-full backdrop-blur-sm"
                >
                  {g}
                </span>
              ))}
            </div>
          )}
        </div>

        {/* コンテンツエリア */}
        <div className="p-6">
          {/* タイトル */}
          <h3 className="text-2xl font-serif-jp text-elegant-wine mb-3 group-hover:text-elegant-wine-light transition-colors duration-300 leading-relaxed line-clamp-2">
            {title}
          </h3>

          {/* 日付 */}
          <time className="text-xs text-elegant-text-dark tracking-wider block mb-4">
            {new Date(date).toLocaleDateString('ja-JP', {
              year: 'numeric',
              month: 'long',
              day: 'numeric',
            })}
          </time>

          {/* 抜粋 */}
          <p className="text-elegant-text-light leading-relaxed mb-4 line-clamp-3">
            {excerpt}
          </p>

          {/* スコア表示 */}
          {(storyScore || actingScore) && (
            <div className="flex gap-4 mb-4 text-xs text-elegant-text-light">
              {storyScore && (
                <div className="flex items-center gap-1">
                  <span className="font-medium">物語</span>
                  <span className="text-elegant-wine font-bold">{storyScore}</span>
                </div>
              )}
              {actingScore && (
                <div className="flex items-center gap-1">
                  <span className="font-medium">演技</span>
                  <span className="text-elegant-wine font-bold">{actingScore}</span>
                </div>
              )}
            </div>
          )}

          {/* タグ */}
          <div className="flex flex-wrap gap-2">
            {tags.slice(0, 4).map((tag) => (
              <span
                key={tag}
                className="text-xs text-elegant-text-dark px-2 py-1 bg-elegant-bg-lighter rounded border border-elegant-border"
              >
                #{tag}
              </span>
            ))}
          </div>

          {/* 続きを読む */}
          <div className="mt-4 pt-4 border-t border-elegant-border">
            <span className="text-elegant-wine font-medium text-sm group-hover:underline inline-flex items-center gap-1">
              記事を読む
              <svg className="w-4 h-4 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </span>
          </div>
        </div>
      </Link>
    </article>
  );
}

