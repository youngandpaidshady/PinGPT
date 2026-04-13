const { chromium } = require('playwright');
const fs = require('fs');

const QUEUE_FILE = 'C:\\Users\\Administrator\\Desktop\\PinGPT\\gemgen_queue.json';

async function main() {
    const browser = await chromium.connectOverCDP('http://localhost:9222');
    let url = null;
    
    for (const ctx of browser.contexts()) {
        for (const p of ctx.pages()) {
            if (p.url().includes('labs.google/fx/tools/flow/project/')) {
                url = p.url();
                break;
            }
        }
    }
    
    if (url) {
        console.log("Found project URL:", url);
        if (fs.existsSync(QUEUE_FILE)) {
            const data = JSON.parse(fs.readFileSync(QUEUE_FILE, 'utf8'));
            data.flow_project_url = url;
            fs.writeFileSync(QUEUE_FILE, JSON.stringify(data, null, 2));
            console.log("Updated gemgen_queue.json explicitly with current Flow URL.");
        }
    } else {
        console.log("Could not find a project URL.");
    }
    process.exit(0);
}

main();
