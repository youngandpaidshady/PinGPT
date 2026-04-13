#!/usr/bin/env node
/**
 * TrendTok — Text Overlay Engine v2.0
 * 
 * Burns bold ranked text onto generated images for TikTok carousels.
 * Uses Sharp + SVG text rendering (no Canvas/Python dependency).
 * 
 * v2.0 Changes:
 *   - Per-style font mapping (no more Impact-only)
 *   - Tight pill/bar text backgrounds instead of crude full-width gradient
 *   - Style-aware color accent system
 * 
 * Style → Font Mapping:
 *   - CINEMATIC: Bebas Neue (tall, cinematic display)
 *   - MANGA_RAW: Anton (heavy compressed, manga energy)
 *   - MANGA_TINT: Oswald Bold (geometric, clean contrast)
 *   - COVER/CLOSER: Bangers (loud, attention-grabbing)
 *   - FALLBACK: Impact → Arial Black → sans-serif
 * 
 * Usage:
 *   node scripts/overlay_text.js                        → process all slides from carousel_deck.json
 *   node scripts/overlay_text.js --input img.png --text "5. GOJO" --output out.png
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
const DECK_FILE = path.join(PINGPT_ROOT, 'carousel_deck.json');
const BATCH_DIR = path.join(PINGPT_ROOT, 'output', 'gemgen_batch');

// ─── Style-to-Font Presets ────────────────────────────────────
const STYLE_PRESETS = {
  cinematic: {
    font: 'Bebas Neue, Impact, Arial Black, sans-serif',
    letterSpacing: 4,
    textTransform: 'uppercase',
  },
  manga_raw: {
    font: 'Anton, Impact, Arial Black, sans-serif',
    letterSpacing: 2,
    textTransform: 'uppercase',
  },
  manga_tint: {
    font: 'Oswald, Impact, Arial Black, sans-serif',
    letterSpacing: 3,
    textTransform: 'uppercase',
  },
  cover: {
    font: 'Bangers, Impact, Arial Black, sans-serif',
    letterSpacing: 5,
    textTransform: 'uppercase',
  },
  closer: {
    font: 'Bangers, Impact, Arial Black, sans-serif',
    letterSpacing: 5,
    textTransform: 'uppercase',
  },
};

// ─── Background Style Presets ─────────────────────────────────
const BG_STYLES = {
  // Tight pill behind each line
  pill: (x, y, textWidth, fontSize) => {
    const padX = fontSize * 0.4;
    const padY = fontSize * 0.2;
    const rx = fontSize * 0.15; // rounded corners
    return `<rect x="${x - textWidth/2 - padX}" y="${y - fontSize + padY}" 
      width="${textWidth + padX * 2}" height="${fontSize + padY * 2}" 
      rx="${rx}" ry="${rx}" 
      fill="black" fill-opacity="0.55"/>`;
  },
  // Subtle bottom fade — only for cinematic
  fade: (startY, height, imgWidth, imgHeight) => {
    return `
      <defs>
        <linearGradient id="fadeGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="black" stop-opacity="0"/>
          <stop offset="40%" stop-color="black" stop-opacity="0.3"/>
          <stop offset="100%" stop-color="black" stop-opacity="0.75"/>
        </linearGradient>
      </defs>
      <rect x="0" y="${startY}" width="${imgWidth}" height="${imgHeight - startY}" fill="url(#fadeGrad)"/>`;
  },
  // No background — just stroke for readability
  none: () => '',
};

// ─── Estimate text width (rough heuristic for SVG) ───────────
function estimateTextWidth(text, fontSize, letterSpacing) {
  // Average character width ≈ 0.55 * fontSize for bold condensed fonts
  const charWidth = fontSize * 0.55;
  return text.length * charWidth + (text.length - 1) * letterSpacing;
}

// ─── Resolve font preset from slide type + style ─────────────
function resolvePreset(slideType, slideStyle) {
  const type = (slideType || '').toLowerCase();
  const style = (slideStyle || '').toLowerCase();
  
  // COVER and CLOSER get their own treatment
  if (type === 'cover') return STYLE_PRESETS.cover;
  if (type === 'closer') return STYLE_PRESETS.closer;
  
  // Otherwise map by visual style
  return STYLE_PRESETS[style] || STYLE_PRESETS.cinematic;
}

// ─── Determine background approach ──────────────────────────
function resolveBgStyle(slideType, slideStyle) {
  const type = (slideType || '').toLowerCase();
  const style = (slideStyle || '').toLowerCase();
  
  if (type === 'cover' || type === 'closer') return 'pill';
  if (style === 'cinematic') return 'fade';
  if (style === 'manga_raw') return 'none'; // B&W manga looks cleaner without bg
  if (style === 'manga_tint') return 'pill';
  return 'fade';
}

// ─── SVG Text Generator ──────────────────────────────────────
function createTextSVG(lines, imgWidth, imgHeight, spec, slideType, slideStyle) {
  const preset = resolvePreset(slideType, slideStyle);
  const bgStyleName = resolveBgStyle(slideType, slideStyle);
  
  const {
    color = '#FFFFFF',
    stroke = '#000000',
    strokeWidth = 4,
    position = 'center-bottom',
  } = spec;
  
  // Use preset font, but allow spec override
  const fontFamily = spec.font && spec.font !== 'Impact' 
    ? spec.font 
    : preset.font;
  const letterSpacing = preset.letterSpacing || 2;

  // Scale font size to image width
  const baseFontSize = Math.round(imgWidth * 0.065);
  const titleFontSize = Math.round(baseFontSize * 1.4);
  const commentFontSize = Math.round(baseFontSize * 0.75);
  const lineSpacing = Math.round(baseFontSize * 1.6);

  // Determine Y position
  let startY;
  switch (position) {
    case 'center':
      startY = Math.round(imgHeight * 0.45);
      break;
    case 'center-bottom':
      startY = Math.round(imgHeight * 0.60);
      break;
    case 'bottom':
      startY = Math.round(imgHeight * 0.75);
      break;
    default:
      startY = Math.round(imgHeight * 0.60);
  }

  // Build background elements
  let bgElements = '';
  
  if (bgStyleName === 'fade') {
    const fadeStart = Math.round(startY - lineSpacing * 2);
    bgElements = BG_STYLES.fade(fadeStart, lineSpacing * (lines.length + 3), imgWidth, imgHeight);
  }

  // Build text elements with per-line pill backgrounds
  let textElements = '';
  let pillElements = '';
  
  lines.forEach((line, i) => {
    if (!line) return;
    const fontSize = i === 0 ? titleFontSize : commentFontSize;
    const y = startY + (i * lineSpacing);

    // Escape XML
    const escapedLine = line
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');

    // Pill background per line (if pill mode)
    if (bgStyleName === 'pill') {
      const textWidth = estimateTextWidth(line, fontSize, letterSpacing);
      pillElements += BG_STYLES.pill(imgWidth / 2, y, textWidth, fontSize);
    }

    // Stroke layer (outline)
    textElements += `
      <text x="50%" y="${y}" 
        font-family="${fontFamily}" 
        font-size="${fontSize}" 
        font-weight="900"
        text-anchor="middle" 
        fill="none"
        stroke="${stroke}" 
        stroke-width="${strokeWidth * 2}"
        stroke-linejoin="round"
        letter-spacing="${letterSpacing}"
      >${escapedLine}</text>`;
    
    // Fill layer
    textElements += `
      <text x="50%" y="${y}" 
        font-family="${fontFamily}" 
        font-size="${fontSize}" 
        font-weight="900"
        text-anchor="middle" 
        fill="${color}"
        letter-spacing="${letterSpacing}"
      >${escapedLine}</text>`;
  });

  return Buffer.from(`
    <svg width="${imgWidth}" height="${imgHeight}" xmlns="http://www.w3.org/2000/svg">
      ${bgElements}
      ${pillElements}
      ${textElements}
    </svg>
  `);
}

// ─── Process single image ─────────────────────────────────────
async function overlayImage(inputPath, outputPath, lines, spec, slideType, slideStyle) {
  const metadata = await sharp(inputPath).metadata();
  const { width, height } = metadata;

  const svgOverlay = createTextSVG(lines, width, height, spec, slideType, slideStyle);

  await sharp(inputPath)
    .composite([{
      input: svgOverlay,
      top: 0,
      left: 0,
    }])
    .png()
    .toFile(outputPath);

  const stats = fs.statSync(outputPath);
  console.log(`  ✅ ${path.basename(outputPath)} (${Math.round(stats.size / 1024)}KB)`);
}

// ─── Batch mode: Process all slides from carousel_deck.json ───
async function processDeck() {
  if (!fs.existsSync(DECK_FILE)) {
    console.error('❌ No carousel_deck.json found. Run carousel_planner.js first!');
    process.exit(1);
  }

  const deck = JSON.parse(fs.readFileSync(DECK_FILE, 'utf-8'));
  console.log(`[Deck] "${deck.topic}" — ${deck.slide_count} slides\n`);

  // #8: Validate — warn if any slide has hardcoded font override
  const fontOverrides = deck.slides.filter(s => s.text_overlay?.spec?.font);
  if (fontOverrides.length > 0) {
    console.warn(`  ⚠️  ${fontOverrides.length} slide(s) have explicit font overrides (engine auto-selects per style):`);
    fontOverrides.forEach(s => console.warn(`     Slide ${s.slide_num}: "${s.text_overlay.spec.font}" — consider removing to use style default`));
    console.log();
  }

  // Find image files in batch dir
  const images = fs.readdirSync(BATCH_DIR)
    .filter(f => /\.(png|jpg|jpeg)$/i.test(f))
    .sort((a, b) => {
      const numA = parseInt((a.match(/(\d+)\.\w+$/) || ['','0'])[1]);
      const numB = parseInt((b.match(/(\d+)\.\w+$/) || ['','0'])[1]);
      return numA - numB;
    });

  if (images.length === 0) {
    console.error('❌ No images found in output/gemgen_batch/. Generate images first!');
    process.exit(1);
  }

  if (images.length < deck.slides.length) {
    console.warn(`⚠️  Only ${images.length} images for ${deck.slides.length} slides. Processing available images.`);
  }

  // Create overlay output dir
  const overlayDir = path.join(BATCH_DIR, 'overlaid');
  if (!fs.existsSync(overlayDir)) fs.mkdirSync(overlayDir, { recursive: true });

  // Process each slide
  for (let i = 0; i < Math.min(images.length, deck.slides.length); i++) {
    const slide = deck.slides[i];
    const inputPath = path.join(BATCH_DIR, images[i]);
    const outputPath = path.join(overlayDir, `trendtok_${String(i + 1).padStart(2, '0')}.png`);

    const preset = resolvePreset(slide.type, slide.style);
    console.log(`  Slide ${slide.slide_num} [${slide.type}] [${slide.style}] — "${slide.title}" (font: ${preset.font.split(',')[0]})`);
    await overlayImage(inputPath, outputPath, slide.text_overlay.lines, slide.text_overlay.spec, slide.type, slide.style);
  }

  console.log(`\n═══════════════════════════════════════`);
  console.log(`✅ ${Math.min(images.length, deck.slides.length)} slides overlaid → output/gemgen_batch/overlaid/`);
  console.log(`═══════════════════════════════════════`);
}

// ─── Single image mode ────────────────────────────────────────
async function processSingle(inputPath, text, outputPath) {
  const lines = text.split('\\n');
  const spec = { color: '#FFFFFF', stroke: '#000000', strokeWidth: 4, position: 'center-bottom' };
  await overlayImage(inputPath, outputPath, lines, spec, 'ENTRY', 'cinematic');
}

// ─── Main ─────────────────────────────────────────────────────
async function main() {
  console.log('═══════════════════════════════════════');
  console.log('  TrendTok — Text Overlay Engine v2.0');
  console.log('═══════════════════════════════════════\n');

  const args = process.argv.slice(2);
  const inputIdx = args.indexOf('--input');
  const textIdx = args.indexOf('--text');
  const outputIdx = args.indexOf('--output');

  if (inputIdx !== -1 && textIdx !== -1 && outputIdx !== -1) {
    await processSingle(args[inputIdx + 1], args[textIdx + 1], args[outputIdx + 1]);
  } else {
    await processDeck();
  }
}

main().catch(err => {
  console.error('❌ Fatal error:', err.message);
  process.exit(1);
});
