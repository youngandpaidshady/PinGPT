#!/usr/bin/env node
/**
 * TrendTok One-Shot Pipeline — Master Orchestrator
 * 
 * One command. Results in Drive. Zero babysitting.
 * 
 * Chains 10 phases:
 *   0. Cleanup         — Clear old batch, kill stale processes
 *   1. VPN Check       — Verify/rotate ExpressVPN
 *   2. Fresh Project   — Create new Flow project, save URL
 *   3. Submit Prompts  — Smart batching with VPN-aware delays
 *   4. Wait & Retry    — Poll for failures, exit→re-enter→resubmit, NB Pro fallback
 *   5. Download 2K     — CDP download with escape recovery from Downloads folder
 *   6. Rename & Strip  — Sort by mtime (reverse-chrono fix), convert to PNG via Sharp, strip AI metadata
 *   7. Overlay         — Run overlay_text.js
 *  7.5a. Compress      — Run compress_images.js --dir overlaid
 *  7.5b. Mismatch Gate — LLM visual verification (prints paths for agent to view_file)
 *   8. Metadata        — Generate tiktok_metadata.txt
 *   9. Upload          — python upload_drive.py --clean
 * 
 * Usage:
 *   node scripts/trendtok_oneshot.js                → full pipeline
 *   node scripts/trendtok_oneshot.js --dry-run      → phases 6-9 only (skip Flow)
 *   node scripts/trendtok_oneshot.js --from-overlay  → phases 7-9 only (skip gen+download)
 *   node scripts/trendtok_oneshot.js --from-upload   → phase 9 only
 * 
 * Prereqs:
 *   - Chrome open with Google login + CDP port 9222
 *   - ExpressVPN CLI installed (optional, recommended)
 *   - gemgen_queue.json populated with prompts
 *   - carousel_deck.json populated with deck data
 */

