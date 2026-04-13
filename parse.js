const fs = require('fs');
const path = require('path');

const inputPath = 'C:\\Users\\Administrator\\.gemini\\antigravity\\brain\\b7479f5d-4366-41ae-ab70-8f9a07605b65\\sadboy_prompts_20.md';
const outDir = 'C:\\Users\\Administrator\\.gemini\\antigravity\\brain\\b7479f5d-4366-41ae-ab70-8f9a07605b65\\browser';
const outPath = 'C:\\Users\\Administrator\\.gemini\\antigravity\\brain\\b7479f5d-4366-41ae-ab70-8f9a07605b65\\browser\\prompts.json';

if (!fs.existsSync(outDir)) {
    fs.mkdirSync(outDir, {recursive: true});
}

const text = fs.readFileSync(inputPath, 'utf8');
const blocks = text.split(/## Prompt \d+/).slice(1);
const prompts = [];

for (let block of blocks) {
    const lines = block.split('\n');
    const pLines = [];
    for (let line of lines) {
        if (line.trim().startsWith('>')) {
            pLines.push(line.replace(/^>\s*/, ''));
        }
    }
    const fullPrompt = pLines.join('\n').trim();
    if (fullPrompt.length > 0) {
        prompts.push(fullPrompt);
    }
}

fs.writeFileSync(outPath, JSON.stringify(prompts, null, 2));
