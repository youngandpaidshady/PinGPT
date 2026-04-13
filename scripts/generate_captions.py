import os
import sys
import json
import glob
import base64
import time
import io

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

MODEL = "gemini-3.1-flash-lite-preview"
BATCH_DIR = r"C:\Users\Administrator\Desktop\PinGPT\output\gemgen_batch"
OUTPUT_FILE = os.path.join(BATCH_DIR, "bulkpin_metadata.json")

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
api_keys_str = os.getenv("GEMINI_API_KEYS", os.getenv("GEMINI_API_KEY", ""))
api_keys = [k.strip() for k in api_keys_str.split(",") if k.strip()]
live_keys = list(api_keys)
_key_index = 0

def get_client():
    global _key_index
    if not live_keys:
        raise RuntimeError("All API keys exhausted.")
    _key_index = _key_index % len(live_keys)
    key = live_keys[_key_index]
    _key_index = (_key_index + 1) % len(live_keys)
    return genai.Client(api_key=key), key[-6:], key

def compress_image(image_path):
    img = Image.open(image_path)
    w, h = img.size
    if max(w, h) > 1024:
        ratio = 1024 / max(w, h)
        new_size = (int(w * ratio), int(h * ratio))
        img = img.resize(new_size, Image.LANCZOS)
    if img.mode in ("RGBA", "P"): img = img.convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=80)
    return base64.b64encode(buf.getvalue()).decode("utf-8"), "image/jpeg"

system_instruction = """
You are a Pinterest expert capturing anime aesthetic vibes. 
Analyze the image provided and generate a perfect Pinterest title, description, and hashtags.
RULES:
1. Titles: Unique, lowercase aesthetic ("when toji walks home at 3am"), questions, or quotes. Max 100 characters. NEVER repeat the same structure. NO KANJI.
2. Descriptions: Write organically like texting a friend. Mix sentence lengths. Describe the mood and scene naturally. Max 500 characters. NO KANJI.
3. Tags: 5 broad + 5 character + 5 niche + 3-5 trending hashtags separated by spaces (e.g. "#toji #jujutsukaisen #animeaesthetic"). DO NOT format tags as an array; output a single string separated by spaces.
4. Respond ONLY with a valid JSON object matching this schema exactly:
{
  "title": "string",
  "description": "string",
  "tags": "string",
  "alt_text": "string short description",
  "mood": "string guessed mood (e.g. edgeofbed, rainytokyo)",
  "character": "string predicted character name based on the art"
}
NO MARKDOWN. ONLY valid JSON.
"""

def main():
    images = glob.glob(os.path.join(BATCH_DIR, "*.png"))
    images.sort(key=os.path.getctime)
    final_mapping = {}
    
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            final_mapping = json.load(f)

    for i, image_path in enumerate(images):
        filename = os.path.basename(image_path)
        if filename in final_mapping and "prompt_details" in final_mapping[filename]:
            print(f"Skipping {filename}, already processed.")
            continue
            
        print(f"Processing {filename} [{i+1}/{len(images)}]")
        image_b64, mime_type = compress_image(image_path)
        
        success = False
        for _ in range(len(api_keys)):
            if not live_keys: break
            client, key_suffix, full_key = get_client()
            try:
                response = client.models.generate_content(
                    model=MODEL,
                    contents=[
                        {"role": "user", "parts": [
                            {"inline_data": {"mime_type": mime_type, "data": image_b64}},
                            {"text": "Analyze this anime art and return the JSON object."}
                        ]}
                    ],
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.8,
                    ),
                )
                
                text = response.text.strip()
                if text.startswith("```json"): text = text[7:]
                if text.endswith("```"): text = text[:-3]
                text = text.strip()
                
                data = json.loads(text)
                
                final_mapping[filename] = {
                    "matched_id": i+999,
                    "matched_character": data.get("character", "Unknown") + " - " + data.get("mood", "unknown"),
                    "matched_title": data.get("title", ""),
                    "prompt_details": {
                        "character": data.get("character", "Unknown"),
                        "mood": data.get("mood", "unknown"),
                        "title": data.get("title", ""),
                        "description": data.get("description", ""),
                        "tags": data.get("tags", ""),
                        "alt_text": data.get("alt_text", "")
                    }
                }
                success = True
                print(f"  ✅ {data.get('title')}")
                break
            except Exception as e:
                err = str(e)
                if "PERMISSION_DENIED" in err or "project has been" in err:
                    if full_key in live_keys: live_keys.remove(full_key)
                print(f"  ⚠️ Error: {err[:80]}")
                time.sleep(2)
                
        if not success:
            final_mapping[filename] = {"error": "Failed to generate"}
            
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(final_mapping, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()
