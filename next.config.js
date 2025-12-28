/** @type {import('next').NextConfig} */
const nextConfig = {
  // カラフルボックスなどの静的ホスティング用に設定
  output: 'export', // 静的サイトとしてエクスポート
  
  // トレイリングスラッシュを有効化（ディレクトリ構造を維持し、404エラーを防ぐ）
  trailingSlash: true,
  
  images: {
    // 静的エクスポート時は画像最適化を無効化（必須）
    unoptimized: true,
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

