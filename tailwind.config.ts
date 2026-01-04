import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/AffiliateAdMock.tsx',
    './components/AffiliateSidebar.tsx',
    './components/FanzaSubscriptionPromo.tsx',
    './components/FanzaTvSidebarBanner.tsx',
    './components/IframeAd.tsx',
    './components/InFeedAdCard.tsx',
    './components/MgsAd300x250.tsx',
    './components/MgsAd728x90.tsx',
    './components/MgsBanner.tsx',
    './components/Sidebar.tsx',
    './components/TopPageContent.tsx',
    './components/VitalityPromoSection.tsx',
    './components/VitalityProductCard.tsx',
    './components/WorkFeedCard.tsx',
  ],
  theme: {
    extend: {
      colors: {
        // ラグジュアリー・官能小説的カラーパレット（ダークテーマ）
        'elegant': {
          'wine': '#C97A9A', // 明るめのワインレッド（アクセント）
          'wine-dark': '#8B2252', // 深みのあるワインレッド（メインカラー）
          'wine-darker': '#5A1528', // ダークワインレッド
          'wine-light': '#E8A5C4', // ライトワインレッド
          'gold': '#D4AF37', // ゴールド（アクセント）
          'champagne': '#F0E68C', // シャンパンゴールド
          'bg': '#1A1A1A', // メイン背景（ほぼ黒）
          'bg-light': '#252525', // ライト背景（カード用）
          'bg-lighter': '#2F2F2F', // さらに明るい背景
          'text': '#E5E5E5', // メインテキスト（明るいグレー）
          'text-light': '#B8B8B8', // ライトテキスト
          'text-dark': '#8B8B8B', // ダークテキスト
          'border': '#3A3A3A', // ボーダー色（ダークグレー）
          'border-light': '#4A4A4A', // ライトボーダー
        },
      },
      fontFamily: {
        'serif-jp': ['Noto Serif JP', 'Yu Mincho', 'YuMincho', 'Hiragino Mincho ProN', 'serif'],
        'sans-jp': ['Noto Sans JP', 'Hiragino Kaku Gothic ProN', 'Yu Gothic', 'sans-serif'],
      },
      lineHeight: {
        'relaxed-plus': '1.9',
        'loose-plus': '2.0',
      },
    },
  },
  plugins: [],
}
export default config

