import os
import base64
import requests

api_key = "AIzaSyBeY454G8AuxpnK1b1ibcta9M71izVdJC8"
directory = r"C:\Users\Administrator\Downloads\New"

files = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]

prompt = """
Examine these 15 images.
Analyze the artistic mood, setting, lighting, and aesthetic vibe of these images collectively. 
We are creating new anime Pinterest prompt workflows based on this dataset. 
Group them into 1-3 distinct 'moods' (e.g. lofi, solitude, melancholic). 
For each mood, describe the specific lighting (e.g. golden hour, moonlight), typical setting, colors, and clothing style seen in the images.
Be detailed but concise.
"""

payload_parts = [{"text": prompt}]

for f in files:
    path = os.path.join(directory, f)
    with open(path, 'rb') as img:
        b64 = base64.b64encode(img.read()).decode('utf-8')
        payload_parts.append({
            "inlineData": {"mimeType": "image/jpeg", "data": b64}
        })

print(f"Sending {len(files)} images in one request...")

payload = {
    "contents": [{"parts": payload_parts}],
    "generationConfig": {"temperature": 0.0}
}
        
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"

try:
    resp = requests.post(url, json=payload).json()
    if 'candidates' in resp:
        ans = resp['candidates'][0]['content']['parts'][0]['text'].strip()
        with open('mood_analysis_results.txt', 'w', encoding='utf-8') as out:
            out.write("=== BATCH ANALYSIS ===\n" + ans + "\n")
        print("Success!")
    else:
        print("API Error:", resp)
except Exception as e:
    print("Error:", e)
