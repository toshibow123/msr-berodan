'use client'

interface MgsAd728x90Props {
  htmlFile?: string
  className?: string
}

export default function MgsAd728x90({ 
  htmlFile = '/ads/mgs-728x90-1.html',
  className = ''
}: MgsAd728x90Props) {
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
          width="728"
          height="90"
          frameBorder="0"
          scrolling="no"
          style={{
            border: 'none',
            overflow: 'hidden'
          }}
          title="MGStage Ad 728x90"
        />
      </div>
    </div>
  )
}

