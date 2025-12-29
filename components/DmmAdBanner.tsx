'use client'

interface DmmAdBannerProps {
  affiliateId: string
  bannerId: string
  className?: string
  style?: React.CSSProperties
}

/**
 * DMMバナー広告コンポーネント
 * 固定の広告コードのみを使用するため、XSSリスクは低い
 * 注意: DMMの広告スクリプトはdangerouslySetInnerHTMLで直接HTMLを挿入しないと正しく動作しない
 */
export default function DmmAdBanner({
  affiliateId,
  bannerId,
  className = 'flex justify-center',
  style = { minHeight: '250px', flex: '1 1 300px' }
}: DmmAdBannerProps) {
  // 広告コードは固定値のみを使用（外部入力を受け付けない）
  // affiliateIdとbannerIdは固定値のみを受け付ける（ホワイトリスト方式）
  const allowedAffiliateIds = ['toshichan-002']
  const allowedBannerIds = ['1760_300_250', '1298_300_250']
  
  // ホワイトリストチェック
  const safeAffiliateId = allowedAffiliateIds.includes(affiliateId) ? affiliateId : allowedAffiliateIds[0]
  const safeBannerId = allowedBannerIds.includes(bannerId) ? bannerId : allowedBannerIds[0]
  
  // URLエンコードして安全に構築
  const adScriptUrl = `https://widget-view.dmm.co.jp/js/banner_placement.js?affiliate_id=${encodeURIComponent(safeAffiliateId)}&banner_id=${encodeURIComponent(safeBannerId)}`
  
  // 固定値のみを使用したHTML（XSSリスクは低い）
  const adHtml = `<ins class="widget-banner"></ins><script class="widget-banner-script" src="${adScriptUrl}"></script>`
  
  return (
    <div 
      className={className}
      style={style}
      suppressHydrationWarning
      dangerouslySetInnerHTML={{ __html: adHtml }}
    />
  )
}

