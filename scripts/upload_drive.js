#!/usr/bin/env node
/**
 * Upload files to Google Drive "Tiktok ready" folder.
 * Extracts OAuth access token from Chrome's active session via CDP,
 * then uses Google Drive REST API to upload files directly.
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const https = require('https');

const CDP_PORT = 9222;
const FOLDER_ID = '1hGKOtWbET3cmPMZ6zK85-heFQRq9s5k8'; // "Tiktok ready" folder
const OVERLAID_DIR = path.resolve(__dirname, '..', 'output', 'gemgen_batch', 'overlaid');

async function getAccessToken(browser) {
  const contexts = browser.contexts();
  let page = null;
  
  // Find or open a Google page
  for (const ctx of contexts) {
    for (const p of ctx.pages()) {
      if (p.url().includes('google.com')) {
        page = p;
        break;
      }
    }
    if (page) break;
  }
  
  if (!page) {
    page = await contexts[0].newPage();
    await page.goto('https://drive.google.com', { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(3000);
  }

  // Navigate to the OAuth token endpoint
  // Google's internal token endpoint returns a valid access token for the logged-in user
  const tokenPage = await contexts[0].newPage();
  await tokenPage.goto('https://accounts.google.com/o/oauth2/auth?' + 
    'client_id=65746573420-jcjmpgep677t35h8n03nl0hhk7t60hk3.apps.googleusercontent.com' +
    '&redirect_uri=https://www.googleapis.com/auth/callback' +
    '&scope=https://www.googleapis.com/auth/drive.file' +
    '&response_type=token' +
    '&prompt=none', { timeout: 15000 }).catch(() => {});
  
  await tokenPage.waitForTimeout(3000);
  
  // Try to extract token from URL fragment
  const url = tokenPage.url();
  const hashMatch = url.match(/access_token=([^&]+)/);
  if (hashMatch) {
    await tokenPage.close();
    return hashMatch[1];
  }

  // Fallback: Use the Drive API through the browser's cookies
  // Extract a token by making XHR request from Drive page
  const token = await page.evaluate(async () => {
    try {
      const resp = await fetch('https://www.googleapis.com/drive/v3/about?fields=user', {
        credentials: 'include'
      });
      // If this works, we have cookie-based auth
      if (resp.ok) return '__cookie_auth__';
    } catch (e) {}
    return null;
  });

  await tokenPage.close().catch(() => {});
  return token;
}

function uploadFile(filePath, accessToken) {
  return new Promise((resolve, reject) => {
    const fileName = path.basename(filePath);
    const fileSize = fs.statSync(filePath).size;
    
    // Step 1: Create file metadata
    const metadata = JSON.stringify({
      name: fileName,
      parents: [FOLDER_ID]
    });
    
    const boundary = '-------314159265358979323846';
    const delimiter = `\r\n--${boundary}\r\n`;
    const closeDelimiter = `\r\n--${boundary}--`;
    
    const fileData = fs.readFileSync(filePath);
    
    const multipartBody = Buffer.concat([
      Buffer.from(delimiter),
      Buffer.from('Content-Type: application/json; charset=UTF-8\r\n\r\n'),
      Buffer.from(metadata),
      Buffer.from(delimiter),
      Buffer.from('Content-Type: image/png\r\n\r\n'),
      fileData,
      Buffer.from(closeDelimiter)
    ]);
    
    const options = {
      hostname: 'www.googleapis.com',
      path: '/upload/drive/v3/files?uploadType=multipart',
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': `multipart/related; boundary=${boundary}`,
        'Content-Length': multipartBody.length
      }
    };
    
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode === 200 || res.statusCode === 201) {
          const result = JSON.parse(data);
          resolve(result);
        } else {
          reject(new Error(`HTTP ${res.statusCode}: ${data.substring(0, 200)}`));
        }
      });
    });
    
    req.on('error', reject);
    req.write(multipartBody);
    req.end();
  });
}

async function uploadViaBrowser(browser, filePath) {
  // Alternative: use browser's authenticated session to upload via fetch
  const contexts = browser.contexts();
  let page = null;
  
  for (const ctx of contexts) {
    for (const p of ctx.pages()) {
      if (p.url().includes('drive.google.com')) {
        page = p;
        break;
      }
    }
    if (page) break;
  }
  
  if (!page) {
    page = await contexts[0].newPage();
    await page.goto('https://drive.google.com', { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(3000);
  }

  const fileName = path.basename(filePath);
  const fileData = fs.readFileSync(filePath);
  const base64Data = fileData.toString('base64');
  
  const result = await page.evaluate(async ({ fileName, base64Data, folderId }) => {
    try {
      // Convert base64 back to binary
      const binaryStr = atob(base64Data);
      const bytes = new Uint8Array(binaryStr.length);
      for (let i = 0; i < binaryStr.length; i++) {
        bytes[i] = binaryStr.charCodeAt(i);
      }
      const blob = new Blob([bytes], { type: 'image/png' });
      
      const metadata = {
        name: fileName,
        parents: [folderId]
      };
      
      const formData = new FormData();
      formData.append('metadata', new Blob([JSON.stringify(metadata)], { type: 'application/json' }));
      formData.append('file', blob);
      
      const resp = await fetch('https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart', {
        method: 'POST',
        body: formData
      });
      
      if (resp.ok) {
        const data = await resp.json();
        return { success: true, id: data.id, name: data.name };
      } else {
        const text = await resp.text();
        return { success: false, error: `HTTP ${resp.status}: ${text.substring(0, 200)}` };
      }
    } catch (err) {
      return { success: false, error: err.message };
    }
  }, { fileName, base64Data, folderId: FOLDER_ID });
  
  return result;
}

async function main() {
  const files = fs.readdirSync(OVERLAID_DIR)
    .filter(f => /\.(png|jpg|jpeg)$/i.test(f))
    .sort()
    .map(f => path.join(OVERLAID_DIR, f));

  if (files.length === 0) {
    console.error('❌ No images found.');
    process.exit(1);
  }

  console.log(`Found ${files.length} images to upload.\n`);

  console.log(`Connecting to Chrome on CDP port ${CDP_PORT}...`);
  const browser = await chromium.connectOverCDP(`http://localhost:${CDP_PORT}`);
  
  // Try OAuth token approach first
  console.log('Extracting access token...');
  const token = await getAccessToken(browser);
  
  let uploaded = 0;
  let failed = 0;

  if (token && token !== '__cookie_auth__') {
    console.log('Got OAuth token. Using direct API upload.\n');
    
    for (const file of files) {
      const basename = path.basename(file);
      const sizeMB = (fs.statSync(file).size / (1024 * 1024)).toFixed(1);
      process.stdout.write(`  [${uploaded + failed + 1}/${files.length}] ${basename} (${sizeMB}MB)... `);
      
      try {
        const result = await uploadFile(file, token);
        console.log(`✅ (id: ${result.id})`);
        uploaded++;
      } catch (err) {
        console.log(`❌ ${err.message.substring(0, 80)}`);
        failed++;
      }
    }
  } else {
    console.log('No direct token. Using browser-authenticated upload.\n');
    
    for (const file of files) {
      const basename = path.basename(file);
      const sizeMB = (fs.statSync(file).size / (1024 * 1024)).toFixed(1);
      process.stdout.write(`  [${uploaded + failed + 1}/${files.length}] ${basename} (${sizeMB}MB)... `);
      
      try {
        const result = await uploadViaBrowser(browser, file);
        if (result.success) {
          console.log(`✅ (id: ${result.id})`);
          uploaded++;
        } else {
          console.log(`❌ ${result.error}`);
          failed++;
        }
      } catch (err) {
        console.log(`❌ ${err.message.substring(0, 80)}`);
        failed++;
      }
    }
  }

  console.log(`\n========== RESULTS ==========`);
  console.log(`Uploaded: ${uploaded}/${files.length}`);
  console.log(`Failed: ${failed}`);
}

main().catch(err => {
  console.error('Fatal error:', err.message);
  process.exit(1);
});
