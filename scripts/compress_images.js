#!/usr/bin/env node
/**
 * compress_images.js — Auto-compress 2K images for API analysis
 * 
 * Problem: 2K Flow PNGs are ~9-13MB. Claude API rejects base64 images > 5MB,
 * crashing the entire conversation context. And when the LLM views 10+ images
 * in one conversation for QA, the total context easily exceeds the 30MB limit.
 * 
 * Solution: Two compression tiers:
 *   DEFAULT — ≤4MB / 1600px PNG (single-image API calls)
 *   --qa   — ≤300KB / 800px JPEG (multi-image QA sessions: 10×300KB = 3MB total)
 * 
 * Originals stay untouched for Pinterest/TikTok publishing.
 * 
 * Usage:
 *   node scripts/compress_images.js                         → default compress output\gemgen_batch\*.png
 *   node scripts/compress_images.js --dir overlaid          → default compress overlaid\*.png
 *   node scripts/compress_images.js --dir overlaid --qa     → QA-grade compress for caption verification
 *   node scripts/compress_images.js --dir "C:\path" --qa    → QA-grade compress any path
 */

const fs = require('fs');
const path = require('path');

let sharp;
try {
  sharp = require('sharp');
} catch (e) {
  console.error('❌ Sharp not installed. Run: npm install sharp');
  process.exit(1);
}

const PINGPT_ROOT = path.resolve(__dirname, '..');
const DEFAULT_BATCH_DIR = path.join(PINGPT_ROOT, 'output', 'gemgen_batch');

// === Compression Profiles ===
// DEFAULT: 4MB / 1600px — safe for single-image API calls (5MB limit)
// QA:     300KB / 800px — safe for 10-image QA sessions (30MB context limit)
const PROFILES = {
  default: {
    maxBytes: 4 * 1024 * 1024,
    maxDimension: 1600,
    format: 'auto',       // PNG first, fallback JPEG 85
    jpegQuality: 85,
    label: 'API (≤4MB)',
  },
  qa: {
    maxBytes: 300 * 1024,
    maxDimension: 800,
    format: 'jpeg',       // Always JPEG for max compression
    jpegQuality: 72,
    label: 'QA (≤300KB)',
  },
};

async function compressImage(inputPath, outputPath, profile) {
  const stats = fs.statSync(inputPath);
  const sizeMB = (stats.size / (1024 * 1024)).toFixed(2);
  const sizeKB = (stats.size / 1024).toFixed(0);

  if (stats.size <= profile.maxBytes && profile.format !== 'jpeg') {
    // Already small enough and not forced JPEG — copy as-is
    fs.copyFileSync(inputPath, outputPath);
    console.log(`  ✅ ${path.basename(inputPath)} (${sizeMB}MB) — already under limit, copied`);
    return;
  }

  const metadata = await sharp(inputPath).metadata();
  const { width, height } = metadata;
  const scale = Math.min(profile.maxDimension / Math.max(width, height), 1);
  const newWidth = Math.round(width * scale);
  const newHeight = Math.round(height * scale);

  let buffer;

  if (profile.format === 'jpeg') {
    // QA mode: always JPEG for maximum compression
    buffer = await sharp(inputPath)
      .resize(newWidth, newHeight, { fit: 'inside', withoutEnlargement: true })
      .jpeg({ quality: profile.jpegQuality })
      .toBuffer();
    outputPath = outputPath.replace(/\.png$/i, '.jpg');
  } else {
    // Default mode: try PNG first, fallback to JPEG
    buffer = await sharp(inputPath)
      .resize(newWidth, newHeight, { fit: 'inside', withoutEnlargement: true })
      .png({ compressionLevel: 9, adaptiveFiltering: true })
      .toBuffer();

    if (buffer.length > profile.maxBytes) {
      buffer = await sharp(inputPath)
        .resize(newWidth, newHeight, { fit: 'inside', withoutEnlargement: true })
        .jpeg({ quality: profile.jpegQuality })
        .toBuffer();
      outputPath = outputPath.replace(/\.png$/i, '.jpg');
    }
  }

  fs.writeFileSync(outputPath, buffer);
  const newSizeKB = (buffer.length / 1024).toFixed(0);
  const newSizeMB = (buffer.length / (1024 * 1024)).toFixed(2);
  const sizeLabel = buffer.length < 1024 * 1024 ? `${newSizeKB}KB` : `${newSizeMB}MB`;
  console.log(`  ✅ ${path.basename(inputPath)} (${sizeMB}MB → ${sizeLabel}) — ${width}x${height} → ${newWidth}x${newHeight}`);
}

