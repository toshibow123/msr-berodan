import { notFound } from 'next/navigation'
import type { Metadata } from 'next'
import { getActressById, getAllActressIds } from '@/lib/actresses'
import ActressPageClient from './ActressPageClient'

// 静的エクスポート用の設定
export const dynamicParams = false

export async function generateStaticParams() {
  const ids = getAllActressIds()
  if (ids.length === 0) {
    // 空の場合は空配列を返す（エラーを防ぐ）
    return []
  }
  return ids.map((id) => ({
    id: String(id),
  }))
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ id: string }>
}): Promise<Metadata> {
  const { id } = await params
  const actress = getActressById(id)

  if (!actress) {
    return {
      title: '女優が見つかりません',
    }
  }

  return {
    title: `${actress.name}の作品一覧`,
    description: `${actress.name}の作品${actress.works.length}件を掲載。`,
  }
}

export default async function ActressPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  const actress = getActressById(id)

  if (!actress) {
    notFound()
  }

  // 全作品を表示
  const works = actress.works

  return <ActressPageClient actress={actress} works={works} />
}

