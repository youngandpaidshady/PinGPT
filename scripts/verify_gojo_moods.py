import os
import json
import base64
import requests
import glob

api_key = "AIzaSyBeY454G8AuxpnK1b1ibcta9M71izVdJC8"

queue_file = r"C:\Users\Administrator\Desktop\PinGPT\gemgen_queue.json"
with open(queue_file, 'r', encoding='utf-8') as f:
    items = json.load(f)

prompt_options = ""
for item in items:
    prompt_options += f"MOOD: {item['mood']}\nDESCRIPTION: {item['prompt']}\n\n"

batch_dir = r"C:\Users\Administrator\Desktop\PinGPT\output\gemgen_batch"
files = glob.glob(os.path.join(batch_dir, "*.png"))

final_mapping = {}

master_prompt = (
    "You are an expert image analyzer. I am providing you with an anime aesthetic image and a list of 20 different mood descriptions. "
    "Please look carefully at the visual elements in the image (is it raining? is he on a train? in a gym? at a cafe? etc) "
    "and tell me WHICH MOOD EXACTLY matches this image. Output ONLY the exact 'MOOD' name (e.g. 'lasttrain', 'quietday', 'ironsilence') and nothing else. "
    f"Here are the options:\n{prompt_options}"
)

print(f"Verifying {len(files)} images via Gemini computer vision...")

for idx, f in enumerate(files):
    filename = os.path.basename(f)
    with open(f, 'rb') as img:
        b64 = base64.b64encode(img.read()).decode('utf-8')
    
    payload = {
        "contents": [{
            "parts": [
                {"text": master_prompt},
                {"inlineData": {"mimeType": "image/png", "data": b64}}
            ]
        }],
        "generationConfig": {"temperature": 0.0}
    }
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={api_key}"
    import time
    while True:
        resp = requests.post(url, json=payload).json()
        if 'error' in resp:
            print(f"API Error, retrying in 15s... ({resp.get('error', {}).get('message', '')})")
            time.sleep(15)
            continue
        break
    
    try:
        ans = resp.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '').strip()
        
        matched_item = None
        # Clean answer from possible quotes
        clean_ans = ans.replace("'", "").replace('"', '').strip()
        for item in items:
            if item['mood'].lower() == clean_ans.lower():
                matched_item = item
                break
                
        # Fallback partial match
        if not matched_item:
            for item in items:
                if item['mood'].lower() in clean_ans.lower():
                    matched_item = item
                    break
        
        if matched_item:
            final_mapping[filename] = {
                "matched_character": f"gojo - {matched_item['mood']}",
                "prompt_details": matched_item
            }
            print(f"[{idx+1:02d}/{len(files)}] {filename} -> {matched_item['mood']}")
        else:
            print(f"[{idx+1:02d}/{len(files)}] {filename} -> ERROR matching AI answer: '{ans}'")
            final_mapping[filename] = {
                "error": f"Failed to match AI answer: {ans}"
            }
    except Exception as e:
        print(f"[{idx+1:02d}/{len(files)}] {filename} -> API Error {e}")
        final_mapping[filename] = {"error": f"API Error {e}"}

out_path = os.path.join(batch_dir, "bulkpin_metadata.json")
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(final_mapping, f, indent=4, ensure_ascii=False)

print("Verification complete and bulkpin_metadata.json updated!")
