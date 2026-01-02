#!/usr/bin/env python3
"""
MGS記事のサンプル画像をクリーンアップして修正するスクリプト
重複を削除し、正しいサンプル画像URLを設定
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
    """MGSのメイン画像URLからサンプル画像URLを生成"""
    if not image_url or "image.mgstage.com" not in image_url:
        return []
    
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
    for i in range(1, count + 1):
        sample_url = f"https://image.mgstage.com/images/{maker}/{series}/{id_part}/pf_{base_name}-{i}.jpg"
        sample_urls.append(sample_url)
    
    return sample_urls

def fix_sample_images_in_body(body: str, image_url: str, content_id: str, affiliate_url: str, title: str) -> str:
    """本文内のサンプル画像を修正（重複を削除）"""
    sample_urls = generate_mgs_sample_image_urls(image_url, content_id, count=3)
    
    if not sample_urls:
        sample_urls = [image_url] * 3
    
    # 「心に残るシーン」セクションを探す
    scene_section_match = re.search(r'## 心に残るシーン', body)
    
    if scene_section_match:
        section_start = scene_section_match.start()
        before_section = body[:section_start]
        after_section = body[section_start:]
        
        # 「読者への語りかけ」セクションを探す
        next_section_match = re.search(r'\n## 読者への語りかけ', after_section)
        if next_section_match:
            section_end = section_start + next_section_match.start()
            rest_body = body[section_end:]
        else:
            section_end = len(body)
            rest_body = ""
        
        # 「心に残るシーン」から「読者への語りかけ」までの部分を取得
        section_body = body[section_start:section_end]
        
        # セクション内の全ての画像タグを削除（複数行対応）
        img_pattern = r'<a href="[^"]*" target="_blank" rel="sponsored noopener noreferrer">\s*<img src="[^"]*"[^>]*/>\s*</a>\s*\n?'
        section_body = re.sub(img_pattern, '', section_body, flags=re.MULTILINE)
        
        # 「この名作を確認する」リンクを探す
        link_pattern = r'<div className="affiliate-link-inline">[^<]*</div>'
        link_match = re.search(link_pattern, section_body)
        
        # サンプル画像を生成
        images_html = "\n\n"
        for sample_url in sample_urls:
            images_html += f'<a href="{affiliate_url}" target="_blank" rel="sponsored noopener noreferrer">\n  <img src="{sample_url}" alt="{title}" />\n</a>\n\n'
        
        if link_match:
            # リンクの前に画像を挿入
            insert_pos = link_match.start()
            section_body = section_body[:insert_pos] + images_html + section_body[insert_pos:]
        else:
            # リンクが見つからない場合は、セクションの最後に追加
            section_body = section_body.rstrip() + images_html
        
        # 「読者への語りかけ」セクション以降の画像も削除
        if rest_body:
            rest_body = re.sub(img_pattern, '', rest_body, flags=re.MULTILINE)
        
        body = before_section + section_body + rest_body
    
    return body

def main():
    """メイン処理"""
    print("=" * 80)
    print("  MGS記事のサンプル画像修正（クリーンアップ）")
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
            affiliate_url = frontmatter.get("affiliateLink", "")
            title = frontmatter.get("title", "")
            
            if not image_url or not content_id:
                print(f"⏭️  {article_file.name} - 必要な情報が不足しています")
                skipped_count += 1
                continue
            
            new_body = fix_sample_images_in_body(body, image_url, content_id, affiliate_url, title)
            
            frontmatter_lines = ["---"]
            for key, value in frontmatter.items():
                if isinstance(value, str):
                    frontmatter_lines.append(f'{key}: "{value}"')
                else:
                    frontmatter_lines.append(f'{key}: {json.dumps(value, ensure_ascii=False)}')
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

