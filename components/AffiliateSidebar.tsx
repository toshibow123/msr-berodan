'use client'

interface AffiliateSidebarProps {
  className?: string
}

export default function AffiliateSidebar({ className = '' }: AffiliateSidebarProps) {
  return (
    <aside className={`w-80 space-y-6 hidden md:flex md:flex-col ${className}`}>
      {/* FANZA広告 */}
      <div className="bg-[var(--elegant-bg-light)] rounded-xl p-4 border border-[var(--elegant-border)] shadow-lg">
        <div className="text-center mb-3">
          <span className="text-xs text-[var(--elegant-text-dark)] font-medium bg-[var(--elegant-bg)] px-3 py-1 rounded-full border border-[var(--elegant-border)]">
            PR・FANZA
          </span>
        </div>
        <div className="flex justify-center">
          <iframe
            src="/ads/fanza-300.html"
            width={300}
            height={250}
            scrolling="no"
            frameBorder="0"
            style={{
              border: 'none',
              display: 'block',
              backgroundColor: 'transparent'
            }}
            title="FANZA広告"
            loading="lazy"
          />
        </div>
      </div>

      {/* MGS SuperCH広告 */}
      <div className="bg-[var(--elegant-bg-light)] rounded-xl p-4 border border-[var(--elegant-border)] shadow-lg">
        <div className="text-center mb-3">
          <span className="text-xs text-[var(--elegant-text-dark)] font-medium bg-[var(--elegant-bg)] px-3 py-1 rounded-full border border-[var(--elegant-border)]">
            PR・MGS SuperCH
          </span>
        </div>
        <div className="flex justify-center">
          <iframe
            src="/ads/mgs-300x250.html"
            width={300}
            height={250}
            frameBorder="0"
            scrolling="no"
            style={{
              border: 'none',
              overflow: 'hidden'
            }}
            title="MGS SuperCH広告"
          />
        </div>
      </div>

      {/* 検索・フィルター機能 */}
      <div className="bg-[var(--elegant-bg-light)] rounded-xl p-6 border border-[var(--elegant-border)]">
        <h3 className="text-lg font-serif text-[var(--elegant-wine)] mb-4">検索・絞り込み</h3>
        <div className="space-y-4">
          <input
            type="text"
            placeholder="女優名で検索..."
            className="w-full px-4 py-2 bg-[var(--elegant-bg)] rounded border border-[var(--elegant-border)] text-[var(--elegant-text)] placeholder:text-[var(--elegant-text-dark)] focus:outline-none focus:border-[var(--elegant-wine)] transition-colors"
          />
          <select className="w-full px-4 py-2 bg-[var(--elegant-bg)] rounded border border-[var(--elegant-border)] text-[var(--elegant-text)] focus:outline-none focus:border-[var(--elegant-wine)] transition-colors">
            <option value="all">すべての作品数</option>
            <option value="10plus">10作品以上</option>
            <option value="5plus">5作品以上</option>
            <option value="3plus">3作品以上</option>
          </select>
        </div>
      </div>

      {/* 人気女優 */}
      <div className="bg-[var(--elegant-bg-light)] rounded-xl p-6 border border-[var(--elegant-border)]">
        <h3 className="text-lg font-serif text-[var(--elegant-wine)] mb-4">人気女優 TOP5</h3>
        <div className="space-y-3">
          {[
            { name: '篠田ゆう', works: 45 },
            { name: '君島みお', works: 38 },
            { name: '森沢かな', works: 32 },
            { name: '波多野結衣', works: 28 },
            { name: '水野朝陽', works: 25 }
          ].map((actress, index) => (
            <div key={actress.name} className="flex items-center gap-3 p-2 rounded hover:bg-[var(--elegant-bg-lighter)] transition-colors">
              <div className="text-[var(--elegant-gold)] font-bold text-sm w-6 text-center">
                {index + 1}
              </div>
              <div className="flex-1">
                <div className="text-[var(--elegant-text)] text-sm font-medium">
                  {actress.name}
                </div>
                <div className="text-[var(--elegant-text-dark)] text-xs">
                  {actress.works}作品
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 統計情報 */}
      <div className="bg-[var(--elegant-bg-light)] rounded-xl p-6 border border-[var(--elegant-border)]">
        <h3 className="text-lg font-serif text-[var(--elegant-wine)] mb-4">統計</h3>
        <div className="space-y-2 text-sm text-[var(--elegant-text-light)]">
          <div className="flex justify-between">
            <span>登録女優数</span>
            <span className="font-semibold text-[var(--elegant-wine)]">
              1,200+人
            </span>
          </div>
          <div className="flex justify-between">
            <span>総作品数</span>
            <span className="font-semibold text-[var(--elegant-wine)]">
              8,500+作品
            </span>
          </div>
          <div className="flex justify-between">
            <span>最新更新</span>
            <span className="font-semibold text-[var(--elegant-wine)]">
              毎日
            </span>
          </div>
        </div>
      </div>

      {/* MGS人妻チャンネル広告 */}
      <div className="bg-[var(--elegant-bg-light)] rounded-xl p-4 border border-[var(--elegant-border)] shadow-lg">
        <div className="text-center mb-3">
          <span className="text-xs text-[var(--elegant-text-dark)] font-medium bg-[var(--elegant-bg)] px-3 py-1 rounded-full border border-[var(--elegant-border)]">
            PR・MGS 人妻チャンネル
          </span>
        </div>
        <div className="flex justify-center">
          <iframe
            src="/ads/mgs-hitotuma-234x60.html"
            width={234}
            height={60}
            frameBorder="0"
            scrolling="no"
            style={{
              border: 'none',
              overflow: 'hidden'
            }}
            title="MGS人妻チャンネル広告"
          />
        </div>
      </div>

      {/* お知らせ */}
      <div className="bg-[var(--elegant-bg-light)] rounded-xl p-6 border border-[var(--elegant-border)]">
        <h3 className="text-lg font-serif text-[var(--elegant-wine)] mb-4">お知らせ</h3>
        <div className="space-y-3 text-sm text-[var(--elegant-text-light)]">
          <div className="p-3 bg-[var(--elegant-bg)] rounded border border-[var(--elegant-border)]">
            <div className="text-[var(--elegant-wine)] font-semibold mb-1">新機能追加</div>
            <div>女優別ページで作品をより見やすく表示できるようになりました。</div>
          </div>
          <div className="p-3 bg-[var(--elegant-bg)] rounded border border-[var(--elegant-border)]">
            <div className="text-[var(--elegant-wine)] font-semibold mb-1">サイト更新</div>
            <div>毎日新しい作品情報を追加しています。</div>
          </div>
        </div>
      </div>

      {/* 免責事項 */}
      <div className="bg-[var(--elegant-bg-light)] rounded-xl p-4 border border-[var(--elegant-border)] text-center">
        <div className="text-xs text-[var(--elegant-text-dark)] space-y-1">
          <div>※このサイトは18歳未満の方の閲覧を禁止しています。</div>
          <div>※広告・アフィリエイトリンクが含まれています。</div>
          <div>※作品の詳細は各配信サイトでご確認ください。</div>
        </div>
      </div>
    </aside>
  )
}