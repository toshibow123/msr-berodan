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


def load_ranking_data(data_dir: Path) -> list:
    """
    mature_drama_all_latest.jsonからランキングデータを読み込む
    
    Args:
        data_dir: dataディレクトリのパス
        
    Returns:
        作品情報のリスト
    """
    import json
    
    latest_file = data_dir / "mature_drama_all_latest.json"
    
    if not latest_file.exists():
        print(f"❌ ランキングファイルが見つかりません: {latest_file}", file=sys.stderr)
        return []
    
    try:
        with open(latest_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("ranking", [])
    except Exception as e:
        print(f"❌ ランキングデータの読み込み失敗: {e}", file=sys.stderr)
        return []


def convert_to_product_info(work: dict) -> dict:
    """
    JSONファイルのworkデータをproduct_info形式に変換
    
    Args:
        work: JSONファイルから読み込んだ作品情報
        
    Returns:
        product_info形式の辞書
    """
    # ジャンルを文字列に変換
    genres = work.get("genre", [])
    genres_str = "、".join(genres) if genres else ""
    
    # 出演者を文字列に変換
    actresses = work.get("actress", [])
    actresses_str = "、".join(actresses) if actresses else ""
    
    # keywordsを作成（ジャンル + 出演者）
    keywords_parts = []
    if genres_str:
        keywords_parts.append(genres_str)
    if actresses_str:
        keywords_parts.append(actresses_str)
    if work.get("maker"):
        keywords_parts.append(f"メーカー:{work.get('maker')}")
    if work.get("director"):
        keywords_parts.append(f"監督:{work.get('director')}")
    keywords = "、".join(keywords_parts)
    
    # サンプル画像URLを生成（image_urlから推測）
    sample_images = []
    image_url = work.get("image_url", "")
    if image_url:
        # メイン画像を追加
        sample_images.append(image_url)
        # サンプル画像のパターンを生成
        content_id = work.get("content_id", "")
        if content_id:
            # videoa と video の両方のパターンを試す
            for floor in ["videoa", "video"]:
                for i in range(1, 11):
                    sample_url = f"https://pics.dmm.co.jp/digital/{floor}/{content_id}/{content_id}jp-{i}.jpg"
                    sample_images.append(sample_url)
    
    product_info = {
        "title": work.get("title", ""),
        "description": work.get("description", ""),
        "content_id": work.get("content_id", ""),
        "keywords": keywords,
        "genres": genres,
        "main_image_url": image_url,
        "sample_images": sample_images,
        "affiliate_url": work.get("affiliate_url", ""),
        "url": work.get("url", ""),
        "release_date": work.get("release_date", ""),
        "actress": actresses,
        "maker": work.get("maker", ""),
        "director": work.get("director", ""),
    }
    
    return product_info


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
    data_dir = project_root / "data"
    content_dir = project_root / "content"
    prompts_dir = project_root / "prompts"
    
    # ランキングデータを読み込む
    print(f"📋 {data_dir / 'mature_drama_all_latest.json'} を読み込み中...")
    ranking_data = load_ranking_data(data_dir)
    
    if not ranking_data:
        print("❌ ランキングデータが空です", file=sys.stderr)
        sys.exit(1)
    
    print(f"✅ {len(ranking_data)}件の作品を読み込みました\n")
    
    # 既存記事のcontent_idを取得
    print("🔍 既存記事をチェック中...")
    existing_content_ids = set()
    for content_file in content_dir.glob("*.md"):
        try:
            with open(content_file, "r", encoding="utf-8") as f:
                content = f.read()
                # frontmatterからcontentIdを抽出
                if "contentId:" in content:
                    for line in content.split("\n"):
                        if line.startswith("contentId:"):
                            existing_id = line.split("contentId:")[1].strip().strip('"').strip("'")
                            if existing_id:
                                existing_content_ids.add(existing_id)
                            break
        except Exception:
            pass
    
    print(f"✅ {len(existing_content_ids)}件の既存記事を検出しました\n")
    
    # 既存記事を除外
    filtered_ranking = [work for work in ranking_data if work.get("content_id", "") not in existing_content_ids]
    print(f"📊 フィルタリング後: {len(filtered_ranking)}件（既存除外: {len(ranking_data) - len(filtered_ranking)}件）\n")
    
    if not filtered_ranking:
        print("❌ 新規記事がありません。全て既存記事です。", file=sys.stderr)
        sys.exit(0)
    
    # 既存記事を読み込む（参考用）
    print("📚 既存記事を読み込み中...")
    example_articles = load_example_articles(content_dir, max_articles=3)
    if example_articles:
        print(f"✅ {len(example_articles)}件の既存記事を読み込みました\n")
    else:
        print("⚠️  既存記事が見つかりませんでした\n")
    
    # 生成するプロンプト数を入力
    max_prompts = int(input(f"何件のプロンプトを生成しますか？（最大{len(filtered_ranking)}件）: ").strip() or "10")
    max_prompts = min(max_prompts, len(filtered_ranking))
    
    # 各作品についてプロンプトを生成
    print("=" * 80)
    print("📝 プロンプト生成を開始します...\n")
    
    success_count = 0
    skip_count = 0
    fail_count = 0
    
    for idx, work in enumerate(filtered_ranking[:max_prompts], 1):
        content_id = work.get("content_id", "")
        title = work.get("title", "不明")
        url = work.get("url", "")
        
        print(f"[{idx}/{max_prompts}] 処理中...")
        print(f"   作品名: {title[:50]}...")
        print(f"   品番: {content_id}")
        
        # 既存プロンプトのチェック
        today = datetime.now().strftime("%Y-%m-%d")
        existing_file = prompts_dir / f"{today}-{content_id}-prompt.txt"
        if existing_file.exists():
            print(f"   ⏭️  既存プロンプトがあるためスキップ: {existing_file.name}")
            skip_count += 1
            print()
            continue
        
        # JSONデータをproduct_info形式に変換
        product_info = convert_to_product_info(work)
        
        print(f"   ✅ 作品名: {product_info.get('title', '不明')[:50]}...")
        
        # プロンプトを生成
        print(f"   📝 プロンプト生成中...")
        prompt = generate_cursor_prompt(
            product_info,
            url,
            "",  # メモは空（JSONデータに含まれているため）
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
        if idx < max_prompts:
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

