import urllib.request
import re
import os

urls = [
    "https://pin.it/1M4er9A4S",
    "https://pin.it/5dmOptI8V",
    "https://pin.it/7cLnR45rd",
    "https://pin.it/2aH0sfZS7"
]

out_dir = r"C:\Users\Administrator\Desktop\PinGPT\new_mood_pics"
os.makedirs(out_dir, exist_ok=True)

for i, url in enumerate(urls):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        html = response.read().decode('utf-8')
        
        # Look for og:image
        match = re.search(r'<meta property="og:image" content="(.*?)"', html)
        if match:
            img_url = match.group(1)
            print(f"URL: {url} -> Image URL: {img_url}")
            
            # Download image
            img_path = os.path.join(out_dir, f"mood_{i}.jpg")
            urllib.request.urlretrieve(img_url, img_path)
            print(f"Downloaded to {img_path}")
        else:
            print(f"Could not find image for {url}")
            
    except Exception as e:
        print(f"Error for {url}: {e}")
