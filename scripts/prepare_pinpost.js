const fs = require('fs');
const path = require('path');

const QUEUE_FILE = 'C:\\Users\\Administrator\\Desktop\\PinGPT\\gemgen_queue.json';
const OUTPUT_FILE = 'C:\\Users\\Administrator\\Desktop\\PinGPT\\pinpost_instructions.txt';
const BATCH_DIR = 'C:\\Users\\Administrator\\Desktop\\PinGPT\\output\\gemgen_batch';

const data = JSON.parse(fs.readFileSync(QUEUE_FILE, 'utf8'));

let out = `**Task for subagent:**

**For EACH pin (repeat for every image from 1 to 20):**

**A. Navigate to Pin creation:**
1. Go to \`https://www.pinterest.com/pin-creation-tool/\`
2. If not logged in, click "Log in" → select aaronbrian78 account.
3. You should see the Pin creation form with "Drag and drop or click to upload".

**B. Upload the image:**
1. Click the upload area ("Drag and drop or click to upload").
2. A file picker dialog will appear — this is handled by the \`upload_file\` browser tool.
3. Use the upload tool to select the image file from the absolute path provided below.
4. Wait for the image preview to appear in the form.

**C. Fill in metadata:**
1. Click the "Title" field → type the pin title precisely.
2. Click the "Tell everyone what your Pin is about" description field → wait 2s → type the description + hashtags.
3. Click the "Alt text" field (may need to expand "More options") → type the alt text.

**D. Select board:**
1. Click the board selector dropdown (shows "Choose a board" or last used board).
2. Search for the appropriate board. Use "Jujutsu Kaisen Wallpapers" for JJK characters, "Attack on Titan Art" for AOT characters, "Solo Leveling Aesthetic" for Jinwoo, and "Dark Anime Aesthetic" for others.
3. Select the board carefully.

**E. Publish:**
1. Click the strictly REQUIRED "Publish" button.
2. Wait 3-5 seconds for the "Your Pin has been published!" confirmation.
3. DO NOT click "Save to another board", just continue.

**F. Next pin:**
1. Navigate back to \`https://www.pinterest.com/pin-creation-tool/\`.
2. Repeat for the next image.

**Here are the 20 pins to post:**

`;

for (let i = 0; i < data.items.length; i++) {
    const item = data.items[i];
    
    // Assign proper board based on character
    const char = item.character.toLowerCase();
    let board = "Dark Anime Aesthetic";
    if (char.includes('gojo') || char.includes('toji') || char.includes('megumi') || char.includes('yuji') || char.includes('nanami')) board = "Jujutsu Kaisen Wallpapers";
    if (char.includes('levi') || char.includes('eren')) board = "Attack on Titan Art";
    if (char.includes('jinwoo')) board = "Solo Leveling Aesthetic";

    out += `PIN ${i + 1}:
Image: ${path.join(BATCH_DIR, `lasttrain_${i + 1}.png`)}
Title: ${item.title}
Description: ${item.description}
Hashtags: ${item.tags}
Alt text: ${item.alt_text}
Board: ${board}

`;
}

fs.writeFileSync(OUTPUT_FILE, out);
console.log('Instructions written to', OUTPUT_FILE);
