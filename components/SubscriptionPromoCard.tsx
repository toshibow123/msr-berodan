'use client'

// CheckアイコンをSVGで実装
const CheckIcon = ({ className }: { className?: string }) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="3"
    strokeLinecap="round"
    strokeLinejoin="round"
    className={className}
  >
    <polyline points="20 6 9 17 4 12" />
  </svg>
)

interface SubscriptionPromoCardProps {
  singleAffiliateUrl?: string
  affiliateUrl: string
}

export default function SubscriptionPromoCard({ 
  singleAffiliateUrl,
  affiliateUrl
}: SubscriptionPromoCardProps) {
  return (
    <div className="my-12">
      {/* PR表示 */}
      <div className="text-center mb-2">
        <span className="text-xs text-neutral-500 font-medium bg-neutral-900 px-3 py-1 rounded-full border border-neutral-800">PR・アフィリエイト広告</span>
      </div>
      
      <div className="bg-neutral-900 rounded-lg border border-neutral-800 overflow-hidden">
        {/* ヘッダー */}
        <div className="bg-neutral-800 px-6 py-3 border-b border-neutral-700">
          <h3 className="text-lg font-bold text-neutral-100 text-center">
            お得な視聴方法を比較
          </h3>
        </div>

        {/* 比較カード（モバイル: 縦積み、PC: 横並び） */}
        <div className="grid md:grid-cols-2 gap-0">
          {/* A. 単品レンタル・購入エリア（左 or 上） */}
          <div className="bg-neutral-800 p-6 border-r border-neutral-700 md:border-b-0 border-b">
            <div className="text-center">
              <div className="text-sm text-neutral-400 mb-2">通常価格</div>
              <div className="mb-4">
                <div className="text-xs text-neutral-500">1本あたり</div>
              </div>
              {singleAffiliateUrl ? (
                <a
                  href={singleAffiliateUrl}
                  target="_blank"
                  rel="sponsored noopener noreferrer"
                  className="inline-block px-4 py-2 bg-neutral-700 hover:bg-neutral-600 text-neutral-200 text-sm rounded transition-colors"
                >
                  単品で購入する
                </a>
              ) : (
                <div className="inline-block px-4 py-2 bg-neutral-700 text-neutral-500 text-sm rounded cursor-not-allowed opacity-60">
                  単品で購入する
                </div>
              )}
            </div>
          </div>

          {/* B. DMM TV (FANZA TV) エリア（右 or 下）★強調 */}
          <div className="bg-gradient-to-br from-yellow-700 to-yellow-600 p-6 relative overflow-hidden">
            {/* バッジ */}
            <div className="absolute top-2 right-2">
              <span className="bg-yellow-800 text-yellow-100 text-xs font-bold px-2 py-1 rounded">
                おすすめ！見放題対象
              </span>
            </div>

            <div className="text-center text-neutral-950">
              <div className="mb-4">
                <div className="text-3xl font-bold mb-2">
                  月額 550円
                </div>
                <div className="text-xl font-bold bg-yellow-800 text-yellow-100 px-4 py-2 rounded-full inline-block mb-3">
                  初回 14日間無料
                </div>
              </div>

              {/* 特典リスト */}
              <div className="space-y-2 mb-4 text-left bg-yellow-800/30 rounded-lg p-3">
                <div className="flex items-start gap-2 text-sm">
                  <CheckIcon className="w-5 h-5 text-yellow-900 flex-shrink-0 mt-0.5" />
                  <span className="text-neutral-950">追加料金なしでFANZAも見放題</span>
                </div>
                <div className="flex items-start gap-2 text-sm">
                  <CheckIcon className="w-5 h-5 text-yellow-900 flex-shrink-0 mt-0.5" />
                  <span className="text-neutral-950">
                    <strong className="text-yellow-900">登録だけですぐに550pt</strong>もらえる
                  </span>
                </div>
                <div className="flex items-start gap-2 text-sm">
                  <CheckIcon className="w-5 h-5 text-yellow-900 flex-shrink-0 mt-0.5" />
                  <span className="text-neutral-950">アニメ・ドラマも見放題</span>
                </div>
              </div>

              {/* CTAボタン */}
              <a
                href={affiliateUrl}
                target="_blank"
                rel="sponsored noopener noreferrer"
                className="inline-block w-full bg-neutral-950 hover:bg-neutral-900 text-yellow-500 font-bold py-4 px-6 rounded-lg transition-all shadow-lg hover:shadow-xl text-lg animate-pulse"
              >
                今すぐ無料で試す（550pt GET）
              </a>
            </div>
          </div>
        </div>

        {/* フッター（補足情報） */}
        <div className="bg-neutral-800 px-6 py-3 border-t border-neutral-700">
          <p className="text-xs text-neutral-400 text-center">
            ※ 無料体験期間中に解約すれば料金は一切かかりません
          </p>
        </div>
      </div>
    </div>
  )
}
