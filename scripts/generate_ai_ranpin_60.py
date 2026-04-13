import os
import sys
import json
import random
import glob
import time
import concurrent.futures
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
api_keys_str = os.getenv("GEMINI_API_KEYS", os.getenv("GEMINI_API_KEY", ""))
live_keys = [k.strip() for k in api_keys_str.split(",") if k.strip()]

_key_idx = 0
def get_client():
    global _key_idx, live_keys
    if not live_keys: return None, None
    key = live_keys[_key_idx % len(live_keys)]
    _key_idx += 1
    return genai.Client(api_key=key), key

CHARACTERS = [{"name": "Toji Fushiguro", "look": "muscular man with messy black hair, heavily-scarred lip, sharp jawline, heavy-lidded green eyes"}, {"name": "Satoru Gojo", "look": "tall lean man with spiky white hair, bright blue eyes, white cloth blindfold wrapped around eyes, charismatic smirk"}, {"name": "Eren Yeager", "look": "lean muscular man with long dark hair in loose man bun, intense gray-green eyes"}, {"name": "Levi Ackerman", "look": "short but muscular man with sharp military undercut"}, {"name": "Baki Hanma", "look": "extremely muscular young man with wild reddish-brown hair, battle scars"}, {"name": "Nanami Kento", "look": "broad-shouldered man with neat slicked-back blond hair, tired amber eyes behind glasses"}, {"name": "Denji", "look": "lean wiry build, messy dirty-blonde hair, shark-toothed grin"}, {"name": "Aki Hayakawa", "look": "lean man with dark hair pulled into a high samurai-style topknot"}, {"name": "Guts", "look": "massive muscular man with wild black hair, missing left eye, prosthetic iron left arm, facial scar"}, {"name": "Ryomen Sukuna", "look": "tall with pink spiky hair, four eyes (two upper slitted), black tribal tattoo lines"}, {"name": "Choso", "look": "lean man with long dark hair in twin tails, dark blood-line markings across nose bridge"}, {"name": "Yuta Okkotsu", "look": "lean young man with messy dark hair, dark circles under eyes, tired haunted eyes"}, {"name": "Yuji Itadori", "look": "athletic young man with pink undercut hair, dark roots, facial markings on cheeks"}, {"name": "Aqua Hoshino", "look": "handsome young man with dark hair, one star-shaped eye, guarded expression"}, {"name": "Rin Itoshi", "look": "lean striker with messy dark teal hair, cold ice-blue eyes"}, {"name": "Nagi Seishiro", "look": "tall with messy white-grey hair, half-lidded bored eyes"}, {"name": "Isagi Yoichi", "look": "athletic young man with dark blue blue hair, sharp determined eyes"}, {"name": "Megumi Fushiguro", "look": "young man with dark spiky hair, deep blue-green eyes, stoic expression"}, {"name": "Shoto Todoroki", "look": "half-white half-red split hair, heterochromatic eyes, burn scar over left eye"}, {"name": "Loid Forger", "look": "handsome blond man, sharp symmetrical features, calculating eyes"}, {"name": "Killua Zoldyck", "look": "young boy with spiky silver-white hair, sharp blue cat-like eyes"}, {"name": "Sung Jinwoo", "look": "tall man with jet-black hair, glowing purple eyes, sharp angular features"}]

# Load only AI generated moods from registry
base_dir = os.path.join(os.path.dirname(__file__), "..")
registry_path = os.path.join(base_dir, "mood_registry.json")

ai_moods = []
if os.path.exists(registry_path):
    with open(registry_path, "r", encoding="utf-8") as f:
        registry = json.load(f)
        for data in registry.get("moods", []):
            if type(data) is dict and data.get("source") == "moodmind":
                slug = data.get("slug")
                wf_path = os.path.join(base_dir, "_agents", "workflows", f"{slug}.md")
                if os.path.exists(wf_path):
                    with open(wf_path, "r", encoding="utf-8") as wf:
                        content = wf.read()
                        if "DNA" in content or "Environment" in content or "Pose" in content: 
                            ai_moods.append({"name": slug, "content": content[:1500]})

if not ai_moods: 
    print("Warning: No AI moods found.")
    sys.exit(1)

out_file = os.path.join(base_dir, "gemgen_queue.json")

def gen_prompt(item):
    global live_keys
    idx, char, mood = item
    sys_inst = f"""Generate PinGPT prompt for {char["name"]} in {mood["name"]}.
    1. Look: "{char["look"]}".
    2. Outfit: Fitted aesthetic. No bare chests.
    3. Pose: One arm described explicitly (ONE-ARM RULE). Character must be physically interacting with environment (leaning, holding, crouching) — NOT just standing.
    4. Scene: The character is IMMERSED in the environment — rain hits them, neon paints them, snow melts on them. They LIVE in the scene, not layered on top.
    5. Lighting: TWO competing light sources with different color temperatures. Never single-source flat lighting.
    6. MUST END with exactly: "2D anime cel-shaded character with clean black outlines, immersed in [environment 3-5 words]. Cinematic depth-of-field. Grainy film texture. No text, no watermarks, clean image."
    JSON OUT: {{"id": {idx}, "character": "{char["name"]}", "mood": "{mood["name"]}", "prompt": "...", "title": "...", "description": "...", "tags": "#aesthetic...", "alt_text": "..."}}
    """
    for _ in range(5):
        client, key = get_client()
        if not client: return None
        try:
            res = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=[{"role": "user", "parts": [{"text": "Format pure JSON. Return Dict."}]}],
                config=types.GenerateContentConfig(system_instruction=sys_inst, temperature=0.8)
            )
            t = res.text.strip()
            if t.startswith("```json"): t = t[7:]
            if t.endswith("```"): t = t[:-3]
            obj = json.loads(t.strip())
            if isinstance(obj, dict): return obj
        except Exception as e:
            if "PERMISSION_DENIED" in str(e) or "project has been" in str(e) or "403" in str(e):
                if key in live_keys: live_keys.remove(key)
            time.sleep(2)
    return None

def main():
    items = []
    # Generate 60 prompts
    for i in range(1, 61): 
        items.append((i, random.choice(CHARACTERS), random.choice(ai_moods)))
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
        for idx, res in enumerate(ex.map(gen_prompt, items)):
            if res and isinstance(res, dict): 
                results.append(res)
                print(f"Generated {len(results)}/60")
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2)
    print(f"\\nFinished generating {len(results)} prompts in gemgen_queue.json")

if __name__ == "__main__":
    main()
