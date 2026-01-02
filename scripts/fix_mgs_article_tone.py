#!/usr/bin/env python3
"""
MGS記事の口調を修正するスクリプト
タメ口スタイルを洗練されたスタイルに変更
"""

import re
from pathlib import Path
from datetime import datetime

# プロジェクトルート
script_dir = Path(__file__).parent
project_root = script_dir.parent
content_dir = project_root / "content"

# タメ口スタイルの見出しを洗練された見出しに置換
HEADING_REPLACEMENTS = {
    r"###?\s*タイトル見た瞬間、これヤバいって確信したわｗ": "## 作品との出会い",
    r"###?\s*見始めた瞬間に完全にやられたわｗ": "## 作品との出会い",
    r"###?\s*冒頭からマジで期待値ブチ上げだったわｗ": "## 作品との出会い",
    r"###?\s*最初の数秒で完全にハマったわｗ": "## 作品との出会い",
    r"###?\s*画面に映った瞬間、もう完全にやられたわｗ": "## 作品との出会い",
    r"###?\s*見始めた瞬間に「ああ、これは伝説だわ」って確信したわｗ": "## 作品との出会い",
    r"###?\s*冒頭からマジで興奮が止まらなかったわｗ": "## 作品との出会い",
    r"###?\s*最初のシーンで完全に引き込まれたわｗ": "## 作品との出会い",
    r"###?\s*始まった瞬間の「キタコレｗ」感": "## 作品との出会い",
    r"###?\s*ここがエロかったｗ.*": "## 心に残るシーン",
    r"###?\s*今すぐ見てこいｗ.*": "## 読者への語りかけ",
}

# タメ口表現の置換
TONE_REPLACEMENTS = [
    # 「だわ」→削除または「です」「である」
    (r"([。、])\s*だわ", r"\1"),
    (r"だわ\s*([。、])", r"\1"),
    (r"だわ\s*$", ""),
    (r"だわ\s*", ""),
    
    # 「マジで」→削除または「本当に」「まさに」
    (r"マジで\s*", ""),
    
    # 「ヤバい」→「印象的」「魅力的」「素晴らしい」
    (r"ヤバい", "印象的"),
    (r"ヤバかった", "印象的だった"),
    
    # 「ｗ」→削除
    (r"ｗ+", ""),
    (r"w+", ""),
    
    # 「抜ける」「昇天」→「心を奪われる」「感動する」
    (r"抜ける", "心を奪われる"),
    (r"昇天", "感動"),
    (r"昇天した", "感動した"),
    
    # 「エロかった」→「印象的だった」「魅力的だった」
    (r"エロかった", "印象的だった"),
    (r"エロくて", "魅力的で"),
    
    # 「俺」「お前」→「私」「読者」
    (r"俺の", "私の"),
    (r"俺は", "私は"),
    (r"俺が", "私が"),
    (r"俺を", "私を"),
    (r"俺に", "私に"),
    (r"お前", "読者"),
    (r"お前ら", "読者の皆様"),
    
    # 「〜すぎるｗ」→「〜すぎる」
    (r"すぎるｗ", "すぎる"),
    (r"すぎるw", "すぎる"),
    
    # 「〜んだわ」→「〜のだ」
    (r"んだわ", "のだ"),
    (r"んだわ\s*([。、])", r"のだ\1"),
    
    # 「〜だわ」→削除
    (r"だわ\s*([。、])", r"\1"),
    
    # 「〜だわ」→「〜だ」
    (r"だわ\s*$", "だ"),
    
    # 「〜だわ」→「〜である」
    (r"だわ\s+", "である。"),
    
    # 「〜だわ」→「〜だ」
    (r"だわ", "だ"),
]

def fix_article_tone(content: str) -> str:
    """記事の口調を修正"""
    # 見出しを修正
    for pattern, replacement in HEADING_REPLACEMENTS.items():
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    # タメ口表現を修正（改行を保持）
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        # 各行に対して修正を適用
        fixed_line = line
        for pattern, replacement in TONE_REPLACEMENTS:
            fixed_line = re.sub(pattern, replacement, fixed_line)
        fixed_lines.append(fixed_line)
    
    content = '\n'.join(fixed_lines)
    
    # 余分な空白行を整理（ただし改行は保持）
    content = re.sub(r"\n\s*\n\s*\n+", "\n\n", content)
    
    return content

def main():
    """メイン処理"""
    print("=" * 80)
    print("  MGS記事の口調修正")
    print("=" * 80 + "\n")
    
    # 2026-01-02の記事を取得
    mgs_articles = list(content_dir.glob("2026-01-02-*.md"))
    
    if not mgs_articles:
        print("❌ 修正対象の記事が見つかりません")
        return
    
    print(f"📋 {len(mgs_articles)}件の記事を確認します\n")
    
    fixed_count = 0
    skipped_count = 0
    
    for article_file in mgs_articles:
        try:
            with open(article_file, "r", encoding="utf-8") as f:
                original_content = f.read()
            
            # タメ口スタイルが含まれているかチェック
            has_tameguchi = any([
                "だわ" in original_content,
                "マジで" in original_content,
                "ヤバい" in original_content,
                "ｗ" in original_content,
                "w" in original_content and "www" in original_content.lower(),
                "抜ける" in original_content,
                "昇天" in original_content,
                "エロかった" in original_content,
            ])
            
            if not has_tameguchi:
                print(f"⏭️  {article_file.name} - 修正不要")
                skipped_count += 1
                continue
            
            # 口調を修正
            fixed_content = fix_article_tone(original_content)
            
            # 変更があった場合のみ保存
            if fixed_content != original_content:
                with open(article_file, "w", encoding="utf-8") as f:
                    f.write(fixed_content)
                print(f"✅ {article_file.name} - 修正完了")
                fixed_count += 1
            else:
                print(f"⏭️  {article_file.name} - 変更なし")
                skipped_count += 1
                
        except Exception as e:
            print(f"❌ {article_file.name} - エラー: {e}")
    
    print("\n" + "=" * 80)
    print(f"🎉 修正完了！")
    print(f"   修正: {fixed_count}件")
    print(f"   スキップ: {skipped_count}件")
    print("=" * 80)

if __name__ == "__main__":
    main()

