#!/usr/bin/env python3
"""
Google Gemini APIを使ってDMMドラマ系動画データからブログ記事を生成するスクリプト
"""

import os
import json
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
import google.generativeai as genai


def load_ranking_data(json_path: str) -> dict:
    """
    ランキングデータのJSONファイルを読み込む
    
    Args:
        json_path: JSONファイルのパス
        
    Returns:
        ランキングデータ
    """
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"エラー: ファイルが見つかりません: {json_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"エラー: JSONのパースに失敗しました: {e}", file=sys.stderr)
        sys.exit(1)


def initialize_gemini(api_key: str):
    """
    Gemini APIを初期化
    
    Args:
        api_key: Gemini APIキー
    """
    genai.configure(api_key=api_key)


def create_prompt(video_data: dict) -> str:
    """
    Gemini用のプロンプトを作成
    
    Args:
        video_data: 動画データ
        
    Returns:
        プロンプト文字列
    """
    title = video_data.get("title", "")
    image_url = video_data.get("image_url", "")
    affiliate_url = video_data.get("affiliate_url", "")
    actress_list = video_data.get("actress", [])
    genre_list = video_data.get("genre", [])
    maker = video_data.get("maker", "")
    
    actresses = "、".join(actress_list) if actress_list else "不明"
    genres = "、".join(genre_list) if genre_list else "不明"
    
    prompt = f"""あなたは「大阪のビデオ道場師範代」です。陽気な関西弁で、今回は**「ドラマ性の高い名作」**を紹介します。
単なるエロだけでなく、**「ストーリーの没入感」や「女優の演技力」**に焦点を当てて、映画レビューのように熱く語ってください。

**【禁止事項】**
* 批判、悪口は禁止。「ここが泣ける」「ここがエモい」というポジティブな感情で書くこと。

**作品情報:**
- タイトル: {title}
- 出演: {actresses}
- ジャンル: {genres}
- メーカー: {maker}
- 画像URL: {image_url}
- アフィリエイトリンク: {affiliate_url}

**出力フォーマット（Markdown本文のみ）:**

## まいど！
（自然な関西弁の挨拶から始める。「最近ええ作品見つけたから紹介したるわ」「今日はとんでもない名作やで」など、関西人の普通の会話のように自然に）

## 今日の名作：{title}
![パッケージ画像]({image_url})

## あらすじと師範の解説
（あらすじを紹介。「ただのすれ違いかと思ったら、まさかこんな展開になるとは…」と物語に引き込む）

**重要：このセクションの最後に、以下の形式でアフィリエイトリンクを必ず挿入してください：**
<div className="affiliate-link-inline">
  <a href="{affiliate_url}" target="_blank" rel="noopener noreferrer">気になる方はこちらでサンプル動画をチェック！</a>
</div>

## ここがエモい！演技と演出
（女優の表情やセリフ回し、切ないシーンなどを具体的に褒める。「この涙の演技でご飯3杯いけるわ」）

**重要：このセクションの最後にも、以下の形式でアフィリエイトリンクを必ず挿入してください：**
<div className="affiliate-link-inline">
  <a href="{affiliate_url}" target="_blank" rel="noopener noreferrer">演技の見どころを動画で確認する</a>
</div>

## 師範の総評：物語に浸りたい兄弟へ
（「抜いた後、賢者タイムにならずに余韻に浸れる一本や」「ハンカチ用意して見とき」と締める）

**重要：記事の最後に、以下の形式で大きなアフィリエイトリンクを必ず挿入してください：**
<div className="affiliate-link">
  <a href="{affiliate_url}" target="_blank" rel="noopener noreferrer">DMMでサンプルを見る（ストーリーの続きはこちら）</a>
</div>

注意: 
- Frontmatterは含めず、Markdown本文のみを出力してください。
- アフィリエイトリンクは必ず上記の3箇所に配置してください。
- リンクテキストは自然な文章に合わせて変更しても構いません。"""
    
    return prompt


