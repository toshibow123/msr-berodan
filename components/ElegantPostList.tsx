import ElegantPostCard from './ElegantPostCard';
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

      {/* 記事グリッド */}
      {posts.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3 gap-8">
          {posts.map((post) => (
            <ElegantPostCard
              key={post.slug}
              slug={post.slug}
              title={post.title}
              excerpt={post.excerpt || ''}
              image={post.image || ''}
              date={post.date}
              tags={post.tags || []}
              genre={post.genre}
              rating={post.rating}
              storyScore={post.storyScore}
              actingScore={post.actingScore}
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