const { chromium } = require('playwright');
const { execSync, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

let sharp;
try {
  sharp = require('sharp');
} catch (e) {
  console.error('❌ Sharp not installed. Run: npm install sharp');
  process.exit(1);
}

// ─── Paths ────────────────────────────────────────────
const PINGPT_ROOT = path.resolve(__dirname, '..');
const SCRIPTS_DIR = __dirname;
const BATCH_DIR = path.join(PINGPT_ROOT, 'output', 'gemgen_batch');
const OVERLAID_DIR = path.join(BATCH_DIR, 'overlaid');
const ANALYSIS_DIR = path.join(OVERLAID_DIR, 'analysis');
const QUEUE_FILE = path.join(PINGPT_ROOT, 'gemgen_queue.json');
const DECK_FILE = path.join(PINGPT_ROOT, 'carousel_deck.json');
const DOWNLOADS_DIR = 'C:\\Users\\Administrator\\Downloads';
const VPN_EXE = 'C:\\Program Files\\ExpressVPN\\expressvpnctl.exe';
const CDP_PORT = 9222;

const VPN_CITIES = ['usa-chicago', 'usa-dallas', 'usa-denver', 'usa-seattle', 'usa-miami'];

// ─── CLI Args ─────────────────────────────────────────
const args = new Set(process.argv.slice(2));
const DRY_RUN = args.has('--dry-run');
const FROM_OVERLAY = args.has('--from-overlay');
const FROM_UPLOAD = args.has('--from-upload');

// ─── Helpers ──────────────────────────────────────────
function header(phase, text) {
  const line = '═'.repeat(55);
  console.log(`\n${line}`);
  console.log(`  Phase ${phase}: ${text}`);
  console.log(`${line}\n`);
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

function runCmd(cmd, opts = {}) {
  try {
    return execSync(cmd, { encoding: 'utf-8', stdio: opts.silent ? 'pipe' : 'inherit', cwd: PINGPT_ROOT, ...opts });
  } catch (e) {
    if (!opts.ignoreError) throw e;
    return e.stdout || '';
  }
}

function runCmdOutput(cmd) {
  try {
    return execSync(cmd, { encoding: 'utf-8', cwd: PINGPT_ROOT }).trim();
  } catch (e) {
    return '';
  }
}

function loadQueue() {
  return JSON.parse(fs.readFileSync(QUEUE_FILE, 'utf-8'));
}

function loadDeck() {
  return JSON.parse(fs.readFileSync(DECK_FILE, 'utf-8'));
}

function saveQueue(data) {
  fs.writeFileSync(QUEUE_FILE, JSON.stringify(data, null, 2));
}

// ════════════════════════════════════════════════════════
// PHASE 0: Cleanup
// ════════════════════════════════════════════════════════
function phase0_cleanup() {
  header('0', 'Workspace Cleanup');

  // Kill stale node processes (> 10 min old)
  console.log('🔪 Killing stale node processes...');
  runCmd('powershell -Command "Get-Process node -ErrorAction SilentlyContinue | Where-Object { (New-TimeSpan $_.StartTime).TotalMinutes -gt 10 } | ForEach-Object { Write-Host \\"  Killing PID $($_.Id)\\"; Stop-Process -Id $_.Id -Force }"', { ignoreError: true, silent: false });

  // Clear old batch images
  if (fs.existsSync(BATCH_DIR)) {
    const oldFiles = fs.readdirSync(BATCH_DIR).filter(f => /\.(png|jpg|jpeg)$/i.test(f));
    if (oldFiles.length > 0) {
      console.log(`🗑️  Clearing ${oldFiles.length} old images from gemgen_batch/`);
      oldFiles.forEach(f => fs.unlinkSync(path.join(BATCH_DIR, f)));
    }
  }
  if (!fs.existsSync(BATCH_DIR)) fs.mkdirSync(BATCH_DIR, { recursive: true });

  // Clear old overlaid
  if (fs.existsSync(OVERLAID_DIR)) {
    const oldOverlaid = fs.readdirSync(OVERLAID_DIR).filter(f => /\.(png|jpg|jpeg|html|txt)$/i.test(f));
    if (oldOverlaid.length > 0) {
      console.log(`🗑️  Clearing ${oldOverlaid.length} old files from overlaid/`);
      oldOverlaid.forEach(f => fs.unlinkSync(path.join(OVERLAID_DIR, f)));
    }
  }

  // Clear old analysis
  if (fs.existsSync(ANALYSIS_DIR)) {
    const oldAnalysis = fs.readdirSync(ANALYSIS_DIR).filter(f => /\.(png|jpg|jpeg)$/i.test(f));
    if (oldAnalysis.length > 0) {
      console.log(`🗑️  Clearing ${oldAnalysis.length} old files from analysis/`);
      oldAnalysis.forEach(f => fs.unlinkSync(path.join(ANALYSIS_DIR, f)));
    }
  }

  console.log('✅ Workspace clean.\n');
}

// ════════════════════════════════════════════════════════
// PHASE 1: VPN Check
// ════════════════════════════════════════════════════════
function phase1_vpnCheck() {
  header('1', 'VPN Rotation (Fresh IP)');

  if (!fs.existsSync(VPN_EXE)) {
    console.log('⚠️  ExpressVPN not found. Running without VPN (batching delays will apply).');
    return { vpnActive: false };
  }

  const status = runCmdOutput(`"${VPN_EXE}" status`);
  console.log(`  Current VPN Status: ${status}`);

  // Always force-rotate to prevent stale IP flagging
  if (status.toLowerCase().includes('connected')) {
    console.log('🔄 Disconnecting current VPN to rotate server...');
    runCmd(`"${VPN_EXE}" disconnect`, { ignoreError: true, silent: true });
    // Wait for disconnect
    for (let i = 0; i < 5; i++) {
      const check = runCmdOutput(`"${VPN_EXE}" status`);
      if (!check.toLowerCase().includes('connected')) break;
      execSync('ping 127.0.0.1 -n 2 > nul', { stdio: 'ignore' });
    }
    console.log('  ✅ Disconnected.');
  }

  // Connect to a random US city
  const city = VPN_CITIES[Math.floor(Math.random() * VPN_CITIES.length)];
  console.log(`🔄 Connecting to fresh server: ${city}...`);
  runCmd(`"${VPN_EXE}" connect ${city}`, { ignoreError: true, silent: true });
  
  // Wait and verify
  for (let i = 0; i < 10; i++) {
    const check = runCmdOutput(`"${VPN_EXE}" status`);
    if (check.toLowerCase().includes('connected')) {
      console.log(`✅ VPN rotated to ${city}. Fresh IP active.\n`);
      return { vpnActive: true };
    }
    execSync('ping 127.0.0.1 -n 3 > nul', { stdio: 'ignore' });
  }

  console.log('⚠️  VPN connection failed. Running without VPN.\n');
  return { vpnActive: false };
}

// ════════════════════════════════════════════════════════
// PHASE 2: Create Fresh Flow Project
// ════════════════════════════════════════════════════════
async function phase2_freshProject(browser) {
  header('2', 'Create Fresh Flow Project');

  // Close ALL existing Flow tabs (prevent stale tab contamination)
  for (const ctx of browser.contexts()) {
    for (const p of ctx.pages()) {
      if (p.url().includes('labs.google/fx/tools/flow/project/')) {
        console.log(`  Closing stale Flow tab: ${p.url().substring(0, 80)}...`);
        await p.close().catch(() => {});
      }
    }
  }

  const page = await browser.contexts()[0].newPage();
  console.log('  Navigating to Flow home...');
  await page.goto('https://labs.google/fx/tools/flow', { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(3000);

  // Click New Project
  console.log('  Creating new project...');
  const selectors = [
    'button:has-text("New project")',
    'button:has-text("Create new")',
    '[aria-label="New project"]',
    '[aria-label="Create new project"]',
  ];

  let clicked = false;
  for (const sel of selectors) {
    if (await page.locator(sel).count() > 0) {
      await page.locator(sel).first().click();
      clicked = true;
      console.log(`  Clicked: ${sel}`);
      break;
    }
  }
  if (!clicked) {
    // Fallback: click first button
    const buttons = await page.locator('button').all();
    if (buttons.length > 0) await buttons[0].click();
  }

  await page.waitForURL('**/flow/project/*', { timeout: 15000 }).catch(() => {});
  const projectUrl = page.url();

  if (!projectUrl.includes('/project/')) {
    throw new Error('Failed to create new Flow project. URL: ' + projectUrl);
  }

  console.log(`✅ New project: ${projectUrl}\n`);

  // Update queue file
  const queue = loadQueue();
  queue.flow_project_url = projectUrl;
  saveQueue(queue);

  return { page, projectUrl };
}

// ════════════════════════════════════════════════════════
// PHASE 3: Submit Prompts
// ════════════════════════════════════════════════════════
async function phase3_submitPrompts(page, vpnActive) {
  header('3', 'Submit Prompts');

  const queue = loadQueue();
  const prompts = queue.items.map(i => i.prompt);
  const batchSize = vpnActive ? prompts.length : 3; // VPN: all at once. No VPN: batch of 3
  const delay = vpnActive ? 2000 : 10000; // VPN: 2s. No VPN: 10s

  console.log(`  Prompts: ${prompts.length}`);
  console.log(`  Batch size: ${batchSize} | Delay: ${delay / 1000}s`);
  console.log(`  VPN: ${vpnActive ? 'ACTIVE (back-to-back)' : 'OFF (batching)'}\n`);

  // Set 9:16 aspect ratio on first prompt
  const textbox = page.locator('div[role="textbox"]').first();
  await textbox.waitFor({ state: 'visible', timeout: 15000 });
  await textbox.click();
  await page.waitForTimeout(1000);

  const ratioBtn = page.locator('text="9:16", span:has-text("9:16"), button:has-text("9:16")').first();
  if (await ratioBtn.count() > 0) {
    await ratioBtn.click({ force: true }).catch(() => {});
    console.log('  Set aspect ratio to 9:16');
  }

  const submitted = [];
  const failed = [];

  for (let i = 0; i < prompts.length; i++) {
    const prompt = prompts[i];
    const slideLabel = queue.items[i].slide || `#${i + 1}`;

    // Batch delay
    if (i > 0 && i % batchSize === 0) {
      console.log(`\n  ⏳ Batch delay (${delay / 1000}s)...`);
      await sleep(delay);
    }

    console.log(`  [${i + 1}/${prompts.length}] ${slideLabel}...`);

    try {
      await textbox.click();
      await page.keyboard.press('Control+A');
      await page.keyboard.press('Backspace');
      await textbox.fill(prompt);
      await page.waitForTimeout(1000);

      const createBtn = page.locator('button', { hasText: 'Create' }).last();
      await createBtn.click({ timeout: 5000 });
      console.log(`    ✅ Submitted`);
      submitted.push(i);
      await page.waitForTimeout(2000);
    } catch (e) {
      console.log(`    ❌ Failed: ${e.message.substring(0, 80)}`);
      failed.push({ index: i, prompt, error: e.message, strikes: 1 });
    }
  }

  console.log(`\n  Submitted: ${submitted.length}/${prompts.length}`);
  if (failed.length > 0) console.log(`  Failed: ${failed.length} (will retry in Phase 4)`);

  return { submitted, failed };
}

// ════════════════════════════════════════════════════════
// PHASE 4: Wait for Generation & Retry Failures
// ════════════════════════════════════════════════════════
async function phase4_waitAndRetry(page, projectUrl, failedFromPhase3) {
  header('4', 'Wait for Generation & Retry Failures');

  const queue = loadQueue();
  const totalPrompts = queue.items.length;

  // Wait for images to appear in the grid
  console.log(`  Waiting for ${totalPrompts} images to generate...`);
  let images = [];
  let lastCount = 0;
  let staleRounds = 0;

  for (let attempt = 0; attempt < 60; attempt++) {
    images = await page.locator('img[alt="Generated image"]').all();
    if (images.length === 0) {
      // Fallback selector
      const allImgs = await page.locator('img[src*="http"]').all();
      images = [];
      for (const img of allImgs) {
        const alt = await img.getAttribute('alt').catch(() => '');
        if (alt !== 'User profile image') images.push(img);
      }
    }

    if (images.length >= totalPrompts) {
      console.log(`\n  ✅ All ${images.length} images generated!`);
      break;
    }

    if (images.length === lastCount) {
      staleRounds++;
    } else {
      staleRounds = 0;
      lastCount = images.length;
    }

    // Check for failures after 30s of no progress
    if (staleRounds > 6) {
      const errorCount = await page.locator(':text("Something went wrong")').count();
      if (errorCount > 0) {
        console.log(`\n  ⚠️  ${errorCount} failed generation(s) detected. Initiating recovery...`);
        // EXIT → RE-ENTER → RESUBMIT pattern
        await page.goto('https://labs.google/fx/tools/flow', { waitUntil: 'networkidle', timeout: 15000 });
        await page.waitForTimeout(3000);
        await page.goto(projectUrl, { waitUntil: 'networkidle', timeout: 15000 });
        await page.waitForTimeout(3000);
        staleRounds = 0;
        continue;
      }
    }

    process.stdout.write(`\r  Generated: ${images.length}/${totalPrompts} (waiting ${attempt * 5}s)...   `);
    await sleep(5000);
  }

  console.log('');

  // Retry failed prompts from Phase 3
  if (failedFromPhase3.length > 0) {
    console.log(`\n  🔄 Retrying ${failedFromPhase3.length} failed prompt(s)...`);
    const textbox = page.locator('div[role="textbox"]').first();

    for (const fail of failedFromPhase3) {
      console.log(`  Retrying: ${queue.items[fail.index].slide || `#${fail.index + 1}`} (strike ${fail.strikes})...`);

      // If 2+ strikes, try switching to NB Pro
      if (fail.strikes >= 2) {
        console.log('    🔀 Switching to NanoBanana Pro (2-strike rule)...');
        // Try to find and click model selector
        const modelBtns = await page.locator('button:has-text("NanoBanana"), [aria-label*="model"]').all();
        for (const btn of modelBtns) {
          await btn.click({ force: true, timeout: 3000 }).catch(() => {});
          await page.waitForTimeout(1000);
        }
        const proOption = page.locator('text="NanoBanana Pro", [data-value*="pro"]').first();
        if (await proOption.count() > 0) {
          await proOption.click({ force: true }).catch(() => {});
          console.log('    ✅ Switched to NB Pro');
        }
      }

      try {
        await textbox.click();
        await page.keyboard.press('Control+A');
        await page.keyboard.press('Backspace');
        await textbox.fill(fail.prompt);
        await page.waitForTimeout(1000);
        const createBtn = page.locator('button', { hasText: 'Create' }).last();
        await createBtn.click({ timeout: 5000 });
        console.log(`    ✅ Resubmitted`);
        await sleep(3000);
      } catch (e) {
        fail.strikes++;
        if (fail.strikes >= 3) {
          console.log(`    ❌ Giving up after 3 strikes (model limitation): ${e.message.substring(0, 60)}`);
        } else {
          console.log(`    ❌ Strike ${fail.strikes}: ${e.message.substring(0, 60)}`);
        }
      }
    }

    // Wait for retried images
    console.log('\n  Waiting for retried generations...');
    await sleep(30000);
  }

  // Final image count
  images = await page.locator('img[alt="Generated image"]').all();
  if (images.length === 0) {
    const allImgs = await page.locator('img[src*="http"]').all();
    images = [];
    for (const img of allImgs) {
      const alt = await img.getAttribute('alt').catch(() => '');
      if (alt !== 'User profile image') images.push(img);
    }
  }
  console.log(`  Final image count: ${images.length}/${totalPrompts}`);

  return images.length;
}

// ════════════════════════════════════════════════════════
// PHASE 5: Download 2K Images
// ════════════════════════════════════════════════════════
async function phase5_download2K(page, projectUrl) {
  header('5', 'Download 2K Images');

  const queue = loadQueue();
  const targetCount = queue.items.length;
  const prefix = (queue.session_id || 'trendtok').replace(/_run$/, '');

  // Snapshot Downloads folder BEFORE starting
  const downloadsBefore = new Set(
    fs.existsSync(DOWNLOADS_DIR) ? fs.readdirSync(DOWNLOADS_DIR) : []
  );
  console.log(`  📸 Snapshot: ${downloadsBefore.size} files in Downloads folder`);

  // Set CDP download behavior
  const cdpSession = await page.context().newCDPSession(page);
  await cdpSession.send('Browser.setDownloadBehavior', {
    behavior: 'allowAndName',
    downloadPath: BATCH_DIR,
    eventsEnabled: true,
  });
  console.log(`  CDP download redirect set to ${BATCH_DIR}`);

  // Reload to fresh state
  await page.reload({ waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(3000);

  // Scroll to load all images
  for (let s = 0; s < 5; s++) {
    await page.mouse.wheel(0, 500);
    await page.waitForTimeout(500);
  }
  await page.mouse.wheel(0, -5000);
  await page.waitForTimeout(1000);

  // Find all images
  let images = await page.locator('img[alt="Generated image"]').all();
  if (images.length === 0) {
    const allImgs = await page.locator('img[src*="http"]').all();
    images = [];
    for (const img of allImgs) {
      const alt = await img.getAttribute('alt').catch(() => '');
      if (alt !== 'User profile image') images.push(img);
    }
  }
  console.log(`  Found ${images.length} images in grid\n`);

  let downloaded = 0;
  let failed = 0;

  for (let i = 0; i < images.length; i++) {
    console.log(`  [${i + 1}/${images.length}] Downloading 2K...`);

    try {
      // Click image to open detail view
      await images[i].click({ timeout: 5000, force: true }).catch(async () => {
        await images[i].evaluate(n => n.click());
      });
      await page.waitForTimeout(3000);

      // Find download button
      let downloadClicked = false;
      for (const sel of ['button[aria-label*="ownload"]', 'button[data-tooltip*="ownload"]', 'button:has(.google-symbols:text("download"))', '.google-symbols:text("download")', 'button:has-text("download")']) {
        const btn = page.locator(sel).first();
        if (await btn.count() > 0) {
          await btn.click({ timeout: 3000, force: true }).catch(() => {});
          downloadClicked = true;
          break;
        }
      }
      if (!downloadClicked) {
        console.log(`    ❌ No download button`);
        failed++;
        await page.goto(projectUrl, { waitUntil: 'networkidle', timeout: 15000 }).catch(() => {});
        await page.waitForTimeout(2000);
        images = await refreshImageList(page);
        continue;
      }
      await page.waitForTimeout(1500);

      // Click 2K
      let twoKClicked = false;
      for (const sel of ['text=2K', 'button:has-text("2K")', '[aria-label*="2K"]', 'text=Upscaled']) {
        const btn = page.locator(sel).first();
        if (await btn.count() > 0) {
          const [download] = await Promise.all([
            page.waitForEvent('download', { timeout: 45000 }),
            btn.click({ timeout: 3000, force: true }).catch(async () => {
              await btn.evaluate(b => b.click());
            })
          ]);
          const outFile = path.join(BATCH_DIR, `${prefix}_${i + 1}.png`);
          await download.saveAs(outFile);
          const stats = fs.statSync(outFile);
          console.log(`    ✅ ${path.basename(outFile)} (${Math.round(stats.size / 1024)}KB)`);
          downloaded++;
          twoKClicked = true;
          break;
        }
      }
      if (!twoKClicked) {
        console.log(`    ❌ No 2K button`);
        failed++;
      }
    } catch (err) {
      console.log(`    ❌ ${err.message.substring(0, 100)}`);
      failed++;
    }

    // Navigate back to grid
    await page.goto(projectUrl, { waitUntil: 'networkidle', timeout: 15000 }).catch(() => {});
    await page.waitForTimeout(2000);
    images = await refreshImageList(page);
  }

  // ── Download Escape Recovery ──
  console.log('\n  🔍 Checking for escaped downloads...');
  const downloadsAfter = fs.existsSync(DOWNLOADS_DIR) ? fs.readdirSync(DOWNLOADS_DIR) : [];
  const escaped = downloadsAfter.filter(f => !downloadsBefore.has(f) && /\.(png|jpg|jpeg|webp)$/i.test(f));

  if (escaped.length > 0) {
    console.log(`  ⚠️  ${escaped.length} file(s) escaped to Downloads folder. Recovering...`);
    escaped.forEach(f => {
      const src = path.join(DOWNLOADS_DIR, f);
      const dest = path.join(BATCH_DIR, f);
      fs.renameSync(src, dest);
      console.log(`    📦 Moved: ${f}`);
    });
  } else {
    console.log('  ✅ No escaped downloads.');
  }

  // Also check for extensionless UUID files and recover those
  const uuidFiles = fs.readdirSync(BATCH_DIR).filter(f => !path.extname(f) && f.length > 20);
  if (uuidFiles.length > 0) {
    console.log(`  📦 Found ${uuidFiles.length} UUID file(s) — will be processed in Phase 6.`);
  }

  console.log(`\n  Downloaded: ${downloaded} | Failed: ${failed} | Escaped recovered: ${escaped.length}`);
  const totalOnDisk = fs.readdirSync(BATCH_DIR).filter(f => f !== 'overlaid' && f !== 'approved' && f !== 'rejected' && f !== 'analysis').length;
  console.log(`  Total files on disk: ${totalOnDisk}`);

  return { downloaded, failed, escaped: escaped.length };
}

async function refreshImageList(page) {
  let images = await page.locator('img[alt="Generated image"]').all();
  if (images.length === 0) {
    const allImgs = await page.locator('img[src*="http"]').all();
    images = [];
    for (const img of allImgs) {
      const alt = await img.getAttribute('alt').catch(() => '');
      if (alt !== 'User profile image') images.push(img);
    }
  }
  return images;
}

// ════════════════════════════════════════════════════════
// PHASE 6: Rename & Strip AI Metadata
// ════════════════════════════════════════════════════════
async function phase6_renameAndStrip() {
  header('6', 'Rename & Strip AI Metadata');

  const queue = loadQueue();
  const prefix = (queue.session_id || 'trendtok').replace(/_run$/, '');

  // Find all files that need processing
  // UUID files (no extension) + any JPEG/PNG that aren't already properly named
  const allFiles = fs.readdirSync(BATCH_DIR)
    .filter(f => {
      if (fs.statSync(path.join(BATCH_DIR, f)).isDirectory()) return false;
      // Include extensionless UUID files
      if (!path.extname(f)) return true;
      // Include image files
      if (/\.(png|jpg|jpeg|webp)$/i.test(f)) return true;
      return false;
    });

  if (allFiles.length === 0) {
    console.log('  ❌ No files to process!');
    return;
  }

  // ── REVERSE-CHRONO FIX ──
  // Sort by mtime ascending (oldest first = Slide 1)
  // Flow displays newest first, so the first downloaded image is actually the LAST prompt
  const filesWithMtime = allFiles.map(f => ({
    name: f,
    fullPath: path.join(BATCH_DIR, f),
    mtime: fs.statSync(path.join(BATCH_DIR, f)).mtimeMs,
  })).sort((a, b) => a.mtime - b.mtime);

  console.log(`  Processing ${filesWithMtime.length} files (sorted by mtime, oldest=Slide 1)\n`);

  let processed = 0;
  for (let i = 0; i < filesWithMtime.length; i++) {
    const file = filesWithMtime[i];
    const targetName = `${prefix}_${i + 1}.png`;
    const targetPath = path.join(BATCH_DIR, targetName);

    // Read the original file with Sharp — this strips ALL metadata
    const inputBuffer = fs.readFileSync(file.fullPath);
    const image = sharp(inputBuffer);
    const metadata = await image.metadata();

    // Convert to clean PNG (strips C2PA, IPTC, EXIF, XMP)
    await image
      .png({ compressionLevel: 6 })
      .toFile(targetPath + '.tmp');

    // Remove original if it's different from target
    if (file.fullPath !== targetPath) {
      fs.unlinkSync(file.fullPath);
    }

    // Rename temp to target
    if (fs.existsSync(targetPath)) fs.unlinkSync(targetPath);
    fs.renameSync(targetPath + '.tmp', targetPath);

    const newSize = fs.statSync(targetPath);
    console.log(`  ✅ ${file.name} → ${targetName} (${metadata.width}x${metadata.height}, ${Math.round(newSize.size / 1024)}KB, metadata stripped)`);
    processed++;
  }

  console.log(`\n  ✅ ${processed} files processed. AI metadata stripped.\n`);
}

// ════════════════════════════════════════════════════════
// PHASE 7: Overlay Text
// ════════════════════════════════════════════════════════
function phase7_overlay() {
  header('7', 'Text Overlays (v2.0)');
  runCmd(`node "${path.join(SCRIPTS_DIR, 'overlay_text.js')}"`);
  
  const overlaidFiles = fs.existsSync(OVERLAID_DIR)
    ? fs.readdirSync(OVERLAID_DIR).filter(f => /\.(png|jpg|jpeg)$/i.test(f))
    : [];
  console.log(`\n  Overlaid images: ${overlaidFiles.length}`);
}

// ════════════════════════════════════════════════════════
// PHASE 7.5a: Compress for Analysis
// ════════════════════════════════════════════════════════
function phase75a_compress() {
  header('7.5a', 'Compress Overlaid Images for Analysis');
  runCmd(`node "${path.join(SCRIPTS_DIR, 'compress_images.js')}" --dir overlaid`);

  const analysisFiles = fs.existsSync(ANALYSIS_DIR)
    ? fs.readdirSync(ANALYSIS_DIR).filter(f => /\.(png|jpg|jpeg)$/i.test(f))
    : [];
  console.log(`\n  Analysis copies: ${analysisFiles.length} in overlaid/analysis/`);
}

// ════════════════════════════════════════════════════════
// PHASE 7.5b: Caption Mismatch Gate (LLM Visual Verification)
// ════════════════════════════════════════════════════════
function phase75b_mismatchGate() {
  header('7.5b', 'Caption Mismatch Gate — LLM Visual Verification');

  const deck = loadDeck();
  const analysisFiles = fs.existsSync(ANALYSIS_DIR)
    ? fs.readdirSync(ANALYSIS_DIR).filter(f => /\.(png|jpg|jpeg)$/i.test(f)).sort()
    : [];

  console.log(`  Expected slides: ${deck.slides.length}`);
  console.log(`  Analysis images: ${analysisFiles.length}`);

  if (analysisFiles.length === 0) {
    console.error('  ❌ No analysis images found! Cannot verify.');
    process.exit(1);
  }

  if (analysisFiles.length !== deck.slides.length) {
    console.error(`  ❌ Count mismatch! ${analysisFiles.length} images but ${deck.slides.length} slides.`);
    console.error('     Fix the source images and re-run from --from-overlay');
    process.exit(1);
  }

  // Print the mapping for the LLM agent to verify visually
  console.log('\n  ┌─────────┬───────────────────────┬──────────────────────────┬────────────────────────┐');
  console.log('  │ Slide # │ Expected Character    │ Analysis Image           │ Expected Text          │');
  console.log('  ├─────────┼───────────────────────┼──────────────────────────┼────────────────────────┤');

  for (let i = 0; i < deck.slides.length; i++) {
    const slide = deck.slides[i];
    const imgFile = analysisFiles[i] || '❌ MISSING';
    const imgPath = path.join(ANALYSIS_DIR, imgFile);
    const char = (slide.character || '').substring(0, 20).padEnd(20);
    const text = (slide.text_overlay?.lines?.[0] || '').substring(0, 20).padEnd(20);
    const num = String(slide.slide_num).padStart(2);

    console.log(`  │   ${num}    │ ${char} │ ${imgFile.padEnd(24)} │ ${text}  │`);
  }
  console.log('  └─────────┴───────────────────────┴──────────────────────────┴────────────────────────┘');

  // Print absolute paths for the LLM to view_file each image
  console.log('\n  📂 VERIFICATION IMAGES (view_file these to visually confirm):');
  for (let i = 0; i < analysisFiles.length; i++) {
    const imgPath = path.join(ANALYSIS_DIR, analysisFiles[i]);
    const slide = deck.slides[i];
    console.log(`     Slide ${slide.slide_num}: ${imgPath}`);
    console.log(`       Expected: ${slide.character} — "${slide.text_overlay?.lines?.join(' | ')}"`)
  }

  // Structural size-delta check (overlay should add data)
  const queue = loadQueue();
  const prefix = (queue.session_id || 'trendtok').replace(/_run$/, '');
  let sizeDeltaPass = 0;

  console.log('\n  📊 Size delta check (overlay adds pixels):');
  for (let i = 0; i < analysisFiles.length; i++) {
    const sourceFile = path.join(BATCH_DIR, `${prefix}_${i + 1}.png`);
    const overlaidFile = path.join(OVERLAID_DIR, analysisFiles[i].replace(/^(trendtok_\d+)/, '$1'));
    
    if (fs.existsSync(sourceFile) && fs.existsSync(overlaidFile)) {
      const srcSize = fs.statSync(sourceFile).size;
      const ovlSize = fs.statSync(overlaidFile).size;
      const delta = ovlSize - srcSize;
      const status = delta > 0 ? '✅' : '⚠️';
      if (delta > 0) sizeDeltaPass++;
      console.log(`     Slide ${i + 1}: ${status} Δ${delta > 0 ? '+' : ''}${Math.round(delta / 1024)}KB`);
    }
  }

  console.log(`\n  Size delta: ${sizeDeltaPass}/${analysisFiles.length} passed`);
  console.log('\n  ⚠️  AGENT: Use view_file on each analysis image above to visually confirm character + text match.');
  console.log('  ⚠️  If all match → proceed. If mismatch → fix source order and re-run --from-overlay.\n');
}

// ════════════════════════════════════════════════════════
// PHASE 8: Generate Metadata
// ════════════════════════════════════════════════════════
function phase8_metadata() {
  header('8', 'Generate TikTok Metadata');

  const deck = loadDeck();
  const metadataPath = path.join(OVERLAID_DIR, 'tiktok_metadata.txt');

  const content = `═══════════════════════════════════════
📱 TIKTOK CAROUSEL METADATA
═══════════════════════════════════════

🎯 TOPIC: ${deck.topic}
🪝 HOOK: ${deck.tiktok_hook}

📝 CAPTION:
${deck.caption}

🏷️ HASHTAGS:
${deck.hashtags}

🎵 SOUND SUGGESTION:
${deck.sound_suggestion}

📊 SLIDES: ${deck.slide_count}
${deck.slides.map(s => `  ${String(s.slide_num).padStart(2)}. [${s.type.toUpperCase()}] ${s.title} — ${s.character}`).join('\n')}

═══════════════════════════════════════
Generated: ${new Date().toISOString()}
═══════════════════════════════════════
`;

  fs.writeFileSync(metadataPath, content.trim(), 'utf-8');
  console.log(`  ✅ Written: ${metadataPath}`);
  console.log(`  📋 Topic: ${deck.topic}`);
  console.log(`  📋 Hook: ${deck.tiktok_hook}`);
  console.log(`  📋 Slides: ${deck.slide_count}\n`);
}

// ════════════════════════════════════════════════════════
// PHASE 9: Upload to Google Drive
// ════════════════════════════════════════════════════════
function phase9_upload() {
  header('9', 'Upload to Google Drive');
  runCmd(`python "${path.join(SCRIPTS_DIR, 'upload_drive.py')}" --clean --include-raw`);
}

// ════════════════════════════════════════════════════════
// MAIN ORCHESTRATOR
// ════════════════════════════════════════════════════════
async function main() {
  const startTime = Date.now();
  console.log('');
  console.log('╔═══════════════════════════════════════════════════════╗');
  console.log('║  TrendTok One-Shot Pipeline — Master Orchestrator    ║');
  console.log('╚═══════════════════════════════════════════════════════╝');
  console.log('');

  if (DRY_RUN) console.log('  🧪 DRY RUN — skipping Flow interaction (Phases 2-5)\n');
  if (FROM_OVERLAY) console.log('  ⏩ Starting from overlay (Phases 7-9)\n');
  if (FROM_UPLOAD) console.log('  ⏩ Starting from upload (Phase 9 only)\n');

  // Validate prereqs
  if (!fs.existsSync(QUEUE_FILE)) {
    console.error('❌ gemgen_queue.json not found. Generate prompts first!');
    process.exit(1);
  }
  if (!fs.existsSync(DECK_FILE)) {
    console.error('❌ carousel_deck.json not found. Generate deck first!');
    process.exit(1);
  }

  let browser, page, projectUrl;
  let vpnStatus = { vpnActive: false };

  try {
    // ── Phase 0 ──
    if (!FROM_OVERLAY && !FROM_UPLOAD) {
      phase0_cleanup();
    }

    // ── Phase 1 ──
    if (!DRY_RUN && !FROM_OVERLAY && !FROM_UPLOAD) {
      vpnStatus = phase1_vpnCheck();
    }

    // ── Phases 2-5 (Flow interaction) ──
    if (!DRY_RUN && !FROM_OVERLAY && !FROM_UPLOAD) {
      console.log('  🔌 Connecting to Chrome CDP...');
      browser = await chromium.connectOverCDP(`http://localhost:${CDP_PORT}`);
      console.log('  ✅ Connected.\n');

      // Phase 2
      const project = await phase2_freshProject(browser);
      page = project.page;
      projectUrl = project.projectUrl;

      // Phase 3
      const { submitted, failed } = await phase3_submitPrompts(page, vpnStatus.vpnActive);

      // Phase 4
      await phase4_waitAndRetry(page, projectUrl, failed);

      // Phase 5
      await phase5_download2K(page, projectUrl);
    }

    // ── Phase 6 ──
    if (!FROM_OVERLAY && !FROM_UPLOAD) {
      await phase6_renameAndStrip();
    }

    // ── Phase 7 ──
    if (!FROM_UPLOAD) {
      phase7_overlay();
    }

    // ── Phase 7.5a ──
    if (!FROM_UPLOAD) {
      phase75a_compress();
    }

    // ── Phase 7.5b ──
    if (!FROM_UPLOAD) {
      phase75b_mismatchGate();
    }

    // ── Phase 8 ──
    if (!FROM_UPLOAD) {
      phase8_metadata();
    }

    // ── Phase 9 ──
    phase9_upload();

    // ── Done ──
    const elapsed = ((Date.now() - startTime) / 1000 / 60).toFixed(1);
    console.log('');
    console.log('╔═══════════════════════════════════════════════════════╗');
    console.log('║  ✅ PIPELINE COMPLETE                                ║');
    console.log('╚═══════════════════════════════════════════════════════╝');
    console.log('');
    console.log(`  ⏱️  Total time: ${elapsed} minutes`);
    console.log(`  📁 Output: ${OVERLAID_DIR}`);
    console.log(`  ☁️  Uploaded to: Google Drive "Tiktok ready" folder`);
    console.log('');

  } catch (err) {
    console.error(`\n❌ PIPELINE FAILED at ${err.message}`);
    console.error(err.stack);
    process.exit(1);
  }
}

main().catch(err => {
  console.error('❌ Fatal error:', err.message);
  console.error(err.stack);
  process.exit(1);
});
