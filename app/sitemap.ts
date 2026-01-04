import { MetadataRoute } from 'next'
import { getAllActressIds } from '@/lib/actresses'

// 静的エクスポート用の設定
export const dynamic = 'force-static'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://your-domain.com' // 環境変数で設定
  const actressIds = getAllActressIds()

  const actresses = actressIds.map((id) => ({
    url: `${siteUrl}/actresses/${id}`,
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
      url: `${siteUrl}/test-ads`,
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.3,
    },
    ...actresses,
  ]
}

