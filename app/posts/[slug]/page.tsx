import { notFound } from 'next/navigation'
import Link from 'next/link'
import type { Metadata } from 'next'
import { getPostBySlug, getAllPostSlugs, getAllPosts } from '@/lib/posts'
import RelatedPosts from '@/components/RelatedPosts'
import FanzaSubscriptionPromo from '@/components/FanzaSubscriptionPromo'
import ArticleContentWithPromo from '@/components/ArticleContentWithPromo'
import AffiliateAdMock from '@/components/AffiliateAdMock'
import EditorialRecommendations from '@/components/EditorialRecommendations'
import MgstageAd from '@/components/MgstageAd'
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
  const description = post.excerpt || `${post.title}のレビュー。大人の女性の色気とストーリー性を、官能小説のような筆致で綴ります。`

  return {
    title: post.title,
    description,
    keywords: post.tags || [],
    openGraph: {
      title: post.title,
      description,
      url,
      siteName: '艶めく物語',
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
function extractRatings(post: any, averageRating: number) {
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

// 平均評価を計算（記事のratingを使用、なければデフォルト値）
function calculateAverageRating(post: any): string {
  if (post.rating && typeof post.rating === 'number') {
    return post.rating.toFixed(1)
  }
  // デフォルト値（4.5）
  return '4.5'
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

  // 関連記事用に全記事を取得
  const allPosts = await getAllPosts()

  const averageRating = calculateAverageRating(post)
  const ratings = extractRatings(post, parseFloat(averageRating))

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
      name: '艶めく物語',
    },
    publisher: {
      '@type': 'Organization',
      name: '艶めく物語',
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
      {/* JSON.stringifyでエスケープされているため、XSSリスクは低い */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <div className="min-h-screen bg-elegant-bg">
      {/* 広告位置5: 固定追従バナー（モバイル対応・上部固定） */}
      <div className="lg:hidden">
        <AffiliateAdMock position="sticky" size="728x90" />
      </div>

      {/* ヘッダー */}
      <header className="border-b-2 border-elegant-gold/30 bg-elegant-bg-light sticky top-[90px] lg:top-0 z-50 shadow-lg">
        <div className="max-w-5xl mx-auto px-6 py-4">
          <Link 
            href="/"
            className="inline-flex items-center gap-2 text-elegant-text-light hover:text-elegant-wine transition-colors text-sm font-medium"
          >
            <span>←</span>
            <span>記事一覧に戻る</span>
          </Link>
        </div>
      </header>

      <div className="max-w-5xl mx-auto px-6 py-12">
        {/* メインコンテンツとサイドバー */}
        <div className="flex gap-8 items-start">
          <main className="flex-1 max-w-4xl">
        {/* 記事ヘッダー */}
        <div className="mb-12">
          <h1 className="text-4xl md:text-5xl font-serif-jp text-elegant-wine mb-6 leading-relaxed tracking-wider">
            {post.title}
          </h1>
          
          {/* ジャンルタグ */}
          {post.genre && post.genre.length > 0 && (
            <div className="flex flex-wrap items-center gap-3 mb-4">
              {post.genre.map((g: string) => (
                <span
                  key={g}
                  className="px-4 py-1.5 bg-elegant-wine text-white text-sm font-medium rounded-full"
                >
                  {g}
                </span>
              ))}
            </div>
          )}
          
          {/* 評価スコア */}
          {(post.storyScore || post.actingScore || post.atmosphereScore) && (
            <div className="flex gap-6 mb-4 text-sm text-elegant-text-light">
              {post.storyScore && (
                <div className="flex items-center gap-1">
                  <span className="font-medium">物語</span>
                  <span className="text-elegant-wine font-bold">{post.storyScore}</span>
                </div>
              )}
              {post.actingScore && (
                <div className="flex items-center gap-1">
                  <span className="font-medium">演技</span>
                  <span className="text-elegant-wine font-bold">{post.actingScore}</span>
                </div>
              )}
              {post.atmosphereScore && (
                <div className="flex items-center gap-1">
                  <span className="font-medium">雰囲気</span>
                  <span className="text-elegant-wine font-bold">{post.atmosphereScore}</span>
                </div>
              )}
            </div>
          )}
          
          {/* タグ */}
          <div className="flex flex-wrap items-center gap-2 mb-4">
            {post.tags && post.tags.slice(0, 6).map((tag: string) => (
              <Link
                key={tag}
                href={`/?tag=${encodeURIComponent(tag)}`}
                className="px-3 py-1 bg-elegant-bg-lighter rounded border border-elegant-border text-elegant-text-light text-xs hover:bg-elegant-wine/20 hover:text-elegant-wine transition-colors"
              >
                #{tag}
              </Link>
            ))}
          </div>

          {post.date && (
            <time className="text-elegant-text-dark text-sm tracking-wider">
              {new Date(post.date).toLocaleDateString('ja-JP', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
              })}
            </time>
          )}
        </div>

        {/* 広告位置1: 記事上部（タイトル下〜導入文直後） */}
        <MgstageAd 
          scriptUrl="https://www.mgstage.com/afscript/prestigebb/728_90/N2G56Q3UYEPYWXP7P8PKPRIDC3/"
          containerId="mgstage-ad-top"
        />

        {/* メインビジュアル */}
        {post.image && (
          <div className="mb-12">
            <img
              src={post.image}
              alt={post.title}
              className="w-full h-auto rounded-lg border border-elegant-border shadow-lg"
            />
          </div>
        )}

        {/* 広告位置2: メインビジュアルの後 */}
        <AffiliateAdMock position="top" size="responsive" />

        {/* メインアクション (CTA) - ラグジュアリーデザイン */}
        {post.affiliateLink && (
          <div className="mb-12">
            <a
              href={post.affiliateLink}
              target="_blank"
              rel="noopener noreferrer sponsored"
              className="flex items-center justify-center gap-3 w-full bg-gradient-to-r from-elegant-wine to-elegant-wine-dark text-white hover:from-elegant-wine-dark hover:to-elegant-wine font-serif-jp font-semibold text-lg py-5 px-8 rounded-xl transition-all shadow-lg hover:shadow-xl hover:scale-[1.02]"
            >
              <PlayCircle className="w-6 h-6" />
              <span>作品を鑑賞する</span>
            </a>
          </div>
        )}

        {/* 本文エリア */}
        <article className="prose max-w-none mb-20">
          <ArticleContentWithPromo 
            content={post.content || ''}
            affiliateLink={post.affiliateLink}
            contentId={post.contentId}
          />
        </article>

        {/* 広告位置3: 記事末尾（まとめの直後） */}
        <MgstageAd 
          scriptUrl="https://www.mgstage.com/afscript/superch/728_90/N2G56Q3UYEPYWXP7P8PKPRIDC3/"
          containerId="mgstage-ad-bottom"
        />

        {/* FANZA TV / 単品購入の誘導ボックス */}
        <FanzaSubscriptionPromo 
          singleAffiliateUrl={post.affiliateLink}
          contentId={post.contentId}
        />

        {/* 広告位置4: 関連記事の前 */}
        <AffiliateAdMock position="bottom" size="responsive" />

        {/* 関連記事 */}
        <div data-related-posts>
          <RelatedPosts 
            currentSlug={slug}
            currentTags={post.tags}
            allPosts={allPosts}
          />
        </div>

        {/* TOPページに戻るボタン */}
        <div className="mt-16 mb-8 text-center">
          <Link
            href="/"
            className="inline-flex items-center gap-2 px-8 py-4 bg-elegant-gold hover:bg-elegant-champagne text-elegant-bg font-serif-jp font-semibold rounded-xl transition-all shadow-md hover:shadow-lg hover:scale-105"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="w-5 h-5"
            >
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
              <polyline points="9 22 9 12 15 12 15 22" />
            </svg>
            <span>記事一覧に戻る</span>
          </Link>
        </div>
        </main>

        {/* 編集部おすすめ（PCのみ） */}
        <EditorialRecommendations 
          currentPost={post}
          allPosts={allPosts}
        />
        </div>

      </div>

      {/* 広告位置5: 固定追従バナー（モバイル対応・上部固定） */}
      <div className="lg:hidden">
        <AffiliateAdMock position="sticky" size="728x90" />
      </div>

      {/* スティッキーフッター (Mobile) */}
      {post.affiliateLink && (
        <div className="fixed bottom-0 left-0 right-0 bg-elegant-bg-light border-t-2 border-elegant-gold/30 p-4 z-50 lg:hidden shadow-lg">
          <a
            href={post.affiliateLink}
            target="_blank"
            rel="noopener noreferrer sponsored"
            className="flex items-center justify-center gap-2 w-full bg-gradient-to-r from-elegant-wine to-elegant-wine-dark text-white font-serif-jp font-semibold py-3 px-4 rounded-xl transition-all shadow-md hover:shadow-lg"
          >
            <PlayCircle className="w-5 h-5" />
            <span>作品を鑑賞する</span>
          </a>
        </div>
      )}
      
      </div>
    </>
  )
}
