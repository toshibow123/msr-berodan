#!/usr/bin/env python3
"""
MGS記事のサンプル画像を規則性のあるURLで表示するように修正するスクリプト
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
    
    # フロントマターの終了位置を探す
    end_pos = content.find("\n---", 3)
    if end_pos == -1:
        return {}, content
    
    frontmatter_text = content[4:end_pos].strip()
    body = content[end_pos + 5:].strip()
    
    # フロントマターをパース
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
    
    例:
    メイン画像: https://image.mgstage.com/images/ntrnet/348ntr/082/pf_o2_348ntr-082.jpg
    サンプル画像: https://image.mgstage.com/images/ntrnet/348ntr/082/pf_348ntr-082-1.jpg
                 https://image.mgstage.com/images/ntrnet/348ntr/082/pf_348ntr-082-2.jpg
                 etc.
    """
    if not image_url or "image.mgstage.com" not in image_url:
        return []
    
    # メイン画像URLからパス構造を抽出
    # 例: https://image.mgstage.com/images/ntrnet/348ntr/082/pf_o2_348ntr-082.jpg
    match = re.search(r'https://image\.mgstage\.com/images/(.+?)/(.+?)/(.+?)/pf_o2_(.+?)\.jpg', image_url)
    if not match:
        # 別のパターンを試す
        match = re.search(r'https://image\.mgstage\.com/images/(.+?)/(.+?)/(.+?)/pf_(.+?)\.jpg', image_url)
        if not match:
            return []
    
    maker = match.group(1)
    series = match.group(2)
    id_part = match.group(3)
    base_name = match.group(4)
    
    # サンプル画像URLを生成（pf_o2_の代わりにpf_を使用）
    sample_urls = []
    for i in range(1, count + 1):
        # pf_348ntr-082-1.jpg の形式（pf_o2_ではなくpf_）
        sample_url = f"https://image.mgstage.com/images/{maker}/{series}/{id_part}/pf_{base_name}-{i}.jpg"
        sample_urls.append(sample_url)
    
    return sample_urls

def fix_sample_images_in_body(body: str, image_url: str, content_id: str, affiliate_url: str, title: str) -> str:
    """本文内のサンプル画像を修正"""
    # サンプル画像URLを生成
    sample_urls = generate_mgs_sample_image_urls(image_url, content_id, count=3)
    
    if not sample_urls:
        # サンプル画像URLが生成できない場合は、メイン画像を3回繰り返す
        sample_urls = [image_url] * 3
    
    # 「心に残るシーン」セクションの後に来る画像タグを全て探す
    # セクションの位置を特定
    scene_section_pattern = r'## 心に残るシーン[^\n]*\n'
    scene_match = re.search(scene_section_pattern, body)
    
    if scene_match:
        # セクション以降の部分を取得
        section_start = scene_match.end()
        section_body = body[section_start:]
        
        # セクション以降の画像タグを全て探す（メイン画像と同じURLのもの）
        escaped_image_url = re.escape(image_url)
        pattern = rf'<a href="[^"]*" target="_blank" rel="sponsored noopener noreferrer">\s*<img src="{escaped_image_url}"[^>]*alt="[^"]*"[^>]*/>\s*</a>'
        
        matches = list(re.finditer(pattern, section_body))
        if matches:
            # 後ろから置き換える（インデックスのずれを防ぐため）
            result_section = section_body
            reversed_matches = list(reversed(matches[:3]))  # 最初の3つを後ろから
            for i, match in enumerate(reversed_matches):
                # 後ろから置き換えるので、最初のマッチ（最後の画像）にsample_urls[0]を、最後のマッチ（最初の画像）にsample_urls[2]を割り当てる
                idx = len(reversed_matches) - 1 - i  # 2, 1, 0の順
                if idx < len(sample_urls):
                    new_img_tag = f'<a href="{affiliate_url}" target="_blank" rel="sponsored noopener noreferrer">\n  <img src="{sample_urls[idx]}" alt="{title}" />\n</a>'
                    # マッチした位置を置き換え
                    start, end = match.span()
                    result_section = result_section[:start] + new_img_tag + result_section[end:]
            
            # 元の本文と結合
            body = body[:section_start] + result_section
        else:
            # 画像タグが見つからない場合は、セクションの最後に追加
            # セクションの終わりを探す（次の##セクションまで）
            next_section_match = re.search(r'\n## ', section_body)
            if next_section_match:
                insert_pos = section_start + next_section_match.start()
            else:
                insert_pos = len(body)
            
            images_html = "\n\n"
            for sample_url in sample_urls:
                images_html += f'<a href="{affiliate_url}" target="_blank" rel="sponsored noopener noreferrer">\n  <img src="{sample_url}" alt="{title}" />\n</a>\n\n'
            body = body[:insert_pos] + images_html + body[insert_pos:]
    else:
        # 「心に残るシーン」セクションが見つからない場合は、最後に追加
        images_html = "\n\n"
        for sample_url in sample_urls:
            images_html += f'<a href="{affiliate_url}" target="_blank" rel="sponsored noopener noreferrer">\n  <img src="{sample_url}" alt="{title}" />\n</a>\n\n'
        body = body + images_html
    
    return body

def main():
    """メイン処理"""
    print("=" * 80)
    print("  MGS記事のサンプル画像修正")
    print("=" * 80 + "\n")
    
    # 2026-01-02の記事を取得（MGS記事）
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
            
            # フロントマターを抽出
            frontmatter, body = extract_frontmatter(content)
            
            if not frontmatter:
                print(f"⏭️  {article_file.name} - フロントマターが見つかりません")
                skipped_count += 1
                continue
            
            # MGS記事かどうか確認
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
            
            # サンプル画像を修正
            new_body = fix_sample_images_in_body(body, image_url, content_id, affiliate_url, title)
            
            # 保存
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

