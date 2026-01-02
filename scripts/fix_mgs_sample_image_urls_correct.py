#!/usr/bin/env python3
"""
MGS記事のサンプル画像URLを正しい形式に修正するスクリプト
cap_e_{画像番号}_{商品ID}.jpg の形式に修正
"""

import re
import json
from pathlib import Path

# プロジェクトルート
script_dir = Path(__file__).parent
project_root = script_dir.parent
content_dir = project_root / "content"

def extract_frontmatter(content: str) -> tuple[dict, str]:
    """フロントマターを抽出"""
    if not content.startswith("---"):
        return {}, content
    
    end_pos = content.find("\n---", 3)
    if end_pos == -1:
        return {}, content
    
    frontmatter_text = content[4:end_pos].strip()
    body = content[end_pos + 5:].strip()
    
    frontmatter = {}
    for line in frontmatter_text.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().strip('"')
            frontmatter[key] = value
    
    return frontmatter, body

def generate_mgs_sample_image_urls(image_url: str, content_id: str, count: int = 3) -> list[str]:
    """
    MGSのメイン画像URLからサンプル画像URLを生成
    形式: https://image.mgstage.com/images/{maker}/{series}/{id}/cap_e_{画像番号}_{商品ID}.jpg
    
    例:
    メイン画像: https://image.mgstage.com/images/ntrnet/348ntr/082/pf_o2_348ntr-082.jpg
    サンプル画像: https://image.mgstage.com/images/ntrnet/348ntr/082/cap_e_1_348ntr-082.jpg
                 https://image.mgstage.com/images/ntrnet/348ntr/082/cap_e_2_348ntr-082.jpg
                 https://image.mgstage.com/images/ntrnet/348ntr/082/cap_e_3_348ntr-082.jpg
    """
    if not image_url or "image.mgstage.com" not in image_url:
        return []
    
    # メイン画像URLからパス構造を抽出
    # 例: https://image.mgstage.com/images/ntrnet/348ntr/082/pf_o2_348ntr-082.jpg
    match = re.search(r'https://image\.mgstage\.com/images/(.+?)/(.+?)/(.+?)/', image_url)
    if not match:
        return []
    
    maker = match.group(1)
    series = match.group(2)
    id_part = match.group(3)
    
    # content_idを小文字に変換（348NTR-082 -> 348ntr-082）
    content_id_lower = content_id.lower()
    
    # サンプル画像URLを生成
    sample_urls = []
    for i in range(1, count + 1):
        sample_url = f"https://image.mgstage.com/images/{maker}/{series}/{id_part}/cap_e_{i}_{content_id_lower}.jpg"
        sample_urls.append(sample_url)
    
    return sample_urls

def fix_sample_image_urls_in_body(body: str, image_url: str, content_id: str) -> str:
    """本文内のサンプル画像URLを修正"""
    # 現在の間違ったURLパターンを全て探して置き換える
    # pf_o2_348ntr-082-1.jpg や pf_348ntr-082-1.jpg の形式を cap_e_1_348ntr-082.jpg に修正
    
    # メイン画像URLからパス構造を抽出
    match = re.search(r'https://image\.mgstage\.com/images/(.+?)/(.+?)/(.+?)/', image_url)
    if not match:
        return body
    
    maker = match.group(1)
    series = match.group(2)
    id_part = match.group(3)
    content_id_lower = content_id.lower()
    
    # 既存のサンプル画像URLパターンを全て置き換え
    # パターン1: pf_o2_348ntr-082-1.jpg
    pattern1 = rf'https://image\.mgstage\.com/images/{re.escape(maker)}/{re.escape(series)}/{re.escape(id_part)}/pf_o2_[^/]+-(\d+)\.jpg'
    def replace1(m):
        num = m.group(1)
        return f'https://image.mgstage.com/images/{maker}/{series}/{id_part}/cap_e_{num}_{content_id_lower}.jpg'
    body = re.sub(pattern1, replace1, body)
    
    # パターン2: pf_348ntr-082-1.jpg
    pattern2 = rf'https://image\.mgstage\.com/images/{re.escape(maker)}/{re.escape(series)}/{re.escape(id_part)}/pf_[^/]+-(\d+)\.jpg'
    def replace2(m):
        num = m.group(1)
        return f'https://image.mgstage.com/images/{maker}/{series}/{id_part}/cap_e_{num}_{content_id_lower}.jpg'
    body = re.sub(pattern2, replace2, body)
    
    return body

def main():
    """メイン処理"""
    print("=" * 80)
    print("  MGS記事のサンプル画像URL修正（cap_e形式）")
    print("=" * 80 + "\n")
    
    mgs_articles = list(content_dir.glob("2026-01-02-*.md"))
    
    if not mgs_articles:
        print("❌ 修正対象の記事が見つかりません")
        return
    
    print(f"📋 {len(mgs_articles)}件の記事を修正します\n")
    
    fixed_count = 0
    skipped_count = 0
    
    for article_file in mgs_articles:
        try:
            with open(article_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            frontmatter, body = extract_frontmatter(content)
            
            if not frontmatter:
                print(f"⏭️  {article_file.name} - フロントマターが見つかりません")
                skipped_count += 1
                continue
            
            source = frontmatter.get("source", "")
            if source != "MGS":
                print(f"⏭️  {article_file.name} - MGS記事ではありません")
                skipped_count += 1
                continue
            
            image_url = frontmatter.get("image", "")
            content_id = frontmatter.get("contentId", "")
            
            if not image_url or not content_id:
                print(f"⏭️  {article_file.name} - 必要な情報が不足しています")
                skipped_count += 1
                continue
            
            # サンプル画像URLを修正
            new_body = fix_sample_image_urls_in_body(body, image_url, content_id)
            
            # フロントマターを再構築
            frontmatter_lines = ["---"]
            frontmatter_lines.append(f'title: "{frontmatter.get("title", "").replace('"', '\\"')}"')
            frontmatter_lines.append(f'date: "{frontmatter.get("date", "")}"')
            frontmatter_lines.append(f'excerpt: "{frontmatter.get("excerpt", "").replace('"', '\\"')}"')
            frontmatter_lines.append(f'image: "{frontmatter.get("image", "")}"')
            
            # tagsを正しく処理
            tags = frontmatter.get("tags", [])
            if isinstance(tags, str):
                try:
                    tags = json.loads(tags)
                except:
                    tags = []
            frontmatter_lines.append(f'tags: {json.dumps(tags, ensure_ascii=False)}')
            
            frontmatter_lines.append(f'affiliateLink: "{frontmatter.get("affiliateLink", "")}"')
            frontmatter_lines.append(f'contentId: "{frontmatter.get("contentId", "")}"')
            frontmatter_lines.append(f'rating: {frontmatter.get("rating", "4.0")}')
            frontmatter_lines.append(f'source: "MGS"')
            frontmatter_lines.append("---")
            
            new_content = "\n".join(frontmatter_lines) + "\n\n" + new_body
            
            with open(article_file, "w", encoding="utf-8") as f:
                f.write(new_content)
            
            print(f"✅ {article_file.name} - 修正完了")
            fixed_count += 1
                
        except Exception as e:
            print(f"❌ {article_file.name} - エラー: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 80)
    print(f"🎉 修正完了！")
    print(f"   修正: {fixed_count}件")
    print(f"   スキップ: {skipped_count}件")
    print("=" * 80)

if __name__ == "__main__":
    main()

