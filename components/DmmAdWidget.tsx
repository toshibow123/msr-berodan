'use client'

interface DmmAdWidgetProps {
  dataId: string
  className?: string
  style?: React.CSSProperties
}

/**
 * DMMウィジェット広告コンポーネント
 * 固定の広告コードのみを使用するため、XSSリスクは低い
 * 注意: DMMの広告スクリプトはdangerouslySetInnerHTMLで直接HTMLを挿入しないと正しく動作しない
 */
export default function DmmAdWidget({
  dataId,
  className = 'flex justify-center',
  style = { minHeight: '250px', flex: '1 1 300px' }
}: DmmAdWidgetProps) {
  // 広告コードは固定値のみを使用（外部入力を受け付けない）
  // dataIdはホワイトリスト方式で検証
  const allowedDataIds = [
    '66426b1e79607f67541f15ec05ea7c8c',
    'f8bfa16b6ea380c9d074a49090eed3b0',
    '2e1bcfda38effdd988921925f0c34cbb',
    '3fcb9ba032b420a33838c623ce5fae4c',
    '43a8eba658580aad40df9b33383be12f'
  ]
  
  // ホワイトリストチェック
  const safeDataId = allowedDataIds.includes(dataId) ? dataId : allowedDataIds[0]
  
  // 固定値のみを使用したHTML（XSSリスクは低い）
  const adHtml = `<ins class="dmm-widget-placement" data-id="${safeDataId}" style="background:transparent"></ins><script src="https://widget-view.dmm.co.jp/js/placement.js" class="dmm-widget-scripts" data-id="${safeDataId}"></script>`
  
  return (
    <div 
      className={className}
      style={style}
      suppressHydrationWarning
      dangerouslySetInnerHTML={{ __html: adHtml }}
    />
  )
}
