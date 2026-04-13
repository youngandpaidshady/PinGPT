from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import os

batch = r'c:\Users\Administrator\Desktop\PinGPT\output\gemgen_batch'
thumb = os.path.join(batch, 'thumbs')
os.makedirs(thumb, exist_ok=True)

count = 0
for i in range(11, 30):
    src = os.path.join(batch, f'dl_{i}.png')
    dst = os.path.join(thumb, f'dl_{i}.jpg')
    if os.path.exists(dst):
        count += 1
        continue
    if not os.path.exists(src):
        print(f'dl_{i}.png MISSING')
        continue
    try:
        img = Image.open(src)
        w, h = img.size
        ratio = 400 / max(w, h)
        img = img.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)
        img.save(dst, 'JPEG', quality=60)
        sz = os.path.getsize(dst)
        print(f'dl_{i}.jpg  {sz // 1024}KB  ({w}x{h})')
        count += 1
    except Exception as e:
        print(f'dl_{i}.png ERROR: {e}')

existing = len([f for f in os.listdir(thumb) if f.endswith('.jpg')])
print(f'\nDone. {existing} thumbs total')
