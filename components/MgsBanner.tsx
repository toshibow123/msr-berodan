'use client'

export default function MgsBanner() {
  return (
    <div className="my-8">
      <div className="flex flex-col items-center gap-2 mb-2">
        <span className="text-xs text-elegant-text-dark font-medium bg-elegant-bg-lighter px-3 py-1 rounded-full border border-elegant-border">
          PR・アフィリエイト広告
        </span>
      </div>
      <div className="flex justify-center">
        <iframe
          src="/ads/mgs.html"
          width="728"
          height="90"
          frameBorder="0"
          scrolling="no"
          style={{
            border: 'none',
            overflow: 'hidden'
          }}
          title="MGStage Banner Ad"
        />
      </div>
    </div>
  )
}