def insert_affiliate_links(content: str, affiliate_url: str) -> str:
    """
    記事の内容にアフィリエイトリンクを適切な位置に挿入
    
    Args:
        content: 記事本文
        affiliate_url: アフィリエイトURL
        
    Returns:
        アフィリエイトリンクが挿入された記事本文
    """
    # 既にアフィリエイトリンクが含まれているかチェック
    if affiliate_url in content:
        return content
    
    lines = content.split('\n')
    result = []
    section_count = 0
    
    for i, line in enumerate(lines):
        result.append(line)
        
        # セクション見出し（##）の後にアフィリエイトリンクを挿入
        if line.startswith('## ') and not line.startswith('## まいど') and not line.startswith('## 今日の名作'):
            section_count += 1
            
            # 次の見出しまたは記事の終わりまでを確認
            next_section_idx = None
            for j in range(i + 1, len(lines)):
                if lines[j].startswith('## '):
                    next_section_idx = j
                    break
            
            # このセクションの最後にアフィリエイトリンクを挿入
            if next_section_idx:
                # 次の見出しの直前の空行の前に挿入
                if section_count == 1:  # あらすじセクション
                    result.append('')
                    result.append(f'<div className="affiliate-link-inline">')
                    result.append(f'  <a href="{affiliate_url}" target="_blank" rel="noopener noreferrer">気になる方はこちらでサンプル動画をチェック！</a>')
                    result.append(f'</div>')
                elif section_count == 2:  # 演技と演出セクション
                    result.append('')
                    result.append(f'<div className="affiliate-link-inline">')
                    result.append(f'  <a href="{affiliate_url}" target="_blank" rel="noopener noreferrer">演技の見どころを動画で確認する</a>')
                    result.append(f'</div>')
    
    # 記事の最後に大きなアフィリエイトリンクを追加（まだ含まれていない場合）
    final_content = '\n'.join(result)
    if f'<div className="affiliate-link">' not in final_content:
        final_content += '\n\n'
        final_content += '<div className="affiliate-link">\n'
        final_content += f'  <a href="{affiliate_url}" target="_blank" rel="noopener noreferrer">DMMでサンプルを見る（ストーリーの続きはこちら）</a>\n'
        final_content += '</div>'
    
    return final_content


def generate_article(model, video_data: dict) -> str:
    """
    Gemini APIを使って記事を生成
    
    Args:
        model: Geminiモデル
        video_data: 動画データ
        
    Returns:
        生成された記事本文
    """
    prompt = create_prompt(video_data)
    affiliate_url = video_data.get("affiliate_url", "")
    
    try:
        response = model.generate_content(prompt)
        article_content = response.text
        
        # アフィリエイトリンクが不足している場合は自動挿入
        if affiliate_url and affiliate_url not in article_content:
            article_content = insert_affiliate_links(article_content, affiliate_url)
        
        return article_content
    except Exception as e:
        print(f"エラー: 記事生成に失敗しました: {e}", file=sys.stderr)
        return None


def save_article(content: str, video_data: dict, publish_date: str, output_dir: str) -> str:
    """
    記事をMarkdownファイルとして保存
    
    Args:
        content: 記事本文
        video_data: 動画データ
        publish_date: 公開日（YYYY-MM-DD形式）
        output_dir: 出力ディレクトリ
        
    Returns:
        保存したファイルパス
    """
    content_id = video_data.get("content_id", "unknown")
    title = video_data.get("title", "")
    image_url = video_data.get("image_url", "")
    affiliate_url = video_data.get("affiliate_url", "")
    actress_list = video_data.get("actress", [])
    
    # タグの作成（女優名 + 固定タグ）
    tags = []
    if actress_list:
        # 最大3人まで
        tags.extend([f'"{actress}"' for actress in actress_list[:3]])
    tags.extend(['"ドラマ"', '"なにわのビデオ道場"'])
    tags_str = ", ".join(tags)
    
    # Frontmatterを作成
    frontmatter = f"""---
title: "【ドラマ】{title} のストーリーが凄すぎる件"
date: "{publish_date}"
excerpt: "ビデオ道場の師範が{title}のストーリーと演技を関西弁で熱く語る！"
image: "{image_url}"
tags: [{tags_str}]
affiliateLink: "{affiliate_url}"
---

"""
    
    # ファイル名を作成
    filename = f"{publish_date}-{content_id}.md"
    filepath = os.path.join(output_dir, filename)
    
    # 記事全体を作成
    full_content = frontmatter + content
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(full_content)
        return filepath
    except IOError as e:
        print(f"エラー: ファイルの保存に失敗しました: {e}", file=sys.stderr)
        return None


