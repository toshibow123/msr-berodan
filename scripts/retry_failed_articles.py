#!/usr/bin/env python3
"""
失敗した記事の再試行スクリプト
failed_articles.jsonから失敗した記事を読み込んで再生成を試みる
"""

import os
import json
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
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


# bulk_generate_mature_drama_articles.pyから関数をインポート
import importlib.util
spec = importlib.util.spec_from_file_location(
    "bulk_generate", 
    Path(__file__).parent / "bulk_generate_mature_drama_articles.py"
)
bulk_generate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bulk_generate)

def create_article_prompt(product_info: dict) -> str:
    """記事生成用のプロンプトを作成（bulk_generate_mature_drama_articles.pyと同じ）"""
    return bulk_generate.create_article_prompt(product_info)


def generate_article(model: genai.GenerativeModel, product_info: dict, max_retries: int = 5) -> str | None:
    """Gemini APIを使って記事本文を生成（リトライ機能付き、再試行時は多めにリトライ）"""
    prompt = create_article_prompt(product_info)
    
    # セーフティ設定（創作物・小説レビューとして扱うため、ブロックを緩和）
    safety_settings = [
        {
            "category": HarmCategory.HARM_CATEGORY_HARASSMENT,
            "threshold": HarmBlockThreshold.BLOCK_NONE,
        },
        {
            "category": HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            "threshold": HarmBlockThreshold.BLOCK_NONE,
        },
        {
            "category": HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            "threshold": HarmBlockThreshold.BLOCK_ONLY_HIGH,  # 高レベルのみブロック
        },
        {
            "category": HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            "threshold": HarmBlockThreshold.BLOCK_NONE,
        },
    ]
    
    generation_config = {
        "temperature": 0.9,  # 創造性を高める
        "top_p": 0.95,
        "top_k": 40,
    }
    
    for attempt in range(max_retries):
        try:
            response = model.generate_content(
                prompt,
                safety_settings=safety_settings,
                generation_config=generation_config
            )
            
            if not response.candidates:
                if response.prompt_feedback and response.prompt_feedback.block_reason:
                    print(f"   ❌ ブロックされました: {response.prompt_feedback.block_reason}", file=sys.stderr)
                    # ブロックされた場合、プロンプトをさらに婉曲的に修正してリトライ
                    if attempt < max_retries - 1:
                        print(f"   ⚠️  より婉曲的な表現でリトライします... (試行 {attempt + 1}/{max_retries})")
                        time.sleep(10 * (attempt + 1))  # 試行回数に応じて待機時間を増やす
                        continue
                return None
            
            return response.text
            
        except Exception as e:
            error_str = str(e)
            
            # クォータエラーの場合
            if "429" in error_str or "quota" in error_str.lower() or "Quota exceeded" in error_str:
                if attempt < max_retries - 1:
                    wait_time = 120  # 再試行時は長めに待機
                    if "retry in" in error_str.lower():
                        import re
                        match = re.search(r'retry in ([\d.]+)s', error_str, re.IGNORECASE)
                        if match:
                            wait_time = int(float(match.group(1))) + 30  # 余裕を持たせる
                    
                    print(f"   ⚠️  クォータ制限に達しました。{wait_time}秒待機してリトライします... (試行 {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"   ❌ クォータ制限のため生成をスキップしました", file=sys.stderr)
                    return None
            else:
                # その他のエラー
                print(f"   ❌ 記事生成失敗: {e}", file=sys.stderr)
                if attempt < max_retries - 1:
                    wait_time = 15 * (attempt + 1)  # 指数バックオフ
                    print(f"   ⏳ {wait_time}秒待機してリトライします... (試行 {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                return None
    
    return None


def save_article(content: str, product_info: dict, publish_date: str, output_dir: Path, content_id: str, matched_genres: list) -> str | None:
    """記事をMarkdownファイルとして保存（bulk_generate_mature_drama_articles.pyと同じ）"""
    return bulk_generate.save_article(content, product_info, publish_date, output_dir, content_id, matched_genres)


def is_valid_genre(product_info: dict) -> tuple[bool, list]:
    """ジャンル判定（bulk_generate_mature_drama_articles.pyと同じ）"""
    return bulk_generate.is_valid_genre(product_info)


def main():
    """メイン処理"""
    print("\n" + "🔄" * 40)
    print("  失敗した記事の再試行スクリプト")
    print("🔄" * 40 + "\n")
    
    # 環境変数からAPIキーを取得
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ 環境変数 GEMINI_API_KEY が設定されていません", file=sys.stderr)
        sys.exit(1)
    
    # ディレクトリ設定
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    data_dir = project_root / "data"
    content_dir = project_root / "content"
    
    content_dir.mkdir(exist_ok=True)
    
    # 失敗記事ファイルを読み込む
    failed_file = data_dir / "failed_articles.json"
    if not failed_file.exists():
        print(f"❌ 失敗記事ファイルが見つかりません: {failed_file}", file=sys.stderr)
        print("💡 まず bulk_generate_mature_drama_articles.py を実行してください", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(failed_file, "r", encoding="utf-8") as f:
            failed_items = json.load(f)
    except Exception as e:
        print(f"❌ 失敗記事ファイルの読み込み失敗: {e}", file=sys.stderr)
        sys.exit(1)
    
    if not failed_items:
        print("✅ 再試行する記事がありません")
        sys.exit(0)
    
    print(f"📖 {len(failed_items)}件の失敗記事を読み込みました\n")
    
    # Gemini APIを初期化
    print("🤖 Gemini APIを初期化中...")
    initialize_gemini(api_key)
    
    model_name = "gemini-2.5-flash"
    print(f"✅ {model_name} を使用します\n")
    model = genai.GenerativeModel(model_name)
    
    # 再試行
    success_count = 0
    fail_count = 0
    still_failed = []
    
    for idx, item in enumerate(failed_items, 1):
        content_id = item.get("content_id", "")
        title = item.get("title", "不明")
        publish_date = item.get("publish_date", "")
        work = item.get("work", {})
        
        print(f"[{idx}/{len(failed_items)}] 🔄 {title[:40]}...")
        print(f"   公開日: {publish_date}")
        
        # ジャンル判定
        is_valid, matched_genres = is_valid_genre(work)
        if not is_valid:
            print(f"   ⏭️  スキップ（対象外ジャンル）")
            continue
        
        print(f"   ジャンル: {', '.join(matched_genres)}")
        
        # 記事生成
        print(f"   ✍️  再生成中...")
        article_content = generate_article(model, work, max_retries=5)
        
        if article_content:
            # 保存
            filepath = save_article(article_content, work, publish_date, content_dir, content_id, matched_genres)
            
            if filepath:
                print(f"   ✅ 保存完了")
                success_count += 1
            else:
                print(f"   ❌ 保存失敗")
                fail_count += 1
                still_failed.append(item)
        else:
            print(f"   ❌ 生成失敗")
            fail_count += 1
            still_failed.append(item)
        
        # レート制限対策（再試行時は長めに待機）
        if idx < len(failed_items):
            wait_time = 20  # 20秒待機
            print(f"   ⏳ {wait_time}秒待機中...")
            time.sleep(wait_time)
        
        print()
    
    # まだ失敗した記事を更新
    if still_failed:
        try:
            with open(failed_file, "w", encoding="utf-8") as f:
                json.dump(still_failed, f, ensure_ascii=False, indent=2)
            print(f"📝 まだ失敗した記事を記録しました: {failed_file}")
        except Exception as e:
            print(f"⚠️  失敗記事の記録に失敗: {e}", file=sys.stderr)
    else:
        # すべて成功したらファイルを削除
        try:
            failed_file.unlink()
            print(f"✅ すべて成功したため、失敗記事ファイルを削除しました")
        except Exception as e:
            print(f"⚠️  ファイル削除に失敗: {e}", file=sys.stderr)
    
    # 完了メッセージ
    print("=" * 80)
    print("🎉 再試行完了！")
    print("=" * 80)
    print(f"✅ 成功: {success_count}本")
    print(f"❌ 失敗: {fail_count}本")
    if still_failed:
        print(f"💾 まだ失敗した記事は {failed_file} に保存されました")
    print(f"📁 保存先: {content_dir}")
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()

