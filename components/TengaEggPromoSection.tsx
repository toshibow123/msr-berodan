'use client'

import React from 'react'

// CheckアイコンをSVGで実装
const CheckIcon = ({ className }: { className?: string }) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    className={className}
  >
    <polyline points="20 6 9 17 4 12" />
  </svg>
)

// HeartPulseアイコンをSVGで実装
const HeartPulse = ({ className }: { className?: string }) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    className={className}
  >
    <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.29 1.51 4.04 3 5.5l7 7Z" />
    <polyline points="3.5 12 6.5 15 10.5 9" />
  </svg>
)

const TengaEggPromoSection: React.FC = () => {
  return (
    <div className="space-y-12 my-16">
      {/* SPONSORED CONTENT 区切り線 */}
      <div className="w-full border-t border-neutral-800 relative">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-neutral-950 px-6 py-2 text-yellow-500 font-bold tracking-widest text-sm">
          SPONSORED CONTENT
        </div>
      </div>

      {/* Product Hero */}
      <section className="bg-neutral-900/50 border border-neutral-800 rounded-3xl p-8 md:p-12 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent to-black/40 pointer-events-none"></div>
        
        <div className="grid md:grid-cols-2 gap-12 items-center relative z-10">
          <div>
            <h2 className="text-yellow-400 text-2xl font-black mb-4 flex items-center">
              <span className="w-8 h-8 bg-yellow-400 text-neutral-950 flex items-center justify-center rounded-full mr-3 text-lg italic">!</span>
              究極の選択：バリエーション12種
            </h2>
            <p className="text-neutral-200 text-lg leading-relaxed mb-6">
              約2,500円〜3,000円で、12種類もの異なる快感を一度に。
              <br />
              1つあたりわずか<strong className="text-yellow-400">約200円台</strong>という圧倒的なバリュー。
            </p>
            <ul className="space-y-3 mb-8">
              <li className="flex items-center text-neutral-300">
                <CheckIcon className="w-5 h-5 text-yellow-500 mr-2 flex-shrink-0" />
                迷ったらこれ。12個の個性が君を待つ
              </li>
              <li className="flex items-center text-neutral-300">
                <CheckIcon className="w-5 h-5 text-yellow-500 mr-2 flex-shrink-0" />
                お気に入りが見つかれば単品購入へ
              </li>
              <li className="flex items-center text-neutral-300">
                <CheckIcon className="w-5 h-5 text-yellow-500 mr-2 flex-shrink-0" />
                Amazonでベストセラーを記録中
              </li>
            </ul>
            <a 
              href="https://amzn.to/3N337IB" 
              target="_blank"
              rel="sponsored noopener noreferrer"
              className="block w-full text-center bg-yellow-500 hover:bg-yellow-400 text-neutral-950 font-black py-4 rounded-xl transition-transform active:scale-95 shadow-lg shadow-yellow-500/20"
            >
              Amazonで詳細をチェック →
            </a>
          </div>
          <a 
            href="https://amzn.to/3N337IB"
            target="_blank"
            rel="sponsored noopener noreferrer"
            className="relative group cursor-pointer block"
          >
            <img 
              src="/images/products/スクリーンショット 2025-12-27 22.51.41.png" 
              alt="TENGA EGG バラエティパック" 
              className="rounded-2xl border border-neutral-700 group-hover:border-yellow-500/50 transition-colors"
            />
            <div className="absolute top-4 right-4 bg-yellow-500 text-neutral-950 px-4 py-2 rounded-lg font-black text-sm rotate-3 shadow-lg">
              最強コスパ
            </div>
          </a>
        </div>
      </section>

      {/* Features */}
      <section className="space-y-12">
        <div className="text-center">
          <h2 className="text-3xl font-black mb-4 text-neutral-100">「手軽さ」という名の革命</h2>
          <p className="text-neutral-500">既存のオナホールを過去にする、圧倒的機動力。</p>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          <div className="bg-neutral-900 border border-neutral-800 rounded-2xl p-6 transition-all hover:border-yellow-500/50">
            <div className="text-yellow-500 text-3xl mb-4">💧</div>
            <h3 className="text-xl font-bold mb-3 text-neutral-100">水だけで楽しめる</h3>
            <p className="text-neutral-400 leading-relaxed text-sm">ローションすら不要。水さえあれば、いつでもどこでも最高の潤滑を実現。</p>
          </div>
          <div className="bg-neutral-900 border border-neutral-800 rounded-2xl p-6 transition-all hover:border-yellow-500/50">
            <div className="text-yellow-500 text-3xl mb-4">🔄</div>
            <h3 className="text-xl font-bold mb-3 text-neutral-100">洗って繰り返し使用</h3>
            <p className="text-neutral-400 leading-relaxed text-sm">実は数回の使用が可能。使い捨て感覚の手軽さと、複数回耐えうる耐久性を両立。</p>
          </div>
          <div className="bg-neutral-900 border border-neutral-800 rounded-2xl p-6 transition-all hover:border-yellow-500/50">
            <div className="text-yellow-500 text-3xl mb-4">↔️</div>
            <h3 className="text-xl font-bold mb-3 text-neutral-100">回転も自由自在</h3>
            <p className="text-neutral-400 leading-relaxed text-sm">コンパクトゆえに、手に収まり回転させるのも容易。ダイレクトな感触をコントロール。</p>
          </div>
        </div>

        <div className="bg-neutral-900 border border-neutral-800 rounded-2xl overflow-hidden">
          <div className="grid md:grid-cols-2">
            <div className="p-10 flex flex-col justify-center">
              <h3 className="text-2xl font-black mb-4 text-neutral-100">世界を驚かせたサイズ感</h3>
              <p className="text-neutral-400 mb-6">
                普通のオナホールより一回り小さいため、指先でひねったり、押し込んだり、通常のサイズでは不可能な「緻密な攻め」が可能になります。
              </p>
              <div className="flex items-center space-x-4">
                <div className="text-center">
                  <div className="text-yellow-500 font-black text-2xl">Small</div>
                  <div className="text-[10px] text-neutral-500 uppercase">Size</div>
                </div>
                <div className="h-8 w-[1px] bg-neutral-700"></div>
                <div className="text-center">
                  <div className="text-yellow-500 font-black text-2xl">Huge</div>
                  <div className="text-[10px] text-neutral-500 uppercase">Impact</div>
                </div>
              </div>
            </div>
            <div className="h-64 md:h-auto bg-neutral-800 bg-cover bg-center flex items-center justify-center">
              <span className="text-neutral-600 text-sm">商品画像</span>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Table */}
      <section className="space-y-8">
        <h2 className="text-center text-2xl font-black text-neutral-100">どっちから始める？</h2>
        
        <div className="grid md:grid-cols-2 gap-6">
          {/* Variety Pack */}
          <div className="relative border-2 border-yellow-500 rounded-3xl p-8 bg-neutral-900 shadow-xl shadow-yellow-500/10">
            <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-yellow-500 text-neutral-950 font-black px-6 py-1 rounded-full text-xs">
              人気No.1 / 最もお得
            </div>
            <h3 className="text-xl font-black mb-1 text-neutral-100">バラエティパック</h3>
            <p className="text-neutral-500 text-sm mb-6">12種類の全刺激を網羅</p>
            <div className="text-4xl font-black mb-8 text-neutral-100">
              ¥2,500 <span className="text-neutral-500 text-base font-normal">〜 3,000</span>
            </div>
            <ul className="space-y-4 mb-8 text-sm">
              <li className="flex items-center text-neutral-300">
                <CheckIcon className="w-5 h-5 text-yellow-500 mr-2 flex-shrink-0" />
                全12種類コンプリート
              </li>
              <li className="flex items-center text-neutral-300">
                <CheckIcon className="w-5 h-5 text-yellow-500 mr-2 flex-shrink-0" />
                1個あたり約220円の最安価格
              </li>
              <li className="flex items-center text-neutral-300">
                <CheckIcon className="w-5 h-5 text-yellow-500 mr-2 flex-shrink-0" />
                気に入った刺激を見つけられる
              </li>
            </ul>
            <a 
              href="https://amzn.to/3N337IB" 
              target="_blank"
              rel="sponsored noopener noreferrer"
              className="block w-full text-center bg-yellow-500 hover:bg-yellow-400 text-neutral-950 font-black py-3 rounded-xl transition-all"
            >
              今すぐパックを買う
            </a>
          </div>

          {/* Single Item */}
          <div className="border border-neutral-800 rounded-3xl p-8 bg-neutral-900/50 hover:border-neutral-700 transition-colors">
            <h3 className="text-xl font-black mb-1 text-neutral-100">単品お試し</h3>
            <p className="text-neutral-500 text-sm mb-6">特定のお気に入りを見つけたなら</p>
            <div className="text-4xl font-black mb-8 text-neutral-100">
              ¥500 <span className="text-neutral-500 text-base font-normal">前後</span>
            </div>
            <ul className="space-y-4 mb-8 text-sm">
              <li className="flex items-center text-neutral-400">
                <CheckIcon className="w-5 h-5 text-neutral-500 mr-2 flex-shrink-0" />
                特定の刺激をリピート
              </li>
              <li className="flex items-center text-neutral-400">
                <CheckIcon className="w-5 h-5 text-neutral-500 mr-2 flex-shrink-0" />
                必要な時に必要な分だけ
              </li>
              <li className="flex items-center text-neutral-400">
                <CheckIcon className="w-5 h-5 text-neutral-500 mr-2 flex-shrink-0" />
                収納場所に困らない
              </li>
            </ul>
            <a 
              href="https://amzn.to/4p9vWk1" 
              target="_blank"
              rel="sponsored noopener noreferrer"
              className="block w-full text-center border border-neutral-700 hover:border-neutral-500 text-neutral-300 font-bold py-3 rounded-xl transition-all"
            >
              単品リストを見る
            </a>
          </div>
        </div>
      </section>

      {/* Footer CTA */}
      <footer className="mt-24 space-y-12">
        <div className="text-center space-y-4">
          <div className="flex justify-center mb-6">
            <div className="w-12 h-12 rounded-xl bg-yellow-500/10 flex items-center justify-center border border-yellow-500/20">
              <HeartPulse className="w-6 h-6 text-yellow-500" />
            </div>
          </div>
          <h2 className="text-2xl font-black text-neutral-100">「抜く」ことは最高の健康法である</h2>
          <p className="text-neutral-500 max-w-lg mx-auto leading-relaxed">
            我慢しすぎることはストレスを招き、パフォーマンスの低下を引き起こします。<br />
            適切な「排出」こそが、若々しさと活力を保つ秘訣。今すぐ自分への投資を始めてください。
          </p>
        </div>

        <div className="bg-gradient-to-r from-yellow-600 to-yellow-400 p-8 rounded-3xl text-neutral-950 text-center shadow-2xl shadow-yellow-500/30">
          <h3 className="text-3xl font-black mb-4">賢者のための「卵」を手に入れろ</h3>
          <p className="font-bold mb-8 opacity-80">この刺激、一度知ったらもう戻れない。</p>
          <div className="flex flex-col md:flex-row gap-4 justify-center">
            <a 
              href="https://amzn.to/3N337IB" 
              target="_blank"
              rel="sponsored noopener noreferrer"
              className="bg-neutral-950 text-white px-8 py-4 rounded-xl font-black hover:scale-105 transition-transform inline-flex items-center justify-center"
            >
              🛒 12種パックを購入
            </a>
            <a 
              href="https://amzn.to/4p9vWk1" 
              target="_blank"
              rel="sponsored noopener noreferrer"
              className="bg-white/20 backdrop-blur-md text-neutral-950 px-8 py-4 rounded-xl font-black hover:bg-white/30 transition-all inline-flex items-center justify-center"
            >
              まずは単品をチェック
            </a>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default TengaEggPromoSection

