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
  tags?: string[] // タイトルから抽出されるタグ
}

export interface ActressData {
  id: string // URLエンコードされた女優名
  name: string // 元の女優名
  works: WorkData[]
  image?: string // 最初の作品の画像をプロフィール画像として使用
}

/**
 * タイトルからタグを抽出する関数
 */
export function extractTagsFromTitle(title: string): string[] {
  const tags: string[] = []
  
  // 一般的なAVジャンルキーワード
  const tagKeywords = [
    '中出し', 'ベロチュー', 'ガチイキ', '人妻', '熟女', '巨乳', '美乳', 
    'スレンダー', 'ドラマ', 'NTR', 'ネトラレ', '不倫', '浮気', 
    'エステ', 'マッサージ', '痴漢', '逆ナン', 'ナンパ', '素人',
    'OL', '女教師', '看護師', '女医', 'CA', 'メイド', 'コスプレ',
    '3P', '4P', '乱交', 'レズ', 'アナル', 'フェラ', 'パイズリ',
    '顔射', '口内射精', '潮吹き', '失禁', 'SM', '拘束', '調教',
    '近親相姦', '義母', '義父', '兄嫁', '弟嫁', '姉妹', '母娘',
    'デリヘル', 'ソープ', '風俗', 'ピンサロ', 'ヘルス', 'エロマッサージ',
    '温泉', '旅行', '出張', '社内', '会社', '学校', '病院', '電車',
    '野外', '露出', '盗撮', '隠し撮り', '監視カメラ', 'ドキュメント',
    '企画', 'バラエティ', 'ゲーム', '罰ゲーム', '催眠', '媚薬',
    'ローション', 'オイル', 'バイブ', 'ローター', 'おもちゃ',
    '初体験', '処女', '童貞', '年上', '年下', 'ロリ', 'ギャル',
    '黒ギャル', '白ギャル', '金髪', '茶髪', '黒髪', 'ショート',
    'ロング', 'ツインテール', 'ポニーテール', 'お団子', 'パーマ'
  ]
  
  // タイトルに含まれるキーワードを検索
  tagKeywords.forEach(keyword => {
    if (title.includes(keyword)) {
      tags.push(keyword)
    }
  })
  
  // 特殊なパターンのマッチング
  if (title.match(/寝取ら|ネトラ|NTR/i)) {
    tags.push('NTR')
  }
  if (title.match(/中出し|なかだし|ナカダシ/i)) {
    tags.push('中出し')
  }
  if (title.match(/人妻|ひとづま|ヒトヅマ/i)) {
    tags.push('人妻')
  }
  if (title.match(/熟女|じゅくじょ|ジュクジョ/i)) {
    tags.push('熟女')
  }
  
  // 重複を除去
  return [...new Set(tags)]
}

/**
 * 女優名をURLスラッグに変換（静的サイト生成対応）
 */
export function actressNameToSlug(name: string): string {
  // 女優名の長さ制限（ファイルシステム制限対応）
  let cleanName = name
    .replace(/[（）()]/g, '') // 括弧を削除
    .replace(/\s+/g, '') // スペースを削除
    .trim()
  
  // 名前が長すぎる場合は最初の部分のみを使用
  if (cleanName.length > 30) {
    cleanName = cleanName.substring(0, 30)
  }
  
  // Base64エンコードして安全なURLスラッグを生成
  const encoded = Buffer.from(cleanName, 'utf8').toString('base64')
  
  // URL安全な文字に変換（+, /, = を置換）
  const slug = encoded
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=/g, '')
  
  // スラッグの長さも制限（最大50文字）
  return slug.length > 50 ? slug.substring(0, 50) : slug
}

/**
 * URLスラッグを女優名に変換
 */
export function slugToActressName(slug: string): string {
  try {
    // URL安全な文字を元に戻す
    const base64 = slug
      .replace(/-/g, '+')
      .replace(/_/g, '/')
    
    // パディングを追加
    const padded = base64 + '='.repeat((4 - base64.length % 4) % 4)
    
    // Base64デコードして女優名を復元
    return Buffer.from(padded, 'base64').toString('utf8')
  } catch (error) {
    console.error('Failed to decode actress slug:', slug, error)
    return slug // フォールバック
  }
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
  const works = JSON.parse(fileContents) as WorkData[]
  
  // 各作品にタグを自動生成
  return works.map(work => ({
    ...work,
    tags: extractTagsFromTitle(work.title)
  }))
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
      // 女優名が長すぎる場合はスキップ（ファイルシステム制限対応）
      if (actressName.length > 50) {
        console.warn(`女優名が長すぎるためスキップ: ${actressName.substring(0, 50)}...`)
        return
      }
      
      // 複数女優が連結されている場合は最初の女優のみを使用
      const primaryActress = actressName.split(',')[0].trim()
      
      if (!worksByActress.has(primaryActress)) {
        worksByActress.set(primaryActress, [])
      }
      worksByActress.get(primaryActress)!.push(work)
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
  const worksByActress = getWorksByActress()
  
  // 全ての女優名を検索して、スラッグが一致するものを見つける
  for (const [actressName, works] of worksByActress.entries()) {
    if (actressNameToSlug(actressName) === id) {
      return {
        id,
        name: actressName, // 元の女優名を使用
        works,
        image: works[0]?.image || undefined,
      }
    }
  }
  
  return null
}

/**
 * 全女優のID（スラッグ）を取得
 */
export function getAllActressIds(): string[] {
  const actresses = getAllActresses()
  return actresses.map(a => a.id)
}

