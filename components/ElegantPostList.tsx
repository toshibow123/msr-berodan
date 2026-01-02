import VideoCard from './VideoCard';
import { PostData } from '@/lib/posts';

interface ElegantPostListProps {
  posts: PostData[];
  title?: string;
  subtitle?: string;
}

export default function ElegantPostList({ posts, title, subtitle }: ElegantPostListProps) {
  return (
    <section>
      {/* セクションヘッダー */}
      {(title || subtitle) && (
        <div className="text-center mb-12">
          {title && (
            <h2 className="text-4xl font-serif-jp text-elegant-wine mb-4 tracking-wider">
              {title}
            </h2>
          )}
          {subtitle && (
            <p className="text-elegant-text-light tracking-wide">
              {subtitle}
            </p>
          )}
        </div>
      )}

      {/* 記事グリッド（モバイル2列、PC4列） */}
      {posts.length > 0 ? (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6">
          {posts.map((post) => (
            <VideoCard
              key={post.slug}
              post={post}
            />
          ))}
        </div>
      ) : (
        <div className="text-center py-16">
          <p className="text-elegant-text-dark text-lg">記事がまだありません</p>
        </div>
      )}
    </section>
  );
}

