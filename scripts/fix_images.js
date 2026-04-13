const fs = require('fs');
const path = require('path');

const RAW_DIR = path.join(__dirname, 'output', 'gemgen_batch');
const OVERLAID_DIR = path.join(__dirname, 'output', 'gemgen_batch', 'overlaid');

function main() {
  if (fs.existsSync(OVERLAID_DIR)) {
    fs.rmSync(OVERLAID_DIR, { recursive: true, force: true });
  }
  fs.mkdirSync(OVERLAID_DIR, { recursive: true });
  
  const files = fs.readdirSync(RAW_DIR)
    .filter(f => f.toLowerCase().endsWith('.png') && !fs.statSync(path.join(RAW_DIR, f)).isDirectory())
    .map(f => ({ name: f, time: fs.statSync(path.join(RAW_DIR, f)).mtime.getTime() }))
    .sort((a, b) => b.time - a.time); // DESCENDING ORDER (Newest to Oldest) -> Exact match to Slide 1..9

  console.log('Mapping images to slides:');
  for (let i = 0; i < files.length; i++) {
    const rawName = files[i].name;
    const newName = `trendtok_${String(i + 1).padStart(2, '0')}.png`;
    console.log(`Copying ${rawName} -> ${newName}`);
    fs.copyFileSync(path.join(RAW_DIR, rawName), path.join(OVERLAID_DIR, newName));
  }
}

main();
