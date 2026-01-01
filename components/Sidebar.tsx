'use client';

import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { PostData } from '@/lib/posts';
import FanzaTvSidebarBanner from './FanzaTvSidebarBanner';
import AffiliateAdMock from './AffiliateAdMock';

interface SidebarProps {
  allPosts: PostData[];
  tags: { tag: string; count: number }[];
}

export default function Sidebar({ allPosts, tags }: SidebarProps) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');

  // URLパラメータから初期値を設定
  useEffect(() => {
    const tagParam = searchParams.get('tag');
    const categoryParam = searchParams.get('category');
    const searchParam = searchParams.get('search');

    if (tagParam) {
      setSelectedTags([tagParam]);
    }
    if (categoryParam) {
      setSelectedCategory(categoryParam);
    }
    if (searchParam) {
      setSearchQuery(searchParam);
    }
  }, [searchParams]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    const params = new URLSearchParams();
    if (searchQuery) {
      params.set('search', searchQuery);
    }
    if (selectedCategory !== 'all') {
      params.set('category', selectedCategory);
    }
    if (selectedTags.length > 0) {
      params.set('tag', selectedTags[0]);
    }
    router.push(`/?${params.toString()}`);
  };

  const handleTagClick = (tag: string) => {
    const newTags = selectedTags.includes(tag)
      ? selectedTags.filter(t => t !== tag)
      : [...selectedTags, tag];
    setSelectedTags(newTags);

    const params = new URLSearchParams();
    if (searchQuery) {
      params.set('search', searchQuery);
    }
    if (selectedCategory !== 'all') {
      params.set('category', selectedCategory);
    }
    if (newTags.length > 0) {
      params.set('tag', newTags[0]);
    }
    router.push(`/?${params.toString()}`);
  };

  const handleCategoryChange = (category: string) => {
    setSelectedCategory(category);
    const params = new URLSearchParams();
    if (searchQuery) {
      params.set('search', searchQuery);
    }
    if (category !== 'all') {
      params.set('category', category);
    }
    if (selectedTags.length > 0) {
      params.set('tag', selectedTags[0]);
    }
    router.push(`/?${params.toString()}`);
  };

  const clearFilters = () => {
    setSearchQuery('');
    setSelectedTags([]);
    setSelectedCategory('all');
    router.push('/');
  };

  // タグの表示制御（10個のみ表示、残りは別ページで確認）
  const initialTagCount = 10;
  const visibleTags = tags.slice(0, initialTagCount);

  // FANZA TV（DMMプレミアム）のアフィリエイトリンクを生成
  const affiliateId = 'toshichan-002'
  const fanzaTvUrl = `https://al.fanza.co.jp/?lurl=https%3A%2F%2Fpremium.dmm.co.jp%2Fnotice%2Ffanzatv_welcome%2F&af_id=${affiliateId}&ch=link_tool&ch_id=link`

  return (
    <aside className="w-full lg:w-80 space-y-6 lg:sticky lg:top-24 lg:h-fit">
      {/* FANZA TV広告 */}
      <FanzaTvSidebarBanner affiliateUrl={fanzaTvUrl} />

      {/* 広告位置4: サイドバー広告 */}
      <AffiliateAdMock position="sidebar" size="300x250" />

      {/* 検索バー */}
      <div className="bg-elegant-bg-light rounded-xl p-6 border border-elegant-border">
        <h3 className="text-lg font-serif-jp text-elegant-wine mb-4">検索</h3>
        <form onSubmit={handleSearch} className="space-y-3">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="タイトルで検索..."
            className="w-full px-4 py-2 bg-elegant-bg rounded border border-elegant-border text-elegant-text placeholder:text-elegant-text-dark focus:outline-none focus:border-elegant-wine transition-colors"
          />
          <button
            type="submit"
            className="w-full px-4 py-2 bg-elegant-wine hover:bg-elegant-wine-light text-white rounded transition-colors"
          >
            検索
          </button>
        </form>
      </div>

      {/* カテゴリーフィルター */}
      <div className="bg-elegant-bg-light rounded-xl p-6 border border-elegant-border">
        <h3 className="text-lg font-serif-jp text-elegant-wine mb-4">カテゴリー</h3>
        <div className="space-y-2">
          {[
            { id: 'all', label: 'すべて', icon: '✨' },
            { id: 'mature', label: '熟女', icon: '🌹' },
            { id: 'married', label: '人妻', icon: '💍' },
            { id: 'drama', label: 'ドラマ', icon: '🎭' },
            { id: 'ntr', label: 'NTR(ネトラレ)', icon: '💔' },
            { id: 'nakadashi', label: '中出し', icon: '🎯' },
          ].map((category) => (
            <button
              key={category.id}
              onClick={() => handleCategoryChange(category.id)}
              className={`
                w-full text-left px-4 py-2 rounded transition-colors
                ${
                  selectedCategory === category.id
                    ? 'bg-elegant-wine text-white'
                    : 'bg-elegant-bg text-elegant-text hover:bg-elegant-bg-lighter'
                }
              `}
            >
              <span className="mr-2">{category.icon}</span>
              {category.label}
            </button>
          ))}
        </div>
      </div>

      {/* 人気タグ */}
      <div className="bg-elegant-bg-light rounded-xl p-6 border border-elegant-border">
        <h3 className="text-lg font-serif-jp text-elegant-wine mb-4">人気のタグ</h3>
        <div className="flex flex-wrap gap-2">
          {visibleTags.map(({ tag, count }) => (
            <button
              key={tag}
              onClick={() => handleTagClick(tag)}
              className={`
                px-3 py-1.5 rounded-full text-sm transition-colors
                ${
                  selectedTags.includes(tag)
                    ? 'bg-elegant-wine text-white'
                    : 'bg-elegant-bg text-elegant-text-light hover:bg-elegant-bg-lighter border border-elegant-border'
                }
              `}
            >
              #{tag} <span className="text-xs opacity-70">({count})</span>
            </button>
          ))}
        </div>
        {tags.length > initialTagCount && (
          <Link
            href="/tags"
            className="mt-4 block text-center text-sm text-elegant-wine hover:text-elegant-wine/80 transition-colors border border-elegant-border rounded px-4 py-2 hover:border-elegant-wine"
          >
            すべてのタグを見る ({tags.length}件)
          </Link>
        )}
      </div>

      {/* 統計情報 */}
      <div className="bg-elegant-bg-light rounded-xl p-6 border border-elegant-border">
        <h3 className="text-lg font-serif-jp text-elegant-wine mb-4">統計</h3>
        <div className="space-y-2 text-sm text-elegant-text-light">
          <div className="flex justify-between">
            <span>公開済み記事数</span>
            <span className="font-semibold text-elegant-wine">
              {(() => {
                const today = new Date()
                today.setHours(0, 0, 0, 0)
                return allPosts.filter(post => {
                  if (!post.date) return false
                  const postDate = new Date(post.date)
                  postDate.setHours(0, 0, 0, 0)
                  return postDate <= today
                }).length
              })()}
            </span>
          </div>
          <div className="flex justify-between">
            <span>総タグ数</span>
            <span className="font-semibold text-elegant-wine">{tags.length}</span>
          </div>
        </div>
      </div>

      {/* フィルターリセット */}
      {(searchQuery || selectedTags.length > 0 || selectedCategory !== 'all') && (
        <button
          onClick={clearFilters}
          className="w-full px-4 py-2 bg-elegant-bg-lighter hover:bg-elegant-bg text-elegant-text-light rounded border border-elegant-border transition-colors"
        >
          フィルターをリセット
        </button>
      )}
    </aside>
  );
}

