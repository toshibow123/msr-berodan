import Link from 'next/link'
import Image from 'next/image'

interface PostNavigationProps {
  prevPost: { slug: string; title: string; image?: string } | null
  nextPost: { slug: string; title: string; image?: string } | null
}

export default function PostNavigation({ prevPost, nextPost }: PostNavigationProps) {
  if (!prevPost && !nextPost) {
    return null
  }

  return (
    <nav className="flex flex-col md:flex-row gap-4 mb-8 md:mb-12">
      {/* 前の記事 */}
      {prevPost ? (
        <Link
          href={`/posts/${prevPost.slug}`}
          className="flex-1 group flex items-center gap-4 p-4 bg-elegant-bg-lighter rounded-lg border border-elegant-border hover:border-elegant-wine transition-all hover:shadow-lg"
        >
          <div className="flex-shrink-0 w-20 h-20 relative overflow-hidden rounded-md">
            {prevPost.image ? (
              <Image
                src={prevPost.image}
                alt={prevPost.title}
                fill
                className="object-cover transition-transform duration-300 group-hover:scale-110"
                sizes="80px"
              />
            ) : (
              <div className="w-full h-full bg-elegant-border flex items-center justify-center">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  className="w-8 h-8 text-elegant-text-light"
                >
                  <rect x="3" y="3" width="18" height="18" rx="2" />
                  <path d="M9 9h6v6H9z" />
                </svg>
              </div>
            )}
          </div>
          <div className="flex-1 min-w-0">
            <div className="text-xs text-elegant-text-light mb-1 font-medium">前の記事</div>
            <div className="text-sm font-serif-jp text-elegant-text group-hover:text-elegant-wine transition-colors line-clamp-2">
              {prevPost.title}
            </div>
          </div>
          <div className="flex-shrink-0">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="w-5 h-5 text-elegant-text-light group-hover:text-elegant-wine transition-colors"
            >
              <path d="M15 18l-6-6 6-6" />
            </svg>
          </div>
        </Link>
      ) : (
        <div className="flex-1" />
      )}

      {/* 次の記事 */}
      {nextPost ? (
        <Link
          href={`/posts/${nextPost.slug}`}
          className="flex-1 group flex items-center gap-4 p-4 bg-elegant-bg-lighter rounded-lg border border-elegant-border hover:border-elegant-wine transition-all hover:shadow-lg"
        >
          <div className="flex-shrink-0">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="w-5 h-5 text-elegant-text-light group-hover:text-elegant-wine transition-colors"
            >
              <path d="M9 18l6-6-6-6" />
            </svg>
          </div>
          <div className="flex-1 min-w-0 text-right">
            <div className="text-xs text-elegant-text-light mb-1 font-medium">次の記事</div>
            <div className="text-sm font-serif-jp text-elegant-text group-hover:text-elegant-wine transition-colors line-clamp-2">
              {nextPost.title}
            </div>
          </div>
          <div className="flex-shrink-0 w-20 h-20 relative overflow-hidden rounded-md">
            {nextPost.image ? (
              <Image
                src={nextPost.image}
                alt={nextPost.title}
                fill
                className="object-cover transition-transform duration-300 group-hover:scale-110"
                sizes="80px"
              />
            ) : (
              <div className="w-full h-full bg-elegant-border flex items-center justify-center">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  className="w-8 h-8 text-elegant-text-light"
                >
                  <rect x="3" y="3" width="18" height="18" rx="2" />
                  <path d="M9 9h6v6H9z" />
                </svg>
              </div>
            )}
          </div>
        </Link>
      ) : (
        <div className="flex-1" />
      )}
    </nav>
  )
}

