import fs from 'fs'
import path from 'path'

export interface WorkData {
  title: string
  image: string
  videoUrl: string | null
  actress: string | null
  date: string
  affiliateLink: string
  description?: string // あらすじ
  comment?: string // コメント（あらすじの代替）
}

export interface ActressData {
  id: string // URLエンコードされた女優名
  name: string // 元の女優名
  works: WorkData[]
  image?: string // 最初の作品の画像をプロフィール画像として使用
}

/**
 * 女優名をURLスラッグに変換
 */
export function actressNameToSlug(name: string): string {
  return encodeURIComponent(name)
}

/**
 * URLスラッグを女優名に変換
 */
export function slugToActressName(slug: string): string {
  return decodeURIComponent(slug)
}

/**
 * all_works.jsonから全作品データを読み込む
 */
export function getAllWorks(): WorkData[] {
  const dataPath = path.join(process.cwd(), 'data', 'all_works.json')
  
  if (!fs.existsSync(dataPath)) {
    return []
  }
  
  const fileContents = fs.readFileSync(dataPath, 'utf8')
  return JSON.parse(fileContents) as WorkData[]
}

/**
 * 女優名で作品をグループ化
 */
export function getWorksByActress(): Map<string, WorkData[]> {
  const allWorks = getAllWorks()
  const worksByActress = new Map<string, WorkData[]>()
  
  allWorks.forEach((work) => {
    if (!work.actress) {
      return
    }
    
    // 「、」で区切られた複数の女優名を処理
    const actresses = work.actress.split('、').map(a => a.trim()).filter(a => a && a !== '不明')
    
    actresses.forEach((actressName) => {
      if (!worksByActress.has(actressName)) {
        worksByActress.set(actressName, [])
      }
      worksByActress.get(actressName)!.push(work)
    })
  })
  
  // 各女優の作品を日付順（新しい順）にソート
  worksByActress.forEach((works) => {
    works.sort((a, b) => {
      if (a.date < b.date) return 1
      if (a.date > b.date) return -1
      return 0
    })
  })
  
  return worksByActress
}

/**
 * 全女優のデータを取得
 */
export function getAllActresses(): ActressData[] {
  const worksByActress = getWorksByActress()
  const actresses: ActressData[] = []
  
  worksByActress.forEach((works, name) => {
    actresses.push({
      id: actressNameToSlug(name),
      name,
      works,
      image: works[0]?.image || undefined,
    })
  })
  
  // 作品数の多い順にソート
  actresses.sort((a, b) => b.works.length - a.works.length)
  
  return actresses
}

/**
 * 特定の女優のデータを取得
 */
export function getActressById(id: string): ActressData | null {
  const name = slugToActressName(id)
  const worksByActress = getWorksByActress()
  const works = worksByActress.get(name)
  
  if (!works || works.length === 0) {
    return null
  }
  
  return {
    id,
    name,
    works,
    image: works[0]?.image || undefined,
  }
}

/**
 * 全女優のID（スラッグ）を取得
 */
export function getAllActressIds(): string[] {
  const actresses = getAllActresses()
  return actresses.map(a => a.id)
}

