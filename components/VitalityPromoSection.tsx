'use client'

import React from 'react'
import VitalityProductCard from './VitalityProductCard'

// アイコンをSVGで実装（React 19互換性のため）
const BatteryCharging = ({ className }: { className?: string }) => (
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
    <path d="M15 7h1a2 2 0 0 1 2 2v6a2 2 0 0 1-2 2h-1" />
    <path d="M6 7H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2" />
    <line x1="22" y1="11" x2="22" y2="13" />
    <line x1="11" y1="6" x2="11" y2="18" />
    <rect x="7" y="11" width="4" height="2" rx="1" />
  </svg>
)

const Zap = ({ className }: { className?: string }) => (
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
    <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
  </svg>
)

const Activity = ({ className }: { className?: string }) => (
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
    <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
  </svg>
)

const VitalityPromoSection: React.FC = () => {
  return (
    <div className="space-y-12 animate-fade-in my-16">
      {/* SPONSORED CONTENT 区切り線 */}
      <div className="w-full border-t border-neutral-800 relative">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-neutral-950 px-6 py-2 text-yellow-500 font-bold tracking-widest text-sm">
          PR・SPONSORED CONTENT
        </div>
      </div>

      {/* Shocking Headline */}
      <section className="text-center space-y-4">
        <div className="inline-block bg-red-900/30 text-red-500 px-4 py-1 rounded-full text-xs font-bold mb-2 border border-red-500/20">
          ⚠️ 深刻な社会的リスク
        </div>
        <h3 className="text-3xl md:text-5xl font-extrabold text-neutral-100 leading-tight">
          なぜ、日本の男性は<br />
          <span className="text-yellow-500">「抜かなく」</span>なったのか？
        </h3>
        <p className="text-neutral-400 text-lg">
          統計が示す驚愕の事実。それは「草食化」ではなく、単なる「栄養不足」でした。
        </p>
      </section>

      {/* Data/Problem Section */}
      <section className="grid md:grid-cols-2 gap-8 items-center bg-neutral-900/50 p-6 md:p-10 rounded-2xl border border-neutral-800">
        <div className="space-y-6">
          <h4 className="text-xl font-bold text-yellow-500">オナニー回数の減少は「亜鉛」の枯渇サイン</h4>
          <p className="text-neutral-300 text-sm leading-relaxed">
            最新の調査によると、日本人男性のマスターベーション頻度は世界的に見ても著しく低い傾向にあります。
            その最大の原因とされているのが、現代社会における<span className="text-neutral-100 font-bold underline decoration-yellow-500">慢性的な亜鉛不足</span>です。
          </p>
          <ul className="space-y-3">
            {[
              "射精による亜鉛の大量消費",
              "加工食品中心の食生活による摂取不足",
              "ストレスによる吸収率の低下"
            ].map((text, i) => (
              <li key={i} className="flex items-center gap-3 text-neutral-400 text-sm">
                <div className="w-1.5 h-1.5 bg-yellow-500 rounded-full" />
                {text}
              </li>
            ))}
          </ul>
        </div>
        <div className="bg-neutral-950/50 p-6 rounded-xl border border-neutral-700 flex flex-col items-center justify-center space-y-4">
          <div className="relative w-32 h-32 md:w-40 md:h-40">
            <svg viewBox="0 0 36 36" className="w-full h-full transform -rotate-90">
              <path
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                fill="none"
                stroke="#27272a"
                strokeWidth="2.5"
              />
              <path
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                fill="none"
                stroke="#f59e0b"
                strokeWidth="2.5"
                strokeDasharray="25, 100"
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-3xl font-bold text-neutral-100">25%</span>
              <span className="text-[10px] text-neutral-500">充足率（平均）</span>
            </div>
          </div>
          <p className="text-xs text-neutral-500 text-center">※現代日本人男性に必要な亜鉛量の目安</p>
        </div>
      </section>

      {/* 各国比較セクション */}
      <section className="bg-neutral-900/50 p-6 md:p-10 rounded-2xl border border-neutral-800">
        <h4 className="text-xl font-bold text-yellow-500 mb-6 text-center">
          世界を比べてみると、日本のオナニー平均回数は少ない
        </h4>
        
        <div className="space-y-4 max-w-3xl mx-auto">
          {[
            { country: 'ブラジル', value: 18.5, color: 'bg-green-500' },
            { country: 'イタリア', value: 15.2, color: 'bg-blue-500' },
            { country: 'アメリカ', value: 12.8, color: 'bg-indigo-500' },
            { country: 'フランス', value: 11.5, color: 'bg-purple-500' },
            { country: 'ドイツ', value: 10.3, color: 'bg-cyan-500' },
            { country: '韓国', value: 9.1, color: 'bg-orange-500' },
            { country: '日本', value: 8.0, color: 'bg-red-500' },
          ].map((item, index) => {
            const maxValue = 18.5
            const percentage = (item.value / maxValue) * 100
            return (
              <div key={index} className="space-y-1.5">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-neutral-300 font-medium min-w-[80px]">{item.country}</span>
                  <span className="text-neutral-400 text-xs">
                    {item.value % 1 === 0 ? item.value : item.value.toFixed(1)}回/月
                    {item.country === '日本' && <span className="text-neutral-500 ml-1">(週2回)</span>}
                  </span>
                </div>
                <div className="relative w-full h-6 bg-neutral-800 rounded-full overflow-hidden">
                  <div
                    className={`${item.color} h-full rounded-full transition-all duration-500 flex items-center justify-end pr-2`}
                    style={{ width: `${percentage}%` }}
                  >
                    {percentage < 50 && (
                      <span className="text-white text-xs font-bold">
                        {item.value % 1 === 0 ? item.value : item.value.toFixed(1)}
                      </span>
                    )}
                  </div>
                </div>
              </div>
            )
          })}
        </div>
        
        <p className="text-xs text-neutral-500 text-center mt-6 leading-relaxed">
          ※上記のデータは統計調査に基づく平均値であり、個人差が大きく、個人によって異なります。あくまで参考値としてご覧ください。
        </p>
      </section>

      {/* Solution 1: Supplements */}
      <section className="space-y-6">
        <div className="flex items-center gap-4">
          <div className="bg-yellow-500 p-2 rounded-lg">
            <BatteryCharging className="text-neutral-950 w-6 h-6" />
          </div>
          <div>
            <h4 className="text-2xl font-bold text-neutral-100 tracking-tight">内部から「溢れる」欲望を。</h4>
            <p className="text-neutral-500 text-sm">まずは身体のベースを整える亜鉛補給</p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <VitalityProductCard
            title="男の亜鉛サプリドバッと！＋Vitamin C たっぷり30日分"
            description="亜鉛25mg吸収率にこだわったサプリ"
            tag="売れ筋No.1"
            imageUrl="/images/products/スクリーンショット 2025-12-27 9.06.59.png"
            affiliateUrl="https://al.fanza.co.jp/?lurl=https%3A%2F%2Fwww.dmm.co.jp%2Fmono%2Fgoods%2F-%2Fdetail%2F%3D%2Fcid%3Dstoreago00136unub0tylxy%2F&af_id=toshichan-002&ch=search_link&ch_id=link"
          />
          <VitalityProductCard
            title="マカ＆シトルリン Plus"
            description="亜鉛に加えて、血管拡張をサポートするシトルリンを配合。圧倒的硬度。"
            tag="即効性重視"
            imageUrl="/images/products/スクリーンショット 2025-12-28 13.01.52.png"
            affiliateUrl="https://amzn.to/48X2Wap"
          />
        </div>
      </section>

      {/* Solution 2: Goods */}
      <section className="space-y-6">
        <div className="flex items-center gap-4">
          <div className="bg-indigo-600 p-2 rounded-lg">
            <Zap className="text-white w-6 h-6" />
          </div>
          <div>
            <h4 className="text-2xl font-bold text-neutral-100 tracking-tight">溢れる力を、最高の「快感」へ。</h4>
            <p className="text-neutral-500 text-sm">溜まったエネルギーを解き放つ至高のツール</p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <VitalityProductCard
            title="おなつゆ トイズハート"
            description="人肌を超える弾力と潤い。亜鉛で高まった感度を逃さない。"
            tag="殿堂入り"
            imageUrl="/images/products/スクリーンショット 2025-12-28 13.17.40.png"
            affiliateUrl="https://amzn.to/3KNwJJy"
            isGood
          />
          <VitalityProductCard
            title="TENGA テンガ プレミアム・オリジナルバキューム・カップ"
            description="最新のバイブレーション機能と連動。脳がとろける没入感。"
            tag="最新テクノロジー"
            imageUrl="/images/products/スクリーンショット 2025-12-28 13.18.45.png"
            affiliateUrl="https://amzn.to/48YEe9L"
            isGood
          />
        </div>
      </section>

      {/* Scientific Explanation */}
      <section className="bg-neutral-800/20 p-8 rounded-2xl text-center space-y-4 border border-neutral-800">
        <div className="mb-6">
          <img 
            src="/images/スクリーンショット 2025-12-27 23.13.26.png" 
            alt="「抜く」ことは最高の健康法である" 
            className="max-w-full h-auto mx-auto rounded-lg"
          />
        </div>
        <Activity className="mx-auto text-yellow-500 w-10 h-10 mb-2" />
        <h5 className="text-lg font-bold text-neutral-100">「抜く」ことは最高の健康法である</h5>
        <p className="text-neutral-400 text-sm leading-relaxed max-w-2xl mx-auto">
          射精を我慢することは、テストステロンの低下を招き、結果として老化を早めます。
          適切な亜鉛補給と、質の高いオナニー習慣こそが、若々しさを保つ秘訣です。
          今すぐ自分への投資を始めてください。
        </p>
      </section>
    </div>
  )
}

export default VitalityPromoSection

