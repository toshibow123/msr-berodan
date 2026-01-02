'use client';

import { useSearchParams } from 'next/navigation';
import { PostData } from '@/lib/posts';
import PostFilter from './PostFilter';

interface FilteredPostListProps {
  allPosts: PostData[];
}

export default function FilteredPostList({ allPosts }: FilteredPostListProps) {
  const searchParams = useSearchParams();
  
  // 現在の日付を取得（クライアントサイド）
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  
  // 未来の日付の記事も表示する（すべての記事を表示）
  let filteredPosts = allPosts.filter((post) => {
    if (!post.date) return false
    // すべての記事を表示（未来の日付も含む）
    return true
  })

  // カテゴリーフィルター
  const category = searchParams.get('category');
  if (category && category !== 'all') {
    filteredPosts = filteredPosts.filter(post => {
      if (category === 'nakadashi') {
        // 中出しフィルター: tagsに「中出し」が含まれているかチェック
        const tags = post.tags || [];
        return tags.some(t => String(t).trim() === '中出し');
      }
      
      const genres = post.genre || [];
      const categoryMap: Record<string, string[]> = {
        mature: ['熟女', '三十路', '四十路', '五十路'],
        married: ['人妻', '主婦', '奥さん'],
        drama: ['ドラマ', 'ストーリー', '不倫', '近親相姦'],
        ntr: ['NTR', 'ネトラレ', '寝取', '寝取られ'],
      };
      const keywords = categoryMap[category] || [];
      return genres.some(genre => keywords.some(keyword => genre.includes(keyword)));
    });
  }

  // タグフィルター
  const tag = searchParams.get('tag');
  if (tag) {
    filteredPosts = filteredPosts.filter(post => {
      const tags = post.tags || [];
      // 完全一致でチェック（「中出し」など正確に一致する必要がある）
      return tags.some(t => String(t).trim() === tag.trim());
    });
  }

  // 検索フィルター
  const search = searchParams.get('search');
  if (search) {
    const searchLower = search.toLowerCase();
    filteredPosts = filteredPosts.filter(post => {
      const title = post.title?.toLowerCase() || '';
      const excerpt = post.excerpt?.toLowerCase() || '';
      return title.includes(searchLower) || excerpt.includes(searchLower);
    });
  }

  return <PostFilter initialPosts={filteredPosts} />;
}

