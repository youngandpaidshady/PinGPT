#!/usr/bin/env python3
"""
PinGPT — Vision-Based Image-to-Prompt Mapper
Uses Gemini 2.5 Flash to analyze each generated image and match it to
the correct prompt from gemgen_queue.json based on visual content.

Supports key rotation via GEMINI_API_KEYS (comma-separated) env var.
"""

import os
import sys
import json
import glob
import base64
import time
import itertools
import io

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

# ─── Configuration ────────────────────────────────────────────────────────────

MODEL = "gemini-3.1-flash-lite-preview"
BATCH_DIR = r"C:\Users\Administrator\Desktop\PinGPT\output\gemgen_batch"
QUEUE_FILE = r"C:\Users\Administrator\Desktop\PinGPT\gemgen_queue.json"
OUTPUT_FILE = os.path.join(BATCH_DIR, "bulkpin_metadata.json")
MAX_IMAGE_DIM = 1024   # Resize longest side to this before sending
JPEG_QUALITY = 80      # Compression quality for API upload

# ─── Load API Keys (rotation support) ────────────────────────────────────────

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

api_keys_str = os.getenv("GEMINI_API_KEYS", os.getenv("GEMINI_API_KEY", ""))
api_keys = [k.strip() for k in api_keys_str.split(",") if k.strip()]

if not api_keys:
    print("❌ No API keys found. Set GEMINI_API_KEYS or GEMINI_API_KEY in .env")
    sys.exit(1)

print(f"🔑 Loaded {len(api_keys)} API key{'s' if len(api_keys) > 1 else ''}")

# Live key pool — bad keys get removed automatically
live_keys = list(api_keys)
_key_index = 0

def get_client():
    """Get a genai.Client with the next rotated API key from the live pool."""
    global _key_index
    if not live_keys:
        raise RuntimeError("All API keys exhausted (all returned PERMISSION_DENIED)")
    _key_index = _key_index % len(live_keys)
    key = live_keys[_key_index]
    _key_index = (_key_index + 1) % len(live_keys)
    return genai.Client(api_key=key), key[-6:], key

def remove_bad_key(key):
    """Remove a dead key from the live pool."""
    if key in live_keys:
        live_keys.remove(key)
        print(f"   🗑️  Removed dead key ...{key[-6:]} ({len(live_keys)} keys remaining)")

print(f"✅ Model: {MODEL}")

# ─── Image Compression (in-memory only, originals untouched) ──────────────────

def compress_image(image_path):
    """Resize + compress image in-memory for API upload. Returns (b64_string, mime_type).
    Original file is NEVER modified."""
    img = Image.open(image_path)
    
    # Resize so longest side = MAX_IMAGE_DIM
    w, h = img.size
    if max(w, h) > MAX_IMAGE_DIM:
        ratio = MAX_IMAGE_DIM / max(w, h)
        new_size = (int(w * ratio), int(h * ratio))
        img = img.resize(new_size, Image.LANCZOS)
    
    # Convert to RGB (drop alpha) and compress as JPEG
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=JPEG_QUALITY)
    compressed_bytes = buf.getvalue()
    
    original_kb = os.path.getsize(image_path) / 1024
    compressed_kb = len(compressed_bytes) / 1024
    print(f"   📐 {w}x{h} → {img.size[0]}x{img.size[1]} | {original_kb:.0f}KB → {compressed_kb:.0f}KB")
    
    return base64.b64encode(compressed_bytes).decode("utf-8"), "image/jpeg"

# ─── Load Queue & Images ──────────────────────────────────────────────────────

with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
    queue_data = json.load(f)

if isinstance(queue_data, dict) and "items" in queue_data:
    prompts = queue_data["items"]
else:
    prompts = queue_data

images = glob.glob(os.path.join(BATCH_DIR, "*.png"))
images.sort(key=os.path.getctime)

print(f"📦 Found {len(images)} images and {len(prompts)} prompts")

# ─── Build Mood Summary for Matching ──────────────────────────────────────────

prompt_summaries = []
for i, p in enumerate(prompts):
    mood = p.get("mood", "unknown")
    title = p.get("title", "")
    prompt_text = p.get("prompt", "")
    scene_hint = prompt_text[:200] if prompt_text else ""
    prompt_summaries.append(
        f"ID={p.get('id', i+1)} | MOOD={mood} | TITLE={title} | SCENE={scene_hint}"
    )

prompt_reference = "\n".join(prompt_summaries)

# ─── Vision Matching ──────────────────────────────────────────────────────────