async function main() {
  // Parse arguments
  const args = process.argv.slice(2);
  const dirIdx = args.indexOf('--dir');
  const qaMode = args.includes('--qa');
  const profile = qaMode ? PROFILES.qa : PROFILES.default;
  let sourceDir;

  if (dirIdx !== -1 && args[dirIdx + 1]) {
    const dirArg = args[dirIdx + 1];
    // Support relative (to batch dir) or absolute paths
    if (path.isAbsolute(dirArg)) {
      sourceDir = dirArg;
    } else {
      sourceDir = path.join(DEFAULT_BATCH_DIR, dirArg);
    }
  } else {
    sourceDir = DEFAULT_BATCH_DIR;
  }

  if (!fs.existsSync(sourceDir)) {
    console.error(`❌ Source directory not found: ${sourceDir}`);
    process.exit(1);
  }

  const analysisDir = path.join(sourceDir, 'analysis');
  if (!fs.existsSync(analysisDir)) {
    fs.mkdirSync(analysisDir, { recursive: true });
  } else {
    // Clean stale files from previous runs to avoid format conflicts
    // (e.g., old 2.5MB .png copies lingering when --qa creates .jpg)
    const staleFiles = fs.readdirSync(analysisDir)
      .filter(f => /\.(png|jpg|jpeg)$/i.test(f));
    if (staleFiles.length > 0) {
      for (const f of staleFiles) {
        fs.unlinkSync(path.join(analysisDir, f));
      }
      console.log(`  🧹 Cleaned ${staleFiles.length} stale files from previous run\n`);
    }
  }

  // Find all image files
  const images = fs.readdirSync(sourceDir)
    .filter(f => /\.(png|jpg|jpeg)$/i.test(f))
    .sort();

  if (images.length === 0) {
    console.error(`❌ No images found in ${sourceDir}`);
    process.exit(1);
  }

  console.log('═══════════════════════════════════════');
  console.log(`  Image Compressor — ${profile.label}`);
  console.log('═══════════════════════════════════════');
  console.log(`  Mode:   ${qaMode ? '🔬 QA (multi-image caption verification)' : '📷 Default (single-image API)'}`);
  console.log(`  Source: ${sourceDir}`);
  console.log(`  Output: ${analysisDir}`);
  console.log(`  Images: ${images.length}`);
  const limitLabel = profile.maxBytes < 1024 * 1024
    ? `${profile.maxBytes / 1024}KB`
    : `${profile.maxBytes / (1024 * 1024)}MB`;
  console.log(`  Target: ≤${limitLabel} | Max dimension: ${profile.maxDimension}px | Format: ${profile.format === 'jpeg' ? 'JPEG ' + profile.jpegQuality : 'PNG→JPEG fallback'}`);
  console.log('');

  let compressed = 0;
  let copied = 0;
  let totalOriginal = 0;
  let totalCompressed = 0;

  for (const img of images) {
    const inputPath = path.join(sourceDir, img);
    const outputPath = path.join(analysisDir, img);
    const origSize = fs.statSync(inputPath).size;
    totalOriginal += origSize;

    await compressImage(inputPath, outputPath, profile);

    // Check actual output (might be .jpg if PNG was too large)
    const actualOutput = fs.existsSync(outputPath) 
      ? outputPath 
      : outputPath.replace(/\.png$/i, '.jpg');
    const newSize = fs.statSync(actualOutput).size;
    totalCompressed += newSize;

    if (origSize > profile.maxBytes || profile.format === 'jpeg') {
      compressed++;
    } else {
      copied++;
    }
  }

  const savedMB = ((totalOriginal - totalCompressed) / (1024 * 1024)).toFixed(1);
  console.log('');
  console.log('═══════════════════════════════════════');
  console.log(`  ✅ ${images.length} images processed`);
  console.log(`     ${compressed} compressed | ${copied} already under limit`);
  console.log(`     ${(totalOriginal / (1024 * 1024)).toFixed(1)}MB → ${(totalCompressed / (1024 * 1024)).toFixed(1)}MB (saved ${savedMB}MB)`);
  console.log(`  📁 ${analysisDir}`);
  console.log('═══════════════════════════════════════');
}

main().catch(err => {
  console.error('❌ Fatal error:', err.message);
  process.exit(1);
});
