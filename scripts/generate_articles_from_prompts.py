#!/usr/bin/env python3
"""
プロンプトファイルから記事を生成するスクリプト
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# .envファイルの読み込み
try:
    from dotenv import load_dotenv
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass


def initialize_gemini(api_key: str):
    """Gemini APIを初期化"""
    genai.configure(api_key=api_key)


def parse_prompt_file(prompt_file: Path) -> dict:
    """プロンプトファイルから情報を抽出"""
    with open(prompt_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    info = {}
    
    # 作品データを抽出
    title_match = re.search(r'- 作品名：\s*(.+?)\n', content)
    if title_match:
        info['title'] = title_match.group(1).strip()
    
    description_match = re.search(r'- 紹介文：\s*(.+?)\n', content)
    if description_match:
        info['description'] = description_match.group(1).strip()
    
    content_id_match = re.search(r'- 作品ID：\s*(.+?)\n', content)
    if content_id_match:
        info['content_id'] = content_id_match.group(1).strip()
    
    url_match = re.search(r'- 作品URL：\s*(.+?)\n', content)
    if url_match:
        info['url'] = url_match.group(1).strip()
    
    affiliate_match = re.search(r'- アフィリエイトリンク：\s*(.+?)\n', content)
    if affiliate_match:
        info['affiliate_url'] = affiliate_match.group(1).strip()
    
    image_match = re.search(r'- メイン画像URL：\s*(.+?)\n', content)
    if image_match:
        info['image_url'] = image_match.group(1).strip()
    
    actress_match = re.search(r'- 出演：\s*(.+?)\n', content)
    if actress_match:
        info['actress'] = actress_match.group(1).strip()
    
    genre_match = re.search(r'- ジャンル：\s*(.+?)\n', content)
    if genre_match:
        info['genre'] = genre_match.group(1).strip()
    
    maker_match = re.search(r'- メーカー：\s*(.+?)\n', content)
    if maker_match:
        info['maker'] = maker_match.group(1).strip()
    
    director_match = re.search(r'- 監督：\s*(.+?)\n', content)
    if director_match:
        info['director'] = director_match.group(1).strip()
    
    # サンプル画像URLリストを抽出
    sample_images = []
    sample_section = re.search(r'- サンプル画像URLリスト：\s*\n((?:\s+\d+\.\s*.+?\n)+)', content)
    if sample_section:
        for line in sample_section.group(1).strip().split('\n'):
            url_match = re.search(r'\d+\.\s*(https?://.+?)(?:\s|$)', line)
            if url_match:
                sample_images.append(url_match.group(1).strip())
    info['sample_images'] = sample_images
    
    # 保存パスを抽出
    save_path_match = re.search(r'`(.+?)`', content)
    if save_path_match:
        info['save_path'] = save_path_match.group(1).strip()
    
    return info


def generate_article_from_prompt(model: genai.GenerativeModel, prompt_file: Path) -> str | None:
    """プロンプトファイルから記事を生成"""
    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt = f.read()
    
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }
    
    generation_config = {
        "temperature": 0.9,
        "top_p": 0.95,
        "top_k": 40,
    }
    
    try:
        response = model.generate_content(
            prompt,
            safety_settings=safety_settings,
            generation_config=generation_config
        )
        
        if not response.candidates:
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                print(f"   ❌ ブロックされました: {response.prompt_feedback.block_reason}", file=sys.stderr)
                return None
            return None
        
        return response.text
    except Exception as e:
        print(f"   ❌ 記事生成失敗: {e}", file=sys.stderr)
        return None


def save_article(content: str, info: dict, output_dir: Path) -> Path | None:
    """記事を保存"""
    # 保存パスからファイル名を抽出
    if 'save_path' in info:
        filename = Path(info['save_path']).name
    else:
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"{today}-{info.get('content_id', 'unknown')}.md"
    
    filepath = output_dir / filename
    
    try:
        # Frontmatterの```yamlを---に修正
        fixed_content = content
        if fixed_content.startswith("```yaml"):
            fixed_content = re.sub(r'^```yaml\s*\n---\s*\n', '---\n', fixed_content, flags=re.MULTILINE)
            fixed_content = re.sub(r'---\s*\n```\s*\n', '---\n\n', fixed_content, flags=re.MULTILINE)
            fixed_content = re.sub(r'```\s*$', '', fixed_content, flags=re.MULTILINE)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(fixed_content)
        return filepath
    except Exception as e:
        print(f"   ❌ 保存失敗: {e}", file=sys.stderr)
        return None


def main():
    """メイン処理"""
    print("\n" + "=" * 80)
    print("  プロンプトファイルから記事生成")
    print("=" * 80 + "\n")
    
    # 環境変数からAPIキーを取得
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ 環境変数 GEMINI_API_KEY が設定されていません", file=sys.stderr)
        sys.exit(1)
    
    # ディレクトリ設定
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    prompts_dir = project_root / "prompts"
    content_dir = project_root / "content"
    
    content_dir.mkdir(exist_ok=True)
    
    # プロンプトファイルのリスト
    prompt_files = [
        prompts_dir / "2025-12-30-roe00382-prompt.txt",
        prompts_dir / "2025-12-30-jur00145-prompt.txt",
        prompts_dir / "2025-12-30-jur00408-prompt.txt",
        prompts_dir / "2025-12-30-venx00334-prompt.txt",
        prompts_dir / "2025-12-30-juq00871-prompt.txt",
        prompts_dir / "2025-12-30-1dandy00919e-prompt.txt",
        prompts_dir / "2025-12-30-juq00516-prompt.txt",
        prompts_dir / "2025-12-30-roe00233-prompt.txt",
        prompts_dir / "2025-12-30-hntrz00016-prompt.txt",
        prompts_dir / "2025-12-30-juq00799-prompt.txt",
        prompts_dir / "2025-12-30-mbyd00381-prompt.txt",
        prompts_dir / "2025-12-30-gma00081-prompt.txt",
        prompts_dir / "2025-12-30-nsfs00365-prompt.txt",
        prompts_dir / "2025-12-30-vec00655-prompt.txt",
        prompts_dir / "2025-12-30-juvr00209-prompt.txt",
        prompts_dir / "2025-12-30-jjda00052-prompt.txt",
        prompts_dir / "2025-12-30-juq00965-prompt.txt",
        prompts_dir / "2025-12-30-gma00054-prompt.txt",
        prompts_dir / "2025-12-30-h_086hone00286-prompt.txt",
        prompts_dir / "2025-12-30-jur00120-prompt.txt",
    ]
    
    # 存在するプロンプトファイルのみを処理
    existing_prompts = [f for f in prompt_files if f.exists()]
    
    if not existing_prompts:
        print("❌ プロンプトファイルが見つかりません", file=sys.stderr)
        sys.exit(1)
    
    print(f"📖 {len(existing_prompts)}件のプロンプトファイルを読み込みました\n")
    
    # Gemini APIを初期化
    print("🤖 Gemini APIを初期化中...")
    initialize_gemini(api_key)
    
    model_name = "gemini-2.5-flash"
    print(f"✅ {model_name} を使用します\n")
    model = genai.GenerativeModel(model_name)
    
    # 記事生成
    success_count = 0
    fail_count = 0
    
    for idx, prompt_file in enumerate(existing_prompts, 1):
        print(f"[{idx}/{len(existing_prompts)}] 📝 {prompt_file.name}")
        
        # プロンプトファイルから情報を抽出
        info = parse_prompt_file(prompt_file)
        title = info.get('title', '不明')[:50]
        print(f"   作品名: {title}...")
        
        # 既存記事のチェック
        if 'save_path' in info:
            existing_file = Path(info['save_path'])
        else:
            today = datetime.now().strftime("%Y-%m-%d")
            existing_file = content_dir / f"{today}-{info.get('content_id', 'unknown')}.md"
        
        if existing_file.exists():
            print(f"   ⏭️  既存記事があるためスキップ")
            continue
        
        # 記事生成
        print(f"   ✍️  生成中...")
        article_content = generate_article_from_prompt(model, prompt_file)
        
        if article_content:
            # 保存
            filepath = save_article(article_content, info, content_dir)
            
            if filepath:
                print(f"   ✅ 保存完了: {filepath.name}")
                success_count += 1
            else:
                print(f"   ❌ 保存失敗")
                fail_count += 1
        else:
            print(f"   ❌ 生成失敗")
            fail_count += 1
        
        print()
    
    # 完了メッセージ
    print("=" * 80)
    print("🎉 記事生成完了！")
    print("=" * 80)
    print(f"✅ 成功: {success_count}本")
    print(f"❌ 失敗: {fail_count}本")
    print(f"📁 保存先: {content_dir}")
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()

