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

interface FanzaSubscriptionPromoProps {
  singleAffiliateUrl?: string  // 単品購入用のアフィリエイトリンク
  contentId?: string  // 作品ID（FANZA TVリンク生成用）
}

export default function FanzaSubscriptionPromo({ 
  singleAffiliateUrl,
  contentId
}: FanzaSubscriptionPromoProps) {
  // FANZA TV（DMMプレミアム）のアフィリエイトリンクを生成
  // アフィリエイトIDは環境変数から取得、またはデフォルト値を使用
  const affiliateId = 'toshichan-002'  // 必要に応じて環境変数から取得
  const fanzaTvUrl = `https://al.fanza.co.jp/?lurl=https%3A%2F%2Fpremium.dmm.co.jp%2Fnotice%2Ffanzatv_welcome%2F&af_id=${affiliateId}&ch=link_tool&ch_id=link`

  return (
    <div className="my-12">
      {/* PR表示 */}
      <div className="text-center mb-4">
        <span className="text-xs text-elegant-text-dark font-medium bg-elegant-bg-lighter px-4 py-1.5 rounded-full border border-elegant-border">PR・アフィリエイト広告</span>
      </div>
      
      <div className="bg-elegant-bg-light rounded-xl border-2 border-elegant-wine/30 overflow-hidden shadow-xl">
        {/* ヘッダー */}
        <div className="bg-gradient-to-r from-elegant-wine/40 to-elegant-wine-dark/40 px-6 py-4 border-b-2 border-elegant-wine/30">
          <h3 className="text-xl font-serif-jp font-bold text-elegant-wine text-center">
            お得な視聴方法を比較
          </h3>
        </div>

        {/* 比較カード（モバイル: 縦積み、PC: 横並び） */}
        <div className="grid md:grid-cols-2 gap-0">
          {/* A. 単品レンタル・購入エリア（左 or 上） */}
          <div className="bg-elegant-bg-lighter p-6 border-r-2 border-elegant-border md:border-b-0 border-b-2">
            <div className="text-center">
              <div className="text-sm text-elegant-text-light mb-2 font-medium">通常価格</div>
              <div className="mb-4">
                <div className="text-xs text-elegant-text-dark">1本あたり</div>
              </div>
              {singleAffiliateUrl ? (
                <a
                  href={singleAffiliateUrl}
                  target="_blank"
                  rel="sponsored noopener noreferrer"
                  className="inline-block px-6 py-3 bg-elegant-bg hover:bg-elegant-wine/20 text-elegant-text hover:text-elegant-wine border-2 border-elegant-border hover:border-elegant-wine font-medium rounded-lg transition-all duration-300"
                >
                  単品で購入する
                </a>
              ) : (
                <div className="inline-block px-6 py-3 bg-elegant-bg text-elegant-text-dark text-sm rounded-lg cursor-not-allowed opacity-60 border-2 border-elegant-border">
                  単品で購入する
                </div>
              )}
            </div>
          </div>

          {/* B. DMM TV (FANZA TV) エリア（右 or 下）★強調 */}
          <div className="bg-gradient-to-br from-elegant-wine/50 via-elegant-wine-dark/60 to-elegant-wine/50 p-6 relative overflow-hidden border-l-2 border-elegant-wine/50">
            {/* バッジ */}
            <div className="absolute top-3 right-3">
              <span className="bg-elegant-wine-dark text-elegant-wine-light text-xs font-bold px-3 py-1.5 rounded-full shadow-lg border border-elegant-wine/30">
                おすすめ！見放題対象
              </span>
            </div>

            <div className="text-center">
              <div className="mb-4">
                <div className="text-3xl font-serif-jp font-bold mb-2 text-elegant-wine-light">
                  月額 550円
                </div>
                <div className="text-xl font-serif-jp font-bold bg-elegant-wine-dark text-elegant-wine-light px-5 py-2 rounded-full inline-block mb-3 shadow-md border border-elegant-wine/30">
                  初回 14日間無料
                </div>
              </div>

              {/* 特典リスト */}
              <div className="space-y-2.5 mb-5 text-left bg-elegant-bg-light/60 rounded-lg p-4 border border-elegant-wine/20">
                <div className="flex items-start gap-2 text-sm">
                  <CheckIcon className="w-5 h-5 text-elegant-wine flex-shrink-0 mt-0.5" />
                  <span className="text-elegant-text font-medium">追加料金なしでFANZAも見放題</span>
                </div>
                <div className="flex items-start gap-2 text-sm">
                  <CheckIcon className="w-5 h-5 text-elegant-wine flex-shrink-0 mt-0.5" />
                  <span className="text-elegant-text font-medium">
                    <strong className="text-elegant-wine">登録だけですぐに550pt</strong>もらえる
                  </span>
                </div>
                <div className="flex items-start gap-2 text-sm">
                  <CheckIcon className="w-5 h-5 text-elegant-wine flex-shrink-0 mt-0.5" />
                  <span className="text-elegant-text font-medium">アニメ・ドラマも見放題</span>
                </div>
              </div>

              {/* CTAボタン */}
              <a
                href={fanzaTvUrl}
                target="_blank"
                rel="sponsored noopener noreferrer"
                className="inline-block w-full bg-elegant-wine-dark hover:bg-elegant-wine text-white font-serif-jp font-bold py-4 px-6 rounded-lg transition-all shadow-lg hover:shadow-xl text-lg hover:scale-105 border-2 border-elegant-wine/50"
              >
                今すぐ無料で試す（550pt GET）
              </a>
            </div>
          </div>
        </div>

        {/* フッター（補足情報） */}
        <div className="bg-elegant-bg-lighter px-6 py-3 border-t-2 border-elegant-border">
          <p className="text-xs text-elegant-text-dark text-center">
            ※ 無料体験期間中に解約すれば料金は一切かかりません
          </p>
        </div>
      </div>
    </div>
  )
}

