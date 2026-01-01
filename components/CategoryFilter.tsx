'use client';

import { useRouter, useSearchParams } from 'next/navigation';

const categories = [
  { id: 'all', label: 'すべて', icon: '✨' },
  { id: 'mature', label: '熟女', icon: '🌹' },
  { id: 'married', label: '人妻', icon: '💍' },
  { id: 'drama', label: 'ドラマ', icon: '🎭' },
  { id: 'ntr', label: 'NTR(ネトラレ)', icon: '💔' },
  { id: 'nakadashi', label: '中出し', icon: '🎯' },
];

export default function CategoryFilter() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const currentCategory = searchParams.get('category') || 'all';
  const tag = searchParams.get('tag');
  const search = searchParams.get('search');
  
  // フィルターが適用されているかチェック
  const hasFilters = currentCategory !== 'all' || tag || search;

  const handleCategoryChange = (categoryId: string) => {
    if (categoryId === 'all') {
      router.push('/');
    } else {
      router.push(`/?category=${categoryId}`);
    }
  };

  const handleResetFilters = () => {
    router.push('/');
  };

  return (
    <div className="bg-elegant-bg-light border-y-2 border-elegant-border py-6">
      <div className="max-w-5xl mx-auto px-6">
        <div className="flex flex-wrap justify-center items-center gap-4">
          {categories.map((category) => (
            <button
              key={category.id}
              onClick={() => handleCategoryChange(category.id)}
              className={`
                px-6 py-3 rounded-full font-medium transition-all duration-300
                ${
                  currentCategory === category.id
                    ? 'bg-elegant-wine text-white shadow-md'
                    : 'bg-elegant-bg-lighter text-elegant-text hover:bg-elegant-wine/20 hover:text-elegant-wine border border-elegant-border'
                }
              `}
            >
              <span className="mr-2">{category.icon}</span>
              {category.label}
            </button>
          ))}
          {hasFilters && (
            <button
              onClick={handleResetFilters}
              className="px-4 py-3 rounded-full font-medium transition-all duration-300 bg-elegant-bg-lighter text-elegant-text hover:bg-elegant-wine/20 hover:text-elegant-wine border border-elegant-border"
            >
              ✕ リセット
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

