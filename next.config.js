/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'pics.dmm.co.jp',
        pathname: '/**',
      },
    ],
  },
  // 本番環境の最適化設定
  compress: true, // gzip圧縮を有効化
  poweredByHeader: false, // X-Powered-Byヘッダーを非表示（セキュリティ）
  reactStrictMode: true, // React Strict Modeを有効化
  // Turbopack設定（Next.js 16ではデフォルトでTurbopackが有効）
  turbopack: {},
}

module.exports = nextConfig

