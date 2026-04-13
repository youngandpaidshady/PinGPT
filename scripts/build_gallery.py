import os
import json

folder = r"c:\Users\Administrator\Desktop\PinGPT\output\gemgen_batch"
png_files = [f for f in os.listdir(folder) if f.endswith(".png")]

with open(r"c:\Users\Administrator\Desktop\PinGPT\gemgen_queue.json", "r") as f:
    q1 = json.load(f)
with open(r"c:\Users\Administrator\Desktop\PinGPT\gemgen_queue_part2.json", "r") as f:
    q2 = json.load(f)
    
html = """
<html>
<head>
<style>
  body { font-family: Arial; }
  .img-container { display: inline-block; width: 400px; margin: 10px; border: 1px solid #ccc; padding: 10px; vertical-align: top; }
  img { max-width: 100%; height: auto; }
</style>
</head>
<body>
<h1>Image Mapping Gallery</h1>
<p>There are 20 possible characters/prompts. Look at each image below and identify the character based on visual features (e.g., hair, clothing, eyes, scene).</p>

<h2>Prompt/Character List</h2>
<ol>
"""

# add prompts for reference
all_prompts = q1["items"] + q2["items"]
for p in all_prompts:
    html += f"<li><b>{p['character']} ({p['niche']}):</b> {p['prompt']}</li>\n"

html += "</ol>\n<h2>Images to map</h2>\n"

for pf in png_files:
    html += f'<div class="img-container">\n'
    html += f'<h3>Filename: {pf}</h3>\n'
    # Use absolute file URI
    html += f'<img src="file:///{folder.replace(chr(92), "/")}/{pf}" />\n'
    html += f'</div>\n'

html += """
</body>
</html>
"""

with open(r"c:\Users\Administrator\Desktop\PinGPT\mapping_gallery.html", "w", encoding="utf-8") as f:
    f.write(html)
