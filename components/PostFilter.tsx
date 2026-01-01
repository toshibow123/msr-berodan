'use client';

import { useState, useEffect } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import ElegantPostList from './ElegantPostList';
import { PostData } from '@/lib/posts';

interface PostFilterProps {
  initialPosts: PostData[];
}

export default function PostFilter({ initialPosts }: PostFilterProps) {
  const searchParams = useSearchParams();
  const [posts, setPosts] = useState<PostData[]>(initialPosts);
  const [sortBy, setSortBy] = useState<'date' | 'date-oldest' | 'rating' | 'title'>('date');
  const [showAll, setShowAll] = useState(false);

  useEffect(() => {
    setPosts(initialPosts);
    setShowAll(false); // フィルターが変わったらリセット
  }, [initialPosts]);

  // ソート処理
  const sortedPosts = [...posts].sort((a, b) => {
    switch (sortBy) {
      case 'date':
        return new Date(b.date).getTime() - new Date(a.date).getTime();
      case 'date-oldest':
        return new Date(a.date).getTime() - new Date(b.date).getTime();
      case 'rating':
        const ratingA = a.rating || 0;
        const ratingB = b.rating || 0;
        return ratingB - ratingA;
      case 'title':
        return a.title.localeCompare(b.title, 'ja');
      default:
        return 0;
    }
  });

  const category = searchParams.get('category') || 'all';
  const tag = searchParams.get('tag');
  const search = searchParams.get('search');

  // フィルター結果の表示
  const filterInfo = [];
  if (category !== 'all') {
    const categoryNames: Record<string, string> = {
      mature: '熟女',
      married: '人妻',
      drama: 'ドラマ',
      ntr: 'NTR(ネトラレ)',
      nakadashi: '中出し',
    };
    filterInfo.push(categoryNames[category] || category);
  }
  if (tag) {
    filterInfo.push(`#${tag}`);
  }
  if (search) {
    filterInfo.push(`検索: "${search}"`);
  }

  const router = useRouter();
  
  const handleResetFilters = () => {
    router.push('/');
  };

  return (
    <div>
      {/* フィルター情報とソート */}
      <div className="mb-6 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div className="flex-1">
          {filterInfo.length > 0 ? (
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-elegant-text-light">フィルター:</span>
              {filterInfo.map((info, idx) => (
                <span
                  key={idx}
                  className="px-3 py-1 bg-elegant-wine/20 text-elegant-wine rounded-full text-sm"
                >
                  {info}
                </span>
              ))}
              <span className="text-elegant-text-dark text-sm">
                ({sortedPosts.length}件)
              </span>
              <button
                onClick={handleResetFilters}
                className="ml-2 px-3 py-1 text-sm text-elegant-text-light hover:text-elegant-wine border border-elegant-border rounded-full transition-colors hover:border-elegant-wine"
              >
                ✕ リセット
              </button>
            </div>
          ) : (
            <p className="text-elegant-text-light">
              全{sortedPosts.length}件の記事
            </p>
          )}
        </div>

        {/* ソート選択 */}
        <div className="flex items-center gap-2">
          <label className="text-sm text-elegant-text-light">並び替え:</label>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as 'date' | 'date-oldest' | 'rating' | 'title')}
            className="px-3 py-1.5 bg-elegant-bg-light border border-elegant-border rounded text-elegant-text text-sm focus:outline-none focus:border-elegant-wine"
          >
            <option value="date">新しい順</option>
            <option value="date-oldest">古い順</option>
            <option value="rating">評価順</option>
            <option value="title">タイトル順</option>
          </select>
        </div>
      </div>

      {/* 記事一覧 */}
      {sortedPosts.length > 0 ? (
        <>
          <ElegantPostList
            posts={filterInfo.length > 0 ? sortedPosts : (showAll ? sortedPosts : sortedPosts.slice(0, 12))}
            title={filterInfo.length > 0 ? undefined : '最新の記事'}
            subtitle={filterInfo.length > 0 ? undefined : '大人の女性の色気と物語性に満ちた作品をご紹介'}
          />
          {/* もっと見るボタン（フィルター未適用かつ12件以上ある場合のみ） */}
          {filterInfo.length === 0 && sortedPosts.length > 12 && !showAll && (
            <div className="text-center mt-12">
              <button
                onClick={() => setShowAll(true)}
                className="px-8 py-4 bg-elegant-wine hover:bg-elegant-wine-light text-white font-serif-jp font-medium rounded-lg transition-all duration-300 shadow-lg hover:shadow-xl border-2 border-elegant-wine/50 hover:border-elegant-wine"
              >
                もっと見る ({sortedPosts.length - 12}件)
              </button>
            </div>
          )}
        </>
      ) : (
        <div className="text-center py-16">
          <p className="text-elegant-text-dark text-lg mb-4">
            該当する記事が見つかりませんでした
          </p>
          <p className="text-elegant-text-dark text-sm">
            フィルターを変更してお探しください
          </p>
        </div>
      )}
    </div>
  );
}

