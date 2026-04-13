import re
import json
import sqlite3

md_file = r'C:\Users\Administrator\Desktop\PinGPT\ranpin_gojo_20\ranpin_gojo_batch.md'
out_json = r'C:\Users\Administrator\Desktop\PinGPT\gemgen_queue.json'

with open(md_file, 'r', encoding='utf-8') as f:
    text = f.read()

# Extract from Markdown
# Assuming format like:
# ## PROMPT 01 · `lasttrain`
blocks = re.split(r'## PROMPT \d+ · `([^`]+)`', text)[1:]
items = []

for i in range(0, len(blocks), 2):
    mood = blocks[i]
    block_text = blocks[i+1]
    
    match_title = re.search(r'\*\*Title:\*\*\s*(.+)', block_text)
    match_desc = re.search(r'\*\*Description:\*\*\s*(.+)', block_text)
    match_tags = re.search(r'\*\*Tags:\*\*\s*(.+)', block_text)
    match_prompt = re.search(r'\*\*Prompt:\*\*\n(.*?)(?=\n\n\*\*)', block_text, re.DOTALL)
    
    if not match_prompt:
        match_prompt_fallback = re.search(r'\*\*Prompt:\*\*\n(.*?)\n\n', block_text, re.DOTALL)
        prompt_text = match_prompt_fallback.group(1).strip() if match_prompt_fallback else ""
    else:
        prompt_text = match_prompt.group(1).strip()
        
    tags = match_tags.group(1).strip().replace("`", "") if match_tags else ""
    
    item = {
        "id": (i//2) + 1,
        "mood": mood,
        "character": "gojo",
        "title": match_title.group(1).strip() if match_title else "",
        "description": match_desc.group(1).strip() if match_desc else "",
        "tags": tags,
        "prompt": prompt_text,
        "board": "Anime Boys Aesthetic ✨"
    }
    items.append(item)

with open(out_json, 'w', encoding='utf-8') as f:
    json.dump(items, f, indent=2, ensure_ascii=False)

print(f"Generated {len(items)} items in {out_json}")
