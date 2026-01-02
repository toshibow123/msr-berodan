'use client'

interface MgsAd300x250Props {
  htmlFile?: string
  className?: string
}

export default function MgsAd300x250({ 
  htmlFile = '/ads/mgs-300x250.html',
  className = ''
}: MgsAd300x250Props) {
  return (
    <div className={`my-8 ${className}`}>
      <div className="flex flex-col items-center gap-2 mb-2">
        <span className="text-xs text-elegant-text-dark font-medium bg-elegant-bg-lighter px-3 py-1 rounded-full border border-elegant-border">
          PR・アフィリエイト広告
        </span>
      </div>
      <div className="flex justify-center">
        <iframe
          src={htmlFile}
          width="300"
          height="250"
          frameBorder="0"
          scrolling="no"
          style={{
            border: 'none',
            overflow: 'hidden'
          }}
          title="MGStage Ad 300x250"
        />
      </div>
    </div>
  )
}