def main():
    """メイン処理"""
    # 環境変数からAPIキーを取得
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        print("エラー: 環境変数 GEMINI_API_KEY が設定されていません", file=sys.stderr)
        sys.exit(1)
    
    # プロジェクトルートのパスを取得
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # JSONファイルのパスを確認（ranking_data.jsonを優先）
    json_path = project_root / "ranking_data.json"
    if not json_path.exists():
        # ranking_data.jsonが存在しない場合は、data/dmm_ranking_latest.jsonを使用
        json_path = project_root / "data" / "dmm_ranking_latest.json"
        print(f"⚠️  ranking_data.jsonが見つからないため、{json_path}を使用します")
    else:
        print(f"📂 ranking_data.jsonを読み込みます")
    
    # ランキングデータを読み込む
    print("📖 ランキングデータを読み込み中...")
    ranking_data = load_ranking_data(str(json_path))
    
    # rankingキーがある場合はそれを使用、なければitemsキーを探す
    videos = ranking_data.get("ranking", ranking_data.get("items", []))
    
    if not videos:
        print("エラー: 動画データが見つかりません", file=sys.stderr)
        sys.exit(1)
    
    print(f"📊 {len(videos)}件の動画データを取得しました")
    
    # Gemini APIを初期化
    print("🤖 Gemini APIを初期化中...")
    initialize_gemini(api_key)
    # gemini-1.5-flashは存在しないため、gemini-flash-latestを使用（常に最新のFlashモデル）
    model = genai.GenerativeModel("gemini-flash-latest")
    
    # 出力ディレクトリを作成
    content_dir = project_root / "content"
    content_dir.mkdir(exist_ok=True)
    
    # 開始日を設定（12月14日から開始）
    start_date = datetime(2025, 12, 14)
    # 生成する記事数（12月14日〜18日、1日3本 = 15本）
    articles_to_generate = 15
    
    # 各動画について記事を生成
    print(f"\n✍️  記事生成を開始します...")
    print(f"   開始日: {start_date.strftime('%Y-%m-%d')}")
    print(f"   生成記事数: {articles_to_generate}本（1日3本 × 5日間）\n")
    
    # テストモード：環境変数TEST_MODEが設定されている場合は1件のみ処理
    test_mode = os.environ.get("TEST_MODE", "").lower() == "true"
    videos_to_process = videos[:articles_to_generate] if not test_mode else videos[:1]
    
    if test_mode:
        print("🧪 テストモード：1記事のみ生成します\n")
    
    success_count = 0
    for idx, video in enumerate(videos_to_process):
        # 公開日を計算（1日あたり3記事）
        days_offset = idx // 3
        publish_date = (start_date + timedelta(days=days_offset)).strftime("%Y-%m-%d")
        
        content_id = video.get("content_id", f"video_{idx}")
        title = video.get("title", "不明")
        
        print(f"[{idx + 1}/{len(videos)}] {title}")
        print(f"  📅 公開日: {publish_date}")
        print(f"  🔄 記事生成中...")
        
        # Gemini APIで記事を生成
        article_content = generate_article(model, video)
        
        if article_content:
            # 記事を保存
            filepath = save_article(article_content, video, publish_date, str(content_dir))
            
            if filepath:
                print(f"  ✅ 保存完了: {filepath}")
                success_count += 1
            else:
                print(f"  ❌ 保存失敗")
        else:
            print(f"  ❌ 生成失敗")
        
        # レート制限対策：4秒待機
        if idx < len(videos_to_process) - 1:  # 最後の記事の後は待たない
            print(f"  ⏳ レート制限対策で4秒待機中...\n")
            time.sleep(4)
        else:
            print()
    
    # 完了メッセージ
    print("=" * 80)
    print(f"🎉 記事生成完了！")
    print(f"   成功: {success_count}/{len(videos_to_process)}件")
    if test_mode:
        print(f"   テストモード：{len(videos) - len(videos_to_process)}件の記事が残っています")
    print(f"   保存先: {content_dir}")
    print("=" * 80)


if __name__ == "__main__":
    main()

