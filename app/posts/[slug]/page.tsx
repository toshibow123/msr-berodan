import { notFound } from 'next/navigation'
import Link from 'next/link'
import type { Metadata } from 'next'
import { getPostBySlug, getAllPostSlugs } from '@/lib/posts'
import ArticleRadarChart from '@/components/RadarChart'
import SubscriptionPromoCard from '@/components/SubscriptionPromoCard'
import DmmAdWidgetSimple from '@/components/DmmAdWidgetSimple'
import DmmAdWidgetStatic from '@/components/DmmAdWidgetStatic'
import DmmCampaignBanner from '@/components/DmmCampaignBanner'
import ArticleContentWithAds from '@/components/ArticleContentWithAds'
import VitalityPromoSection from '@/components/VitalityPromoSection'
import TengaEggPromoSection from '@/components/TengaEggPromoSection'
// PlayCircleアイコンをSVGで実装（React 19互換性のため）
const PlayCircle = ({ className }: { className?: string }) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    className={className}
  >
    <circle cx="12" cy="12" r="10" />
    <polygon points="10 8 16 12 10 16 10 8" />
  </svg>
)

export async function generateStaticParams() {
  const slugs = await getAllPostSlugs()
  return slugs.map((slug) => ({
    slug,
  }))
}

// SEO用のメタデータ生成
export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>
}): Promise<Metadata> {
  const { slug } = await params
  const post = await getPostBySlug(slug)

  if (!post) {
    return {
      title: '記事が見つかりません',
    }
  }

  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://your-domain.com' // 環境変数で設定
  const url = `${siteUrl}/posts/${slug}`
  const description = post.excerpt || `${post.title}の熱いレビュー。平成時代の名作を再評価する。`

  return {
    title: post.title,
    description,
    keywords: post.tags || [],
    openGraph: {
      title: post.title,
      description,
      url,
      siteName: '過去作・旧作大好きブログ',
      images: post.image ? [
        {
          url: post.image,
          width: 1200,
          height: 630,
          alt: post.title,
        },
      ] : [],
      locale: 'ja_JP',
      type: 'article',
      publishedTime: post.date,
    },
    twitter: {
      card: 'summary_large_image',
      title: post.title,
      description,
      images: post.image ? [post.image] : [],
    },
    alternates: {
      canonical: url,
    },
  }
}

// 評価データを抽出（記事のメタデータから、またはデフォルト値）
function extractRatings(post: any) {
  // 記事のメタデータに評価が含まれている場合はそれを使用
  // なければデフォルト値を返す
  const defaultRatings = [
    { name: '実用度', value: 4.0 },
    { name: 'ストーリー', value: 4.5 },
    { name: '演技力', value: 4.5 },
    { name: '伝説度', value: 4.0 },
    { name: '画質の味', value: 3.5 },
  ]
  
  // 将来的にメタデータから評価を取得できるように拡張可能
  return post.ratings || defaultRatings
}

// 平均評価を計算
function calculateAverageRating(ratings: { value: number }[]) {
  const sum = ratings.reduce((acc, r) => acc + r.value, 0)
  return (sum / ratings.length).toFixed(1)
}

