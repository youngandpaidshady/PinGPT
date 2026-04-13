#!/usr/bin/env node
/**
 * Download files from a Google Drive folder using Chrome's active session.
 * Connects via CDP and uses page.evaluate() to make authenticated
 * Drive API calls from within the browser, then relays the file data.
 *
 * Usage: node scripts/download_drive.js <folder_id_or_url> [output_dir]
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const CDP_PORT = 9222;

function extractFolderId(input) {
  if (!input) return null;
  const urlMatch = input.match(/folders\/([a-zA-Z0-9_-]+)/);
  if (urlMatch) return urlMatch[1];
  if (/^[a-zA-Z0-9_-]+$/.test(input)) return input;
  return null;
}

async function main() {
  const args = process.argv.slice(2);
  const folderId = extractFolderId(args[0]);
  const outputDir = args[1] || path.resolve(__dirname, '..', 'new_mood_pics');

  if (!folderId) {
    console.error('Usage: node scripts/download_drive.js <folder_id_or_url> [output_dir]');
    process.exit(1);
  }

  fs.mkdirSync(outputDir, { recursive: true });
  console.log(`📁 Folder ID: ${folderId}`);
  console.log(`📂 Output: ${outputDir}\n`);

  console.log(`Connecting to Chrome on CDP port ${CDP_PORT}...`);
  const browser = await chromium.connectOverCDP(`http://localhost:${CDP_PORT}`);
  const contexts = browser.contexts();

  // Find or open a Drive page
  let page = null;
  for (const ctx of contexts) {
    for (const p of ctx.pages()) {
      if (p.url().includes('drive.google.com')) { page = p; break; }
    }
    if (page) break;
  }

  if (!page) {
    console.log('No Drive page found, opening one...');
    page = await contexts[0].newPage();
    await page.goto('https://drive.google.com', { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(3000);
  }
  console.log(`Using page: ${page.url().substring(0, 60)}...\n`);

  // Step 1: List files in the folder via in-page fetch
  console.log('Listing files in folder...');
  const files = await page.evaluate(async (fid) => {
    try {
      const query = encodeURIComponent(`'${fid}' in parents and trashed = false`);
      const url = `https://www.googleapis.com/drive/v3/files?q=${query}&fields=files(id,name,mimeType,size)&pageSize=100&key=AIzaSyC1qbk75LEcW7o4SIrides7bAoAT5iCwgsc`;
      const resp = await fetch(url, { credentials: 'include' });
      if (!resp.ok) {
        const text = await resp.text();
        return { error: `HTTP ${resp.status}: ${text.substring(0, 300)}` };
      }
      return await resp.json();
    } catch (e) {
      return { error: e.message };
    }
  }, folderId);

  if (files.error) {
    console.error(`❌ Could not list files: ${files.error}`);
    // Try without API key
    console.log('\nRetrying without API key...');
    const files2 = await page.evaluate(async (fid) => {
      try {
        const query = encodeURIComponent(`'${fid}' in parents and trashed = false`);
        const url = `https://www.googleapis.com/drive/v3/files?q=${query}&fields=files(id,name,mimeType,size)&pageSize=100`;
        const resp = await fetch(url, { credentials: 'include' });
        if (!resp.ok) {
          const text = await resp.text();
          return { error: `HTTP ${resp.status}: ${text.substring(0, 300)}` };
        }
        return await resp.json();
      } catch (e) {
        return { error: e.message };
      }
    }, folderId);

    if (files2.error) {
      console.error(`❌ Still failed: ${files2.error}`);
      
      // Last resort: use the Drive UI's internal APIs scraped from the page
      console.log('\nTrying to extract file list from Drive page directly...');
      
      // Navigate to the actual folder
      const folderUrl = `https://drive.google.com/drive/folders/${folderId}`;
      if (!page.url().includes(folderId)) {
        await page.goto(folderUrl, { waitUntil: 'networkidle', timeout: 20000 });
        await page.waitForTimeout(3000);
      }
      
      // Extract file info from the rendered page
      const pageFiles = await page.evaluate(() => {
        const items = [];
        // Drive renders files with data-id attributes
        const fileElements = document.querySelectorAll('[data-id]');
        for (const el of fileElements) {
          const id = el.getAttribute('data-id');
          // Skip non-file IDs (short ones are usually UI elements)
          if (id && id.length > 20) {
            // Try to get the filename
            const nameEl = el.querySelector('[data-tooltip]') || el.querySelector('.KL4NAf');
            const name = nameEl ? (nameEl.getAttribute('data-tooltip') || nameEl.textContent || '').trim() : '';
            if (name) items.push({ id, name });
          }
        }
        return items;
      });

      if (pageFiles.length === 0) {
        console.error('❌ Could not find any files. Check folder permissions.');
        await browser.close();
        process.exit(1);
      }

      console.log(`Found ${pageFiles.length} files from page DOM.\n`);

      // Download each file
      let downloaded = 0;
      let failed = 0;

      for (const file of pageFiles) {
        process.stdout.write(`  [${downloaded + failed + 1}/${pageFiles.length}] ${file.name}... `);
        try {
          const base64 = await page.evaluate(async (fileId) => {
            const resp = await fetch(`https://drive.google.com/uc?export=download&id=${fileId}`, {
              credentials: 'include',
              redirect: 'follow'
            });
            if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
            const blob = await resp.blob();
            return new Promise((resolve, reject) => {
              const reader = new FileReader();
              reader.onloadend = () => resolve(reader.result.split(',')[1]);
              reader.onerror = reject;
              reader.readAsDataURL(blob);
            });
          }, file.id);

          const destPath = path.join(outputDir, file.name);
          fs.writeFileSync(destPath, Buffer.from(base64, 'base64'));
          const sizeMB = (fs.statSync(destPath).size / (1024 * 1024)).toFixed(1);
          console.log(`✅ ${sizeMB}MB`);
          downloaded++;
        } catch (err) {
          console.log(`❌ ${err.message.substring(0, 80)}`);
          failed++;
        }
      }

      console.log(`\n========== RESULTS ==========`);
      console.log(`Downloaded: ${downloaded}/${pageFiles.length}`);
      console.log(`Failed: ${failed}`);
      console.log(`Output: ${outputDir}`);
      await browser.close();
      return;
    }

    // Use files2
    Object.assign(files, files2);
  }

  if (!files.files || files.files.length === 0) {
    console.error('❌ No files found in folder.');
    await browser.close();
    process.exit(1);
  }

  console.log(`Found ${files.files.length} files.\n`);

  // Download each file via in-page fetch
  let downloaded = 0;
  let failed = 0;

  for (const file of files.files) {
    const sizeMB = file.size ? (parseInt(file.size) / (1024 * 1024)).toFixed(1) : '?';
    process.stdout.write(`  [${downloaded + failed + 1}/${files.files.length}] ${file.name} (${sizeMB}MB)... `);

    try {
      // Download file content as base64 via page.evaluate
      const base64 = await page.evaluate(async (fileId) => {
        const resp = await fetch(`https://www.googleapis.com/drive/v3/files/${fileId}?alt=media`, {
          credentials: 'include'
        });
        if (!resp.ok) {
          // Try the export/download URL instead
          const resp2 = await fetch(`https://drive.google.com/uc?export=download&id=${fileId}`, {
            credentials: 'include',
            redirect: 'follow'
          });
          if (!resp2.ok) throw new Error(`HTTP ${resp2.status}`);
          const blob2 = await resp2.blob();
          return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onloadend = () => resolve(reader.result.split(',')[1]);
            reader.onerror = reject;
            reader.readAsDataURL(blob2);
          });
        }
        const blob = await resp.blob();
        return new Promise((resolve, reject) => {
          const reader = new FileReader();
          reader.onloadend = () => resolve(reader.result.split(',')[1]);
          reader.onerror = reject;
          reader.readAsDataURL(blob);
        });
      }, file.id);

      const destPath = path.join(outputDir, file.name);
      fs.writeFileSync(destPath, Buffer.from(base64, 'base64'));
      const actualSize = (fs.statSync(destPath).size / (1024 * 1024)).toFixed(1);
      console.log(`✅ ${actualSize}MB saved`);
      downloaded++;
    } catch (err) {
      console.log(`❌ ${err.message.substring(0, 80)}`);
      failed++;
    }
  }

  console.log(`\n========== RESULTS ==========`);
  console.log(`Downloaded: ${downloaded}/${files.files.length}`);
  console.log(`Failed: ${failed}`);
  console.log(`Output: ${outputDir}`);

  await browser.close();
}

main().catch(err => {
  console.error('Fatal error:', err.message);
  process.exit(1);
});
