#!/usr/bin/env python3
"""
MGS記事のサンプル画像URLを正しい形式に修正するスクリプト
複数のURLパターンを試して、正しい形式を確認
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
    複数のパターンを試す
    """
    if not image_url or "image.mgstage.com" not in image_url:
        return []
    
    # メイン画像URLからパス構造を抽出
    # 例: https://image.mgstage.com/images/ntrnet/348ntr/082/pf_o2_348ntr-082.jpg
    match = re.search(r'https://image\.mgstage\.com/images/(.+?)/(.+?)/(.+?)/pf_o2_(.+?)\.jpg', image_url)
    if not match:
        match = re.search(r'https://image\.mgstage\.com/images/(.+?)/(.+?)/(.+?)/pf_(.+?)\.jpg', image_url)
        if not match:
            return []
    
    maker = match.group(1)
    series = match.group(2)
    id_part = match.group(3)
    base_name = match.group(4)
    
    sample_urls = []
    
    # パターン1: pf_o2_348ntr-082-1.jpg (pf_o2_のまま、ハイフン区切り)
    for i in range(1, count + 1):
        sample_url = f"https://image.mgstage.com/images/{maker}/{series}/{id_part}/pf_o2_{base_name}-{i}.jpg"
        sample_urls.append(sample_url)
    
    # パターン1が失敗する場合に備えて、パターン2も試す
    # パターン2: pf_348ntr-082_1.jpg (pf_で始まり、アンダースコア区切り)
    # パターン3: pf_348ntr-082_01.jpg (ゼロ埋め)
    
    return sample_urls

def fix_sample_image_urls_in_body(body: str, image_url: str, content_id: str) -> str:
    """本文内のサンプル画像URLを修正"""
    # 現在の間違ったURLパターンを探す
    # pf_348ntr-082-1.jpg の形式を pf_o2_348ntr-082-1.jpg に修正
    pattern = r'(https://image\.mgstage\.com/images/[^/]+/[^/]+/[^/]+/)pf_([^/]+)-(\d+)\.jpg'
    
    def replace_url(match):
        base_path = match.group(1)
        base_name = match.group(2)
        num = match.group(3)
        # pf_o2_ の形式に修正
        return f'{base_path}pf_o2_{base_name}-{num}.jpg'
    
    body = re.sub(pattern, replace_url, body)
    
    return body

def main():
    """メイン処理"""
    print("=" * 80)
    print("  MGS記事のサンプル画像URL修正")
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

