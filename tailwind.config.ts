import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // 平成レトロ・男性向けカラーパレット
        'retro-bg': '#1a1a1a', // ダークグレー（背景）
        'retro-bg-light': '#2a2a2a', // ライトグレー（カード背景）
        'retro-gold': '#d4a574', // 落ち着いたゴールド（アクセント）
        'retro-gold-hover': '#e6b886', // ゴールド（ホバー）
        'retro-cream': '#f5f5dc', // クリーム（テキスト）
        'retro-text': '#e0e0e0', // ライトグレー（テキスト）
        'retro-text-dark': '#f5f5f5', // ほぼ白（見出し）
        'retro-border': '#3a3a3a', // ボーダー色
        'retro-accent': '#8b7355', // ブラウン（サブアクセント）
      },
    },
  },
  plugins: [],
}
export default config

