const { chromium } = require('playwright');

async function main() {
    console.log('Connecting to Chrome...');
    const browser = await chromium.connectOverCDP('http://localhost:9222');
    let page = null;
    for (const ctx of browser.contexts()) {
        for (const p of ctx.pages()) {
            if (p.url().includes('flow/project')) {
                page = p;
                break;
            }
        }
    }
    if (!page) {
        console.log('No flow page found');
        process.exit(1);
    }
    
    // Assume detail view is already open (because download_2k.js failed and left it open)
    console.log('Dumping buttons in detail view...');
    const btns = await page.locator('button, a, div[role="button"], span[role="button"]').evaluateAll(es => {
        return es.filter(e => e.innerText || e.getAttribute('aria-label') || e.getAttribute('data-tooltip')).map(e => ({
            text: e.innerText?.trim()?.substring(0,20),
            aria: e.getAttribute('aria-label'),
            dt: e.getAttribute('data-tooltip'),
            cls: e.className
        }));
    });
    console.log(JSON.stringify(btns, null, 2));

    // After dumping, try to close the detail view so grid is visible again
    const closeBtn = await page.locator('button[aria-label="Back to grid view"], button[aria-label*="lose"]').first();
    if (await closeBtn.count() > 0) {
        await closeBtn.click();
    }
    process.exit(0);
}

main();
