const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
    try {
        console.log('Connecting to browser...');
        const browser = await chromium.connectOverCDP('http://localhost:9222');
        const context = browser.contexts()[0];
        const pages = context.pages();
        
        let p = pages.find(page => page.url().includes('1hGKOtWbET3cmPMZ6zK85-heFQRq9s5k8'));
        
        if (!p) {
            console.log('Opening new tab for Drive');
            p = await context.newPage();
            await p.goto('https://drive.google.com/drive/u/0/folders/1hGKOtWbET3cmPMZ6zK85-heFQRq9s5k8');
            await p.waitForLoadState('networkidle');
        } else {
            console.log('Found existing Drive tab');
            await p.bringToFront();
        }

        const uploadDir = path.join(__dirname, '..', 'output', 'gemgen_batch', 'overlaid');
        
        // Find all overlaid images
        const files = fs.readdirSync(uploadDir)
            .filter(f => /\.(png|jpg)$/i.test(f) && f.startsWith('trendtok_'))
            .map(f => path.join(uploadDir, f));
            
        console.log(`Found ${files.length} images to upload.`);

        // Playwright CDP has a 50MB limit for setFiles. We have ~80MB. Let's chunk them.
        const CHUNK_SIZE = 4;
        const chunks = [];
        for (let i = 0; i < files.length; i += CHUNK_SIZE) {
            chunks.push(files.slice(i, i + CHUNK_SIZE));
        }
        
        console.log(`Splitting into ${chunks.length} chunks due to 50MB Playwright CDP limit...`);
        
        console.log(`Splitting into ${chunks.length} chunks due to 50MB Playwright CDP limit...`);
        
        // Google Drive almost always has a hidden file input available in the document body. 
        // We can just find it and forcibly set its input files.
        const inputLocator = p.locator('input[type="file"]');
        const count = await inputLocator.count();
        console.log(`Found ${count} hidden file inputs. Using the last one (index ${count - 1})...`);
        const targetInput = inputLocator.nth(count - 1);
        
        for (let i = 0; i < chunks.length; i++) {
            const chunk = chunks[i];
            console.log(`Uploading chunk ${i+1}/${chunks.length} (${chunk.length} files)...`);
            
            // Forcibly inject the files into the hidden input
            await targetInput.setInputFiles(chunk, { force: true });
            
            console.log(`Chunk ${i+1} injected! Waiting before next chunk...`);
            await p.waitForTimeout(3000); // Wait for Drive UI to process
        }
        
        console.log('All chunks injected successfully!');
        await browser.disconnect();
    } catch(e) {
        console.error('Error:', e);
    }
})();
