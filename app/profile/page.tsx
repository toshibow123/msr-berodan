import Link from 'next/link'

export default function ProfilePage() {
  return (
    <div className="max-w-4xl mx-auto">
      <Link 
        href="/"
        className="inline-block mb-8 text-retro-gold hover:text-retro-gold-hover transition-colors font-medium"
      >
        ← ホームに戻る
      </Link>

      <article className="card">
        <header className="mb-8 pb-8 border-b border-retro-border">
          <h1 className="text-4xl font-bold text-retro-gold mb-3">
            サイトについて
          </h1>
          <p className="text-retro-text text-lg">
            平成AV映像遺産 ー ビデオ黄金時代を知る愛好家によるレビューサイト
          </p>
        </header>

        <div className="prose max-w-none">
          <section className="mb-8">
            <h2 className="text-2xl font-bold text-retro-gold mb-4">
              このサイトのコンセプト
            </h2>
            <p className="text-retro-text mb-4 leading-relaxed">
              現代のAVは確かに画質が良い。4K、8K、最新の撮影技術。
              女優も綺麗だ。整形技術も発達し、「完璧な美人」が量産される時代。
            </p>
            <p className="text-retro-text mb-4 leading-relaxed">
              しかし、何かが足りない。**熱量が足りない**。
            </p>
            <p className="text-retro-text mb-4 leading-relaxed">
              このサイトは、2000年代〜2010年代の<strong className="text-retro-gold">「平成の名作」</strong>を再評価し、
              現代では作れない企画の狂気、女優の魂、生々しい映像美を語る場所です。
            </p>
          </section>

          <section className="mb-8 card bg-gradient-to-br from-retro-bg to-retro-bg-light">
            <h2 className="text-2xl font-bold text-retro-gold mb-4">
              なぜ旧作・名作なのか
            </h2>
            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <span className="text-2xl flex-shrink-0">🔥</span>
                <div>
                  <h3 className="font-bold text-retro-gold-hover mb-1">企画の狂気</h3>
                  <p className="text-retro-text text-sm">
                    今のコンプライアンス時代では絶対に作れない、頭のおかしい（褒め言葉）企画。
                    これこそが、平成AVの真骨頂だ。
                  </p>
                </div>
              </div>
              
              <div className="flex items-start gap-3">
                <span className="text-2xl flex-shrink-0">💪</span>
                <div>
                  <h3 className="font-bold text-retro-gold-hover mb-1">女優の覚悟</h3>
                  <p className="text-retro-text text-sm">
                    体当たりの演技、表情の作り込み、プロ根性。
                    今の「可愛いだけの女優」では絶対に出せない魂がある。
                  </p>
                </div>
              </div>
              
              <div className="flex items-start gap-3">
                <span className="text-2xl flex-shrink-0">📼</span>
                <div>
                  <h3 className="font-bold text-retro-gold-hover mb-1">生々しい映像美</h3>
                  <p className="text-retro-text text-sm">
                    SD画質の粗い粒子、4:3比率、荒い照明。
                    これが逆に「ドキュメント感」を生み、生々しさを際立たせる。
                  </p>
                </div>
              </div>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-bold text-retro-gold mb-4">
              対象となる読者
            </h2>
            <ul className="space-y-2 text-retro-text">
              <li className="flex items-start gap-2">
                <span className="text-retro-gold">✓</span>
                <span>現代の「綺麗すぎるだけのAV」に飽きている30代〜50代男性</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-retro-gold">✓</span>
                <span>2000年代〜2010年代のAVに懐かしさを感じる方</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-retro-gold">✓</span>
                <span>「画質の良さ」より「熱量」「企画の狂気」を求める方</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-retro-gold">✓</span>
                <span>ビデオ黄金時代を知る、または知りたい方</span>
              </li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-bold text-retro-gold mb-4">
              レビューの方針
            </h2>
            <p className="text-retro-text mb-4 leading-relaxed">
              このサイトのレビューは、「現代作品との対比」を頻繁に行います。
            </p>
            <ul className="space-y-2 text-retro-text mb-4">
              <li className="flex items-start gap-2">
                <span className="text-retro-gold">•</span>
                <span>「今の補正だらけの映像では、この汗の質感は出せない」</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-retro-gold">•</span>
                <span>「コンプラで雁字搦めの今とは違い、この頃の企画は本当に頭がおかしい」</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-retro-gold">•</span>
                <span>「この表情の作り込み、今の女優では絶対に出せない」</span>
              </li>
            </ul>
            <p className="text-retro-text mb-4 leading-relaxed">
              批判ではなく、**リスペクト**。悪口ではなく、**再評価**。
              それが、このサイトのスタンスです。
            </p>
          </section>

          <section className="bg-gradient-to-br from-retro-bg-light to-retro-border rounded-lg p-8 text-center">
            <h2 className="text-2xl font-bold text-retro-gold mb-4">
              執筆者より
            </h2>
            <p className="text-retro-text mb-4 leading-relaxed italic">
              平成という時代は、AVにとって黄金時代だった。
            </p>
            <p className="text-retro-text mb-4 leading-relaxed italic">
              企画は過激で、女優は体当たりで、映像は生々しかった。
            </p>
            <p className="text-retro-text mb-4 leading-relaxed italic">
              今の「綺麗なだけのAV」に飽きた人たちへ。
              一緒に、平成の名作を掘り起こしましょう。
            </p>
            <p className="text-retro-gold font-bold mt-6 text-lg">
              500円だろうが定価だろうが、これは映像遺産として持っておくべきだ。
            </p>
            <p className="text-retro-text/70 text-sm mt-4">
              — ビデオ黄金時代を知る愛好家
            </p>
          </section>
        </div>
      </article>
    </div>
  )
}
