'use client'

import React from 'react'

interface VitalityProductCardProps {
  title: string
  description: string
  price?: string
  tag: string
  imageUrl: string
  isGood?: boolean
  affiliateUrl?: string
}

// ExternalLinkアイコンをSVGで実装
const ExternalLink = ({ className }: { className?: string }) => (
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
    <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
    <polyline points="15 3 21 3 21 9" />
    <line x1="10" y1="14" x2="21" y2="3" />
  </svg>
)

const VitalityProductCard: React.FC<VitalityProductCardProps> = ({
  title,
  description,
  price,
  tag,
  imageUrl,
  isGood = false,
  affiliateUrl = '#'
}) => {
  return (
    <div className={`group relative bg-neutral-900 border ${isGood ? 'border-indigo-500/20' : 'border-neutral-800'} rounded-xl overflow-hidden transition-all duration-300 hover:scale-[1.02] hover:shadow-[0_0_20px_rgba(245,158,11,0.1)]`}>
      <div className="absolute top-2 left-2 z-10">
        <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-tighter ${isGood ? 'bg-indigo-600 text-white' : 'bg-yellow-500 text-neutral-950'}`}>
          {tag}
        </span>
      </div>
      
      <div className="aspect-[16/10] w-full overflow-hidden bg-neutral-800">
        <img
          src={imageUrl}
          alt={title}
          className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
        />
      </div>

      <div className="p-3 space-y-1.5">
        <h5 className="text-neutral-100 font-bold text-base group-hover:text-yellow-400 transition-colors">{title}</h5>
        <p className="text-neutral-500 text-xs leading-relaxed line-clamp-2">
          {description}
        </p>
        
        <div className="flex items-center justify-end pt-1.5">
          <a
            href={affiliateUrl}
            target="_blank"
            rel="sponsored noopener noreferrer"
            className={`flex items-center gap-2 px-4 py-2 rounded-lg font-bold text-xs transition-colors ${isGood ? 'bg-indigo-600 hover:bg-indigo-500 text-white' : 'bg-yellow-500 hover:bg-yellow-400 text-neutral-950'}`}
          >
            詳細を見る
            <ExternalLink className="w-3.5 h-3.5" />
          </a>
        </div>
      </div>
    </div>
  )
}

export default VitalityProductCard

