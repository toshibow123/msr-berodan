import { MetadataRoute } from 'next'
import { getAllPostSlugs } from '@/lib/posts'

// 静的エクスポート用の設定
export const dynamic = 'force-static'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://your-domain.com' // 環境変数で設定
  const slugs = await getAllPostSlugs()

  const posts = slugs.map((slug) => ({
    url: `${siteUrl}/posts/${slug}`,
    lastModified: new Date(),
    changeFrequency: 'weekly' as const,
    priority: 0.8,
  }))

  return [
    {
      url: siteUrl,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1,
    },
    {
      url: `${siteUrl}/profile`,
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.5,
    },
    ...posts,
  ]
}

