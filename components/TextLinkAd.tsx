'use client'

interface TextLinkAdProps {
  text: string
  href: string
  className?: string
}

export default function TextLinkAd({ text, href, className = '' }: TextLinkAdProps) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer sponsored"
      className={`text-elegant-wine hover:text-elegant-wine-light underline decoration-elegant-wine/50 hover:decoration-elegant-wine transition-colors ${className}`}
    >
      {text}
    </a>
  )
}

