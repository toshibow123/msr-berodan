import fs from 'fs'
import path from 'path'
import matter from 'gray-matter'
import { remark } from 'remark'
import html from 'remark-html'

const postsDirectory = path.join(process.cwd(), 'content')

export interface PostData {
  slug: string
  title: string
  date: string
  excerpt?: string
  image?: string
  affiliateLink?: string
  subAffiliateLink?: string  // サブスク用アフィリエイトリンク
  tags?: string[]
  content?: string
  rating?: number  // 評価（4.0-5.0）
  contentId?: string  // 品番
  genre?: string[]  // ジャンル（熟女、人妻、ドラマ）
  storyScore?: number  // ストーリー評価
  actingScore?: number  // 演技評価
  atmosphereScore?: number  // 雰囲気評価
}

export async function getAllPosts(): Promise<PostData[]> {
  // contentディレクトリが存在しない場合は空配列を返す
  if (!fs.existsSync(postsDirectory)) {
    return []
  }

  const fileNames = fs.readdirSync(postsDirectory)
  const allPostsData = fileNames
    .filter((fileName) => fileName.endsWith('.md'))
    .map((fileName) => {
      const slug = fileName.replace(/\.md$/, '')
      const fullPath = path.join(postsDirectory, fileName)
      const fileContents = fs.readFileSync(fullPath, 'utf8')
      const { data } = matter(fileContents)

      return {
        slug,
        title: data.title || slug,
        date: data.date || '',
        excerpt: data.excerpt || '',
        image: data.image || '',
        affiliateLink: data.affiliateLink || '',
        subAffiliateLink: data.subAffiliateLink || '',
        tags: data.tags || [],
        rating: data.rating ? parseFloat(data.rating) : undefined,
        contentId: data.contentId || '',
        genre: data.genre || [],
        storyScore: data.storyScore ? parseFloat(data.storyScore) : undefined,
        actingScore: data.actingScore ? parseFloat(data.actingScore) : undefined,
        atmosphereScore: data.atmosphereScore ? parseFloat(data.atmosphereScore) : undefined,
      }
    })

  // 日付順にソート（未来の日付のフィルタリングはクライアントサイドで行う）
  return allPostsData.sort((a, b) => {
    if (a.date < b.date) {
      return 1
    } else {
      return -1
    }
  })
}

export async function getPostBySlug(slug: string): Promise<PostData | null> {
  const fullPath = path.join(postsDirectory, `${slug}.md`)
  
  if (!fs.existsSync(fullPath)) {
    return null
  }

  const fileContents = fs.readFileSync(fullPath, 'utf8')
  const { data, content } = matter(fileContents)

  // MarkdownをHTMLに変換
  const processedContent = await remark()
    .use(html, { sanitize: false })
    .process(content)
  let contentHtml = processedContent.toString()
  
  // アフィリエイトリンク（al.fanza.co.jp または al.dmm.co.jp）に target="_blank" を追加
  contentHtml = contentHtml.replace(
    /<a\s+href="(https?:\/\/(?:al\.(?:fanza|dmm)\.co\.jp|www\.dmm\.co\.jp)[^"]*)"([^>]*)>/gi,
    (match, url, attrs) => {
      // 既にtarget属性がある場合はスキップ
      if (/target\s*=/i.test(attrs)) {
        return match
      }
      // target="_blank" と rel="noopener noreferrer" を追加
      return `<a href="${url}"${attrs} target="_blank" rel="noopener noreferrer sponsored">`
    }
  )
  
  // サンプル動画のiframeの後にマーカーを挿入（クライアントコンポーネントで置き換え用）
  contentHtml = contentHtml.replace(
    /(<div[^>]*style="[^"]*padding-top[^"]*"[^>]*>[\s\S]*?<\/iframe><\/div>)/gi,
    (match) => {
      // 既にマーカーが挿入されている場合はスキップ
      if (match.includes('data-fanza-promo-marker')) {
        return match
      }
      return match + '<div data-fanza-promo-marker="true"></div>'
    }
  )

  return {
    slug,
    title: data.title || slug,
    date: data.date || '',
    excerpt: data.excerpt || '',
    image: data.image || '',
    affiliateLink: data.affiliateLink || '',
    subAffiliateLink: data.subAffiliateLink || '',
    tags: data.tags || [],
    content: contentHtml,
    rating: data.rating ? parseFloat(data.rating) : undefined,
    contentId: data.contentId || '',
    genre: data.genre || [],
    storyScore: data.storyScore ? parseFloat(data.storyScore) : undefined,
    actingScore: data.actingScore ? parseFloat(data.actingScore) : undefined,
    atmosphereScore: data.atmosphereScore ? parseFloat(data.atmosphereScore) : undefined,
  }
}

export async function getAllPostSlugs(): Promise<string[]> {
  if (!fs.existsSync(postsDirectory)) {
    return []
  }

  const fileNames = fs.readdirSync(postsDirectory)
  return fileNames
    .filter((fileName) => fileName.endsWith('.md'))
    .map((fileName) => fileName.replace(/\.md$/, ''))
}

export async function getAllTags(): Promise<{ tag: string; count: number }[]> {
  const posts = await getAllPosts()
  const tagCount: Record<string, number> = {}
  
  posts.forEach((post) => {
    if (post.tags && Array.isArray(post.tags)) {
      post.tags.forEach((tag) => {
        const tagStr = String(tag).trim()
        if (tagStr) {
          tagCount[tagStr] = (tagCount[tagStr] || 0) + 1
        }
      })
    }
  })
  
  return Object.entries(tagCount)
    .map(([tag, count]) => ({ tag, count }))
    .sort((a, b) => b.count - a.count)
}

