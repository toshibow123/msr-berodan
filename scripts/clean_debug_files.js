#!/usr/bin/env node
/**
 * Next.jsの静的エクスポート時に生成される不要なデバッグファイルを削除
 */

const fs = require('fs');
const path = require('path');

const outDir = path.join(__dirname, '..', 'out');

function deleteDebugFiles(dir) {
  let deletedCount = 0;
  
  if (!fs.existsSync(dir)) {
    console.log(`❌ ディレクトリが見つかりません: ${dir}`);
    return 0;
  }
  
  const files = fs.readdirSync(dir);
  
  for (const file of files) {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat.isDirectory()) {
      // 再帰的にディレクトリを探索
      deletedCount += deleteDebugFiles(filePath);
    } else if (stat.isFile()) {
      // 不要なデバッグファイルを削除
      if (
        file.startsWith('__next.') && file.endsWith('.txt') ||
        file === 'index.txt'
      ) {
        fs.unlinkSync(filePath);
        deletedCount++;
      }
    }
  }
  
  return deletedCount;
}

console.log('🧹 不要なデバッグファイルを削除中...');
const deleted = deleteDebugFiles(outDir);
console.log(`✅ ${deleted}個の不要なファイルを削除しました`);