export default async function PostPage({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  const post = await getPostBySlug(slug)

  if (!post) {
    notFound()
  }

  const ratings = extractRatings(post)
  const averageRating = calculateAverageRating(ratings)

  // タグから年代を抽出
  const yearTag = post.tags?.find((tag: string) => tag.includes('年'))
  const year = yearTag ? yearTag.replace('年', '') : ''

  // タグから女優名を抽出（最初のタグが女優名の可能性が高い）
  const actressTag = post.tags?.find((tag: string) => 
    !tag.includes('年') && 
    !tag.includes('平成') && 
    !tag.includes('作品') &&
    !tag.includes('ハイビジョン')
  )
  const actress = actressTag || ''

  // 構造化データ（JSON-LD）を生成
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://your-domain.com'
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: post.title,
    description: post.excerpt || `${post.title}の熱いレビュー。`,
    image: post.image ? [post.image] : [],
    datePublished: post.date,
    dateModified: post.date,
    author: {
      '@type': 'Person',
      name: '過去作・旧作大好きブログ',
    },
    publisher: {
      '@type': 'Organization',
      name: '過去作・旧作大好きブログ',
      logo: {
        '@type': 'ImageObject',
        url: `${siteUrl}/logo.png`, // ロゴがある場合
      },
    },
    mainEntityOfPage: {
      '@type': 'WebPage',
      '@id': `${siteUrl}/posts/${slug}`,
    },
  }

  return (
    <>
      {/* 構造化データ（JSON-LD） */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <div className="min-h-screen bg-neutral-950 text-neutral-200">
      {/* ヘッダー */}
      <header className="border-b border-neutral-800 bg-neutral-900/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <Link 
            href="/"
            className="inline-flex items-center gap-2 text-neutral-400 hover:text-yellow-500 transition-colors text-sm"
          >
            <span>←</span>
            <span>アーカイブに戻る</span>
          </Link>
        </div>
      </header>

      <div className="flex flex-col lg:flex-row gap-8 max-w-7xl mx-auto px-4 py-8">
        {/* メインコンテンツ */}
        <main className="flex-1 min-w-0 max-w-5xl">
        {/* 記事ヘッダー */}
        <div className="mb-8">
          <h1 className="text-4xl md:text-5xl font-bold text-neutral-100 mb-4">
            {post.title}
          </h1>
          
          <div className="flex flex-wrap items-center gap-4 text-sm text-neutral-400 mb-6">
            {post.tags && post.tags.map((tag: string) => (
              <Link
                key={tag}
                href={`/?tag=${encodeURIComponent(tag)}`}
                className="px-3 py-1 bg-neutral-900 rounded-full border border-neutral-800 hover:border-yellow-500 hover:text-yellow-500 transition-colors"
              >
                {tag}
              </Link>
            ))}
          </div>

          {post.date && (
            <time className="text-neutral-500 text-sm">
              発売日: {post.date}
            </time>
          )}
        </div>

        {/* メインビジュアル */}
        {post.image && (
          <div className="mb-8">
            <img
              src={post.image}
              alt={post.title}
              className="w-full h-auto rounded-lg border border-neutral-800 shadow-2xl"
            />
          </div>
        )}

        {/* FANZA TVリンク - 位置1 */}
        <div className="my-6 text-center">
          <a
            href="https://al.fanza.co.jp/?lurl=https%3A%2F%2Fpremium.dmm.co.jp%2Fbenefit%2F&af_id=toshichan-002&ch=link_tool&ch_id=text"
            rel="sponsored"
            target="_blank"
            className="inline-block px-6 py-3 bg-yellow-600 hover:bg-yellow-500 text-neutral-950 font-bold rounded-lg transition-colors shadow-lg hover:shadow-xl"
          >
            FANZA TV
          </a>
        </div>

        {/* レーダーチャート */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-bold text-neutral-100">評価チャート</h2>
            <div className="flex items-center gap-2">
              <span className="text-yellow-500 text-3xl font-bold">★{averageRating}</span>
            </div>
          </div>
          <ArticleRadarChart data={ratings} />
        </div>

        {/* サブスク誘導カード */}
        <SubscriptionPromoCard 
          singleAffiliateUrl={post.affiliateLink}
          affiliateUrl="https://al.fanza.co.jp/?lurl=https%3A%2F%2Fpremium.dmm.co.jp%2Fbenefit%2F&af_id=toshichan-002&ch=link_tool&ch_id=text"
        />

        {/* メインアクション (CTA) */}
        {post.affiliateLink && (
          <div className="mb-12">
            <a
              href={post.affiliateLink}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center justify-center gap-3 w-full bg-transparent border-2 border-yellow-600 text-yellow-500 hover:bg-yellow-600/10 font-bold text-lg py-4 px-6 rounded-lg transition-all"
            >
              <PlayCircle className="w-6 h-6" />
              <span>無料でサンプル動画を再生 (FANZA)</span>
            </a>
          </div>
        )}

        {/* 広告ウィジェット - 位置2 */}
        <DmmAdWidgetSimple adId="66426b1e79607f67541f15ec05ea7c8c" />

        {/* 本文エリア */}
        <article className="prose prose-invert prose-lg max-w-none mb-20">
          <ArticleContentWithAds htmlContent={post.content || ''} />
        </article>

        {/* 広告ウィジェット - 位置4 */}
        <DmmAdWidgetSimple adId="f8bfa16b6ea380c9d074a49090eed3b0" />

        {/* サプリLPセクション */}
        <VitalityPromoSection />

        {/* オナホールLPセクション */}
        <TengaEggPromoSection />
        </main>

        {/* サイドバー - 位置5（追従広告） */}
        <aside className="lg:w-72 flex-shrink-0">
          <div className="lg:sticky lg:top-24 space-y-6">
            <DmmAdWidgetSimple adId="3fcb9ba032b420a33838c623ce5fae4c" />
            {/* キャンペーンバナー */}
            <DmmCampaignBanner 
              affiliateId="toshichan-002"
              bannerId="1760_300_250"
            />
          </div>
        </aside>
      </div>

      {/* スティッキーフッター (Mobile) */}
      {post.affiliateLink && (
        <div className="fixed bottom-0 left-0 right-0 bg-neutral-900 border-t border-neutral-800 p-4 z-50 lg:hidden">
          <a
            href={post.affiliateLink}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center justify-center gap-2 w-full bg-yellow-600 hover:bg-yellow-500 text-neutral-950 font-bold py-3 px-4 rounded-lg transition-colors"
          >
            <PlayCircle className="w-5 h-5" />
            <span>サンプルを見る</span>
          </a>
        </div>
      )}
      </div>
    </>
  )
}
