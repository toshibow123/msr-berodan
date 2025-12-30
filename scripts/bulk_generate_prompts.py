#!/usr/bin/env python3
"""
一括プロンプト生成スクリプト
works_list.txtから作品リストを読み込み、Cursor用のプロンプトを一括生成してファイルに保存
"""

import os
import sys
import random
import time
from datetime import datetime
from pathlib import Path

# .envファイルの読み込み
try:
    from dotenv import load_dotenv
    # プロジェクトルートの.envファイルを読み込む
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    # python-dotenvがインストールされていない場合はスキップ
    pass

# ============================================================================
# 設定項目
# ============================================================================
DMM_API_ID = os.environ.get("DMM_API_ID", "")
DMM_AFFILIATE_ID = os.environ.get("DMM_AFFILIATE_ID", "")

# 既存の関数をインポート（同じディレクトリから）
sys.path.insert(0, str(Path(__file__).parent))
from generate_prompt_from_api import (
    extract_content_id_from_url,
    fetch_dmm_product_info,
    load_example_articles,
    generate_cursor_prompt
)


def read_works_list(works_list_path: Path) -> list[dict]:
    """
    works_list.txtを読み込む
    
    フォーマット: URL | 作品の特徴・記事に書いて欲しい内容
    メモの例: 美白、中出しがエロい、新人なのに激しい
    メモの例: パイパン デカ美尻 バニーガール
    メモの例: 冒頭のOL衣装が最高、破れるところがピーク
    
    Args:
        works_list_path: works_list.txtのパス
        
    Returns:
        [{"url": "...", "memo": "..."}, ...] のリスト
    """
    works = []
    
    if not works_list_path.exists():
        print(f"❌ {works_list_path} が見つかりません", file=sys.stderr)
        return works
    
    try:
        with open(works_list_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                
                # コメント行をスキップ
                if not line or line.startswith("#"):
                    continue
                
                # URL | メモ の形式をパース
                if "|" in line:
                    parts = line.split("|", 1)
                    url = parts[0].strip()
                    memo = parts[1].strip() if len(parts) > 1 else ""
                else:
                    url = line.strip()
                    memo = ""
                
                if url:
                    works.append({"url": url, "memo": memo})
    except Exception as e:
        print(f"❌ works_list.txtの読み込みに失敗: {e}", file=sys.stderr)
    
    return works


def save_prompt_file(prompt: str, content_id: str, output_dir: Path) -> Path | None:
    """
    プロンプトをファイルとして保存
    
    Args:
        prompt: プロンプト文字列
        content_id: コンテンツID
        output_dir: 出力ディレクトリ
        
    Returns:
        保存されたファイルのパス、またはNone
    """
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"{today}-{content_id}-prompt.txt"
    filepath = output_dir / filename
    
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(prompt)
        return filepath
    except Exception as e:
        print(f"    ❌ ファイル保存に失敗: {e}", file=sys.stderr)
        return None


def main():
    """メイン処理"""
    print("\n" + "=" * 80)
    print("  一括プロンプト生成スクリプト")
    print("=" * 80 + "\n")
    
    # API認証情報の確認
    if not DMM_API_ID or not DMM_AFFILIATE_ID:
        print("❌ DMM API認証情報が設定されていません", file=sys.stderr)
        print("   環境変数 DMM_API_ID と DMM_AFFILIATE_ID を設定してください", file=sys.stderr)
        sys.exit(1)
    
    # プロジェクトルートを取得
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    works_list_path = project_root / "works_list.txt"
    content_dir = project_root / "content"
    prompts_dir = project_root / "prompts"
    
    # works_list.txtを読み込む
    print(f"📋 {works_list_path} を読み込み中...")
    works = read_works_list(works_list_path)
    
    if not works:
        print("❌ 作品リストが空です", file=sys.stderr)
        sys.exit(1)
    
    print(f"✅ {len(works)}件の作品を読み込みました\n")
    
    # 既存記事を読み込む（参考用）
    print("📚 既存記事を読み込み中...")
    example_articles = load_example_articles(content_dir, max_articles=3)
    if example_articles:
        print(f"✅ {len(example_articles)}件の既存記事を読み込みました\n")
    else:
        print("⚠️  既存記事が見つかりませんでした\n")
    
    # 各作品についてプロンプトを生成
    print("=" * 80)
    print("📝 プロンプト生成を開始します...\n")
    
    success_count = 0
    skip_count = 0
    fail_count = 0
    
    for idx, work in enumerate(works, 1):
        url = work["url"]
        memo = work["memo"]
        
        print(f"[{idx}/{len(works)}] 処理中...")
        print(f"   URL: {url[:80]}...")
        if memo:
            print(f"   メモ: {memo}")
        
        # URLから品番を抽出
        content_id = extract_content_id_from_url(url)
        if not content_id:
            print(f"   ❌ URLから品番を抽出できませんでした")
            fail_count += 1
            print()
            continue
        
        print(f"   品番: {content_id}")
        
        # 既存プロンプトのチェック
        today = datetime.now().strftime("%Y-%m-%d")
        existing_file = prompts_dir / f"{today}-{content_id}-prompt.txt"
        if existing_file.exists():
            print(f"   ⏭️  既存プロンプトがあるためスキップ: {existing_file.name}")
            skip_count += 1
            print()
            continue
        
        # DMM APIから商品情報を取得
        print(f"   📡 DMM APIから商品情報を取得中...")
        product_info = fetch_dmm_product_info(DMM_API_ID, DMM_AFFILIATE_ID, content_id)
        
        if not product_info:
            print(f"   ❌ 商品情報の取得に失敗しました")
            fail_count += 1
            print()
            continue
        
        print(f"   ✅ 作品名: {product_info.get('title', '不明')[:50]}...")
        
        # プロンプトを生成
        print(f"   📝 プロンプト生成中...")
        prompt = generate_cursor_prompt(
            product_info,
            url,
            memo,  # ユーザーメモを作品特徴として渡す
            example_articles
        )
        
        if prompt:
            # プロンプトを保存
            filepath = save_prompt_file(prompt, content_id, prompts_dir)
            
            if filepath:
                print(f"   ✅ 保存完了: {filepath.name}")
                print(f"   📍 保存先: {filepath}")
                success_count += 1
            else:
                fail_count += 1
        else:
            print(f"   ❌ プロンプト生成に失敗しました")
            fail_count += 1
        
        # API制限回避のためウェイト（最後の作品以外）
        if idx < len(works):
            wait_time = random.randint(1, 3)  # 1-3秒のランダムウェイト
            print(f"   ⏳ API制限回避のため{wait_time}秒待機中...\n")
            time.sleep(wait_time)
        else:
            print()
    
    # 完了メッセージ
    print("=" * 80)
    print("🎉 プロンプト生成完了！")
    print(f"   成功: {success_count}件")
    print(f"   スキップ: {skip_count}件")
    print(f"   失敗: {fail_count}件")
    print(f"   保存先: {prompts_dir}")
    print("\n💡 各プロンプトファイルを開いて、Cursorに貼り付けて記事を生成してください。")
    print("=" * 80)


if __name__ == "__main__":
    main()

