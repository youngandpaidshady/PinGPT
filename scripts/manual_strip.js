const sharp = require('sharp');
const fs = require('fs');

async function process() {
  const inPath = 'C:\\Users\\Administrator\\Desktop\\PinGPT\\output\\gemgen_batch\\47792d87-9938-4816-a586-23579e3e619e';
  const outPath = 'C:\\Users\\Administrator\\Desktop\\PinGPT\\output\\gemgen_batch\\jjk_aura_3.png';
  
  if (!fs.existsSync(inPath)) {
    console.error('Missing input file', inPath);
    return;
  }
  
  const image = sharp(fs.readFileSync(inPath));
  const metadata = await image.metadata();
  
  await image.png({ compressionLevel: 6 }).toFile(outPath);
  
  fs.unlinkSync(inPath);
  const newSize = fs.statSync(outPath);
  console.log(`Converted successfully! ${metadata.width}x${metadata.height}, ${Math.round(newSize.size / 1024)}KB`);
}
process();
