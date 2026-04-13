import os, shutil, json

# Load both parts
with open('gemgen_queue_part1.json', 'r') as f: p1 = json.load(f)['items']
with open('gemgen_queue_part2.json', 'r') as f: p2 = json.load(f)['items']

all_items = {i['id']: i for i in p1 + p2}

mapping = [
    (1, r'C:\Users\Administrator\Downloads\Generate_an_image_202604070539 (1).png'),
    (2, r'C:\Users\Administrator\Downloads\Aki_Hayakawa,_lean_202604070540.png'),
    (4, r'C:\Users\Administrator\Downloads\Generate_an_image_202604070539.png'),
    (5, r'C:\Users\Administrator\Downloads\Eren_Yeager,_lean_202604070538.png'),
    (6, r'C:\Users\Administrator\Downloads\Vertical_9_16_Portrait._202604070538.png'),
    (7, r'C:\Users\Administrator\Downloads\Spike_Spiegel,_tall_202604070538.png'),
    (8, r'C:\Users\Administrator\Downloads\9_16_Cinematic_Still._202604070537.png'),
    (9, r'C:\Users\Administrator\Downloads\Toji_Fushiguro,_muscular_202604070536.png'),
    (14, r'C:\Users\Administrator\Downloads\Generate_an_image_202604070605.png'),
    (18, r'C:\Users\Administrator\Downloads\Generate_an_image_202604070604.png')
]

out_dir = r"C:\Users\Administrator\Desktop\PinGPT\output\gemgen_batch"
os.makedirs(out_dir, exist_ok=True)

# Clean out_dir safely
for filename in os.listdir(out_dir):
    p = os.path.join(out_dir, filename)
    if os.path.isfile(p) and filename.endswith('.png'):
        os.remove(p)

from PIL import Image

final_items = []
prefix = 'handpicked'
for i, (orig_id, img_path) in enumerate(mapping, 1):
    item = all_items[orig_id].copy()
    item['id'] = i
    final_items.append(item)
    
    new_name = f'{prefix}_{i}.png'
    dest_path = os.path.join(out_dir, new_name)
    
    img = Image.open(img_path)
    data = list(img.getdata())
    clean_img = Image.new(img.mode, img.size)
    clean_img.putdata(data)
    clean_img.save(dest_path, format="PNG")
    print(f"Processed: {new_name}")

out_queue = {
    'session_id': 'handpicked_run',
    'items': final_items
}
with open('gemgen_queue.json', 'w') as f:
    json.dump(out_queue, f, indent=2)

print('Success! All 10 images matched and metadata stripped.')
