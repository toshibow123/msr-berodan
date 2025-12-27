import React from 'react'

interface AffiliateCardProps {
  imageUrl: string
  affiliateUrl: string
  altText?: string
  linkText?: string
}

/**
 * 記事内に配置するアフィリエイト画像カードコンポーネント
 * 中央揃え、影付き、クリック可能な見た目
 */
export default function AffiliateCard({
  imageUrl,
  affiliateUrl,
  altText = "おすすめ商品",
  linkText = "公式サイトで見る"
}: AffiliateCardProps) {
  return (
    <a
      href={affiliateUrl}
      target="_blank"
      rel="noopener noreferrer"
      className="affiliate-card"
    >
      <img
        src={imageUrl}
        alt={altText}
      />
      <span className="affiliate-link-text">{linkText}</span>
    </a>
  )
}

