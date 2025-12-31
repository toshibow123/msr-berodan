'use client'

export default function MgsBanner() {
  const iframeContent = `
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8">
        <style>
          body {
            margin: 0;
            padding: 0;
            overflow: hidden;
          }
        </style>
      </head>
      <body>
        <script type="text/javascript" src="https://www.mgstage.com/afscript/superch/728_90/N2G56Q3UYEPYWXP7P8PKPRIDC3/"></script>
      </body>
    </html>
  `

  return (
    <div className="flex justify-center my-8">
      <iframe
        srcDoc={iframeContent}
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
  )
}