def match_image_to_prompt(image_path, prompt_reference, prompts):
    """Send compressed image to Gemini 2.5 Flash and identify matching prompt.
    Rotates API keys on each call and retries on failure."""
    
    filename = os.path.basename(image_path)
    
    # Compress in-memory (original file untouched)
    image_b64, mime_type = compress_image(image_path)
    
    system_instruction = (
        "You are an image analysis expert. You will be shown an anime-style image and a list of prompts. "
        "Each prompt has a unique ID and MOOD. Your job is to determine WHICH prompt was used to generate this image "
        "by analyzing the visual elements: setting, outfit, lighting, pose, time of day, objects, and overall mood.\n\n"
        "RULES:\n"
        "- Respond with ONLY the numeric ID of the matching prompt\n"
        "- Just the number, nothing else\n"
        "- Example response: 7\n"
    )
    
    user_content = (
        f"Which prompt ID generated this image? Match based on setting, outfit, lighting, pose, objects, and mood.\n\n"
        f"AVAILABLE PROMPTS:\n{prompt_reference}\n\n"
        f"Respond with ONLY the matching ID number."
    )
    
    for attempt in range(len(api_keys)):  # Try up to total key count
        if not live_keys:
            break
        client, key_suffix, full_key = get_client()
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=[
                    {
                        "role": "user",
                        "parts": [
                            {"inline_data": {"mime_type": mime_type, "data": image_b64}},
                            {"text": user_content},
                        ]
                    }
                ],
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.1,
                ),
            )
            
            answer = response.text.strip()
            # Extract just the number (handle "ID: 7" or "7." etc.)
            digits = ''.join(c for c in answer if c.isdigit())
            if not digits:
                print(f"   ⚠️  No number in answer: '{answer}' (key ...{key_suffix})")
                continue
            
            matched_id = int(digits)
            
            for p in prompts:
                if p.get("id") == matched_id:
                    print(f"   ✅ ID {matched_id} → {p['mood']} (key ...{key_suffix})")
                    return {
                        "matched_id": matched_id,
                        "matched_character": f"{p.get('character', '')} - {p.get('mood', '')}",
                        "matched_mood": p.get("mood", ""),
                        "matched_title": p.get("title", ""),
                        "prompt_details": p,
                    }
            
            print(f"   ⚠️  ID {matched_id} not found in prompts")
            return {"error": f"Matched ID {matched_id} not found in prompts", "raw_answer": answer}
            
        except Exception as e:
            err = str(e)
            # Auto-remove dead keys (PERMISSION_DENIED / project blocked)
            if "PERMISSION_DENIED" in err or "project has been" in err:
                remove_bad_key(full_key)
                continue  # Immediately retry with next key, no sleep
            
            print(f"   ⚠️  Attempt failed (key ...{key_suffix}): {err[:80]}")
            if live_keys:
                time.sleep(2)
    
    return {"error": f"All attempts failed ({len(api_keys) - len(live_keys)} keys removed)"}


# ─── Run Matching ─────────────────────────────────────────────────────────────

final_mapping = {}
used_ids = set()

for i, image_path in enumerate(images):
    filename = os.path.basename(image_path)
    print(f"\n{'━'*50}")
    print(f"  [{i+1}/{len(images)}] {filename}")
    
    result = match_image_to_prompt(image_path, prompt_reference, prompts)
    final_mapping[filename] = result
    
    if "matched_id" in result:
        mid = result["matched_id"]
        if mid in used_ids:
            print(f"   ⚠️  DUPLICATE: ID {mid} already matched!")
        used_ids.add(mid)
    
    # Rate limit between calls
    if i < len(images) - 1:
        time.sleep(1.5)

# ─── Save Results ─────────────────────────────────────────────────────────────

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(final_mapping, f, indent=4, ensure_ascii=False)

# ─── Summary ──────────────────────────────────────────────────────────────────

success = sum(1 for v in final_mapping.values() if "matched_id" in v)
failed = sum(1 for v in final_mapping.values() if "error" in v)

print(f"\n{'━'*50}")
print(f"📊 Results: {success}/{len(images)} matched, {failed} failed")

all_ids = {p.get("id") for p in prompts}
matched_ids = {v.get("matched_id") for v in final_mapping.values() if "matched_id" in v}
unmatched = all_ids - matched_ids
if unmatched:
    print(f"📋 Unmatched prompt IDs: {sorted(unmatched)}")

print(f"\n💾 Saved → {OUTPUT_FILE}")
