const fs = require('fs');
const prompts = JSON.parse(fs.readFileSync('C:/Users/Administrator/.gemini/antigravity/brain/b7479f5d-4366-41ae-ab70-8f9a07605b65/browser/prompts.json', 'utf8'));
let html = '<html><body><h1>Prompts</h1>';
prompts.forEach((p, i) => {
    html += `<div><textarea id="p${i}" style="width:100%;height:100px;">${p}</textarea><button id="btn${i}" onclick="document.getElementById('p${i}').select(); document.execCommand('copy');">Copy ${i}</button></div><br/>`;
});
html += '</body></html>';
fs.writeFileSync('C:/Users/Administrator/Desktop/PinGPT/prompts.html', html);
