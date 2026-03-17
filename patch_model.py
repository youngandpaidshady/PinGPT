"""
Patch script to add /model command to webhook.py
Inserts: MODEL_REGISTRY, RACE_PRESETS, generate_model_dna(), build_model_prompt(), cmd_model()
"""
import re

filepath = r'c:\Users\Administrator\Desktop\PinGPT\api\webhook.py'
content = open(filepath, 'r', encoding='utf-8').read()

# ── 1. Add MODEL_REGISTRY after PHOTO_CACHE_TTL ──
model_registry_code = '''
# ─── Model DNA Registry ──────────────────────────────────────────────────────
# Stores generated fictional model DNA profiles
# Key: "{chat_id}_{hash}" → value: {"name": str, "hash": str, "race": str, "gender": str, "dna": str, "created": float}
import hashlib
MODEL_REGISTRY = {}

RACE_PRESETS = {
    "west_african": ("West African", "🌍", "deep brown skin with warm golden/copper undertone, broad nose with low flat bridge, full lips, coily 4C hair texture, prominent cheekbones"),
    "east_african": ("East African", "🌍", "medium-dark brown skin with warm red undertone, narrower nose with higher bridge, angular face, coily 4A-4B hair texture, high cheekbones"),
    "south_african": ("South African", "🌍", "brown skin with warm amber undertone, broad features, full lips, round face shape, coily 4B-4C hair texture"),
    "south_asian": ("South Asian", "🌏", "warm brown skin with golden undertone, dark expressive eyes, straight to wavy black hair, medium nose bridge, full eyebrows"),
    "east_asian": ("East Asian", "🌏", "light to medium skin with yellow-neutral undertone, monolid or single-fold eyes, straight black hair, low nose bridge, small mouth"),
    "southeast_asian": ("Southeast Asian", "🌏", "warm tan to brown skin, wide-set eyes with double fold, straight to wavy dark hair, flat nose bridge, full lips"),
    "northern_european": ("Northern European", "🌎", "fair skin with cool pink undertone, narrow nose with high bridge, thin lips, straight fine hair, light eyes"),
    "mediterranean": ("Mediterranean", "🌎", "olive skin with warm golden undertone, dark eyes, dark wavy hair, prominent nose, thick eyebrows, strong jaw"),
    "eastern_european": ("Eastern European", "🌎", "fair to light skin with neutral undertone, high cheekbones, straight to wavy hair, deep-set eyes, angular features"),
    "latin_american": ("Latin American", "🌎", "warm tan to medium brown skin, dark eyes, dark straight to wavy hair, medium build nose, full lips, round face"),
    "middle_eastern": ("Middle Eastern", "🌍", "olive to tan skin with warm undertone, dark almond eyes, thick dark eyebrows, prominent hooked or straight nose, dark wavy hair"),
    "indigenous": ("Indigenous", "🌍", "tan to deep brown skin, high cheekbones, straight thick black hair, epicanthic eye folds, broad flat nose, round face"),
    "mixed": ("Mixed Heritage", "🌐", "unique blended features, skin tone varies, distinctive feature combinations that transcend single ethnic classification"),
}

GENDER_OPTIONS = {
    "male": "male",
    "female": "female",
    "m": "male",
    "f": "female",
    "man": "male",
    "woman": "female",
}
'''

content = content.replace(
    'PHOTO_CACHE_TTL = 300  # 5 minutes',
    'PHOTO_CACHE_TTL = 300  # 5 minutes' + model_registry_code
)

# ── 2. Add model functions before generate_custom_dna_response ──
model_functions = '''

def generate_model_hash(name, chat_id):
    """Generate a short unique hash for a model."""
    raw = f"{chat_id}_{name}_{time.time()}"
    return hashlib.md5(raw.encode()).hexdigest()[:6]


def generate_model_dna(api_keys, race_key, gender, name):
    """Use Gemini to generate an atomic-level DNA profile for a fictional model."""
    from google import genai

    race_name, _, race_baseline = RACE_PRESETS.get(race_key, RACE_PRESETS["mixed"])
    gender_str = GENDER_OPTIONS.get(gender.lower(), "male")

    instruction = (
        f"You are a forensic character designer. Create an EXTREMELY detailed, hyper-specific DNA profile "
        f"for a FICTIONAL {gender_str} character named '{name}' of {race_name} descent.\\n\\n"
        f"BASELINE ETHNIC FEATURES (starting point only — randomize unique variations):\\n"
        f"{race_baseline}\\n\\n"
        f"Generate a SINGLE DENSE PARAGRAPH that describes this UNIQUE person in extreme detail. "
        f"This paragraph will be used as a text-to-image prompt anchor. The same paragraph must produce "
        f"the SAME recognizable person every time it's used.\\n\\n"
        f"INCLUDE ALL OF THESE (do NOT skip any):\\n"
        f"1. FACE: exact shape (oblong, oval, round, square, heart, diamond), width, length, asymmetries\\n"
        f"2. FOREHEAD: height, width, curvature, any creases or veins\\n"
        f"3. EYES: shape per eye, exact color (with flecks/rings), spacing, depth, lids (mono/double), "
        f"canthal tilt, under-eye features (dark circles, bags, puffiness), lash length per eye\\n"
        f"4. EYEBROWS: shape, thickness gradient (thicker at head?), arch position, gap, hair direction\\n"
        f"5. NOSE: bridge width + height, tip shape + angle, nostril shape + flare, septum visibility, "
        f"any bump or deviation, pore visibility on nose\\n"
        f"6. LIPS: upper/lower thickness ratio (e.g., 1:1.8), Cupid's bow shape, corner direction, "
        f"exact pigmentation (darker edges? lighter center?), philtrum depth\\n"
        f"7. JAWLINE: definition level, mandible angle, chin shape + projection, any cleft\\n"
        f"8. CHEEKS: bone prominence, fullness, dimples (one side? both?), hollowness\\n"
        f"9. EARS: size, lobe type (attached/detached), any protrusion\\n"
        f"10. SKIN (CRITICAL — most detail here):\\n"
        f"    - Exact Fitzpatrick shade + undertone with description\\n"
        f"    - Texture zone map: forehead, nose, cheeks, chin (smooth, rough, porous)\\n"
        f"    - Oil/shine zones vs matte zones\\n"
        f"    - SPECIFIC blemishes with POSITIONS: acne marks, PIH spots, dark spots, moles "
        f"(count + locations like 'small mole 1cm below left eye')\\n"
        f"    - Scars (type + location + size)\\n"
        f"    - Under-eye darkness (color: purple, blue, brown), wrinkle lines\\n"
        f"    - Age indicators: laugh lines, forehead creases, crow's feet\\n"
        f"11. HAIR: exact shade, texture type (1A-4C), curl pattern, length in inches, current style, "
        f"hairline shape, density, any grey/white\\n"
        f"12. FACIAL HAIR: type, coverage map (patchy where?), density, color match, ingrown hairs\\n"
        f"13. NECK: thickness, length, Adam's apple, skin tone match\\n"
        f"14. BUILD: body type with specifics — shoulder width, arm size, chest/waist ratio\\n"
        f"15. DISTINGUISHING FEATURES: 2-3 things that make this person INSTANTLY recognizable "
        f"(e.g., 'scar above right eyebrow', 'gap between front teeth', 'beauty mark on left jaw')\\n\\n"
        f"RULES:\\n"
        f"- Make them look REAL and SPECIFIC, not generic AI-beautiful\\n"
        f"- Include IMPERFECTIONS — asymmetry, marks, texture, bags, patchiness\\n"
        f"- The description must be UNIQUE to this one fictional person\\n"
        f"- Output a SINGLE PARAGRAPH, no line breaks, no labels, no bullet points\\n"
        f"- Start with age bracket and gender, then flow through all features\\n"
        f"- End with the 2-3 distinguishing features\\n"
        f"- Aim for 300-400 words of pure dense description"
    )

    shuffled = list(api_keys)
    random.shuffle(shuffled)
    last_error = None
    for key in shuffled:
        try:
            client = genai.Client(api_key=key)
            r = client.models.generate_content(
                model=PROMPT_MODEL,
                contents=[{"role": "user", "parts": [{"text": instruction}]}],
            )
            dna = r.text.strip()
            # Clean any markdown formatting
            dna = dna.replace("```", "").replace("> ", "").strip()
            if dna.startswith('"') and dna.endswith('"'):
                dna = dna[1:-1]
            return dna
        except Exception as e:
            last_error = e
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                continue
            raise
    raise last_error or Exception("All API keys exhausted")


def build_model_prompt(model_dna, user_request):
    """Build image prompt using stored model DNA + user's request."""
    return (
        f"{model_dna}\\n\\n"
        f"--- SCENE ---\\n"
        f"{user_request}\\n\\n"
        f"CRITICAL CONSISTENCY RULES:\\n"
        f"- Every facial feature, skin mark, blemish, mole, scar described above is IMMUTABLE\\n"
        f"- Skin tone and texture must match exactly as described\\n"
        f"- Hair texture and facial hair pattern never change\\n"
        f"- All distinguishing features must be visible and accurate\\n"
        f"- Only the SCENE changes (pose, outfit, setting, lighting) — the person stays identical\\n"
        f"- Photorealistic, real skin texture with pores and imperfections\\n"
        f"- 9:16 portrait, high resolution, no watermark, no text overlay, no AI smoothing"
    )


def cmd_model(token, cid, args, api_keys):
    """Handle /model create|use|list|delete commands."""
    parts = args.strip().split(None, 2) if args else []

    if not parts:
        tg_send(token, cid, (
            "\\U0001f9ec <b>PinGPT Model Lab</b>\\n"
            "\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\n\\n"
            "<b>Create a model:</b>\\n"
            "<code>/model create Aisha west_african female</code>\\n"
            "<code>/model create Kenji east_asian male</code>\\n\\n"
            "<b>Use a model:</b>\\n"
            "<code>/model use #a7f2 smiling in gym</code>\\n"
            "<code>/model use Aisha LinkedIn headshot in blazer</code>\\n\\n"
            "<b>List your models:</b>\\n"
            "<code>/model list</code>\\n\\n"
            "<b>Delete a model:</b>\\n"
            "<code>/model delete #a7f2</code>\\n\\n"
            "<b>Available races:</b>\\n"
            + "\\n".join(f"  {v[1]} <code>{k}</code> \\u2014 {v[0]}" for k, v in RACE_PRESETS.items())
        ))
        return

    action = parts[0].lower()

    # ── CREATE ──
    if action == "create":
        if len(parts) < 3:
            tg_send(token, cid, "\\u26a0\\ufe0f Usage: <code>/model create Name race gender</code>\\nExample: <code>/model create Aisha west_african female</code>")
            return

        rest = parts[1:]
        # Parse: name race [gender]
        name = rest[0]
        race_gender = rest[1].split() if len(rest) > 1 else []
        race = race_gender[0].lower() if race_gender else "mixed"
        gender = race_gender[1].lower() if len(race_gender) > 1 else "male"

        # Re-parse if gender was passed as third word
        if len(parts) >= 4:
            name = parts[1]
            race = parts[2].lower()
            # Check remaining for gender
            remaining = args.strip().split()
            if len(remaining) >= 4:
                gender = remaining[3].lower()

        if race not in RACE_PRESETS:
            tg_send(token, cid, f"\\u274c Unknown race '<b>{race}</b>'. Use <code>/model</code> to see options.")
            return

        gender = GENDER_OPTIONS.get(gender, "male")
        model_hash = generate_model_hash(name, cid)

        tg_send(token, cid, (
            f"\\U0001f9ec <b>Generating DNA for {name}...</b>\\n"
            f"Race: {RACE_PRESETS[race][0]} {RACE_PRESETS[race][1]}\\n"
            f"Gender: {gender}\\n"
            f"Hash: <code>#{model_hash}</code>"
        ))
        tg_typing(token, cid)

        try:
            dna = generate_model_dna(api_keys, race, gender, name)
        except Exception as e:
            tg_send(token, cid, f"\\u274c DNA generation failed: {str(e)[:200]}")
            return

        # Store in registry
        registry_key = f"{cid}_{model_hash}"
        MODEL_REGISTRY[registry_key] = {
            "name": name,
            "hash": model_hash,
            "race": race,
            "gender": gender,
            "dna": dna,
            "created": time.time(),
        }
        # Also store by name for easy lookup
        name_key = f"{cid}_{name.lower()}"
        MODEL_REGISTRY[name_key] = MODEL_REGISTRY[registry_key]

        # Send DNA summary
        dna_preview = dna[:500] + "..." if len(dna) > 500 else dna
        tg_send(token, cid, (
            f"\\u2705 <b>Model '{name}' created!</b>\\n"
            f"Hash: <code>#{model_hash}</code>\\n"
            f"\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\n\\n"
            f"<b>DNA Preview:</b>\\n"
            f"<i>{dna_preview}</i>\\n\\n"
            f"\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\n"
            f"\\U0001f4cb <b>Use this model:</b>\\n"
            f"<code>/model use #{model_hash} smiling in gym</code>\\n"
            f"<code>/model use {name} LinkedIn headshot</code>"
        ))

        # Generate initial reference prompt
        initial_prompt = build_model_prompt(dna, f"{name} standing naturally, neutral expression, clean background, even studio lighting")
        tg_send(token, cid, (
            f"\\U0001f3b4 <b>Reference Prompt (paste into Gemini):</b>\\n\\n"
            f"<code>{initial_prompt}</code>"
        ))

        captions = generate_captions(api_keys, initial_prompt)
        send_captions(token, cid, captions)
        return

    # ── USE ──
    elif action == "use":
        if len(parts) < 3:
            tg_send(token, cid, "\\u26a0\\ufe0f Usage: <code>/model use #hash your request</code>\\nExample: <code>/model use #a7f2 smiling at camera in gym</code>")
            return

        model_ref = parts[1]
        user_request = parts[2] if len(parts) > 2 else "standing naturally"

        # Lookup by hash or name
        model_data = None
        if model_ref.startswith("#"):
            hash_val = model_ref[1:]
            registry_key = f"{cid}_{hash_val}"
            model_data = MODEL_REGISTRY.get(registry_key)
        else:
            name_key = f"{cid}_{model_ref.lower()}"
            model_data = MODEL_REGISTRY.get(name_key)

        if not model_data:
            tg_send(token, cid, f"\\u274c Model '{model_ref}' not found. Use <code>/model list</code> to see your models.")
            return

        tg_send(token, cid, (
            f"\\U0001f9ec <b>Using {model_data['name']} (#{model_data['hash']})</b>\\n"
            f"<i>{user_request[:100]}</i>"
        ))
        tg_typing(token, cid)

        prompt = build_model_prompt(model_data["dna"], user_request)
        tg_send(token, cid, (
            f"\\U0001f3b4 <b>PinGPT \\u2014 Model Prompt</b>\\n"
            f"\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\n\\n"
            f"<code>{prompt}</code>\\n\\n"
            f"\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\n"
            f"\\U0001f512 <i>DNA locked \\u2014 #{model_data['hash']} \\u2192 paste into Gemini Chat!</i>"
        ))

        captions = generate_captions(api_keys, prompt)
        send_captions(token, cid, captions)
        return

    # ── LIST ──
    elif action == "list":
        # Find all models for this chat (avoid duplicates from name_key)
        seen_hashes = set()
        models = []
        for key, val in MODEL_REGISTRY.items():
            if key.startswith(f"{cid}_") and val["hash"] not in seen_hashes:
                seen_hashes.add(val["hash"])
                models.append(val)

        if not models:
            tg_send(token, cid, "\\U0001f4ed No models yet. Create one with <code>/model create Name race gender</code>")
            return

        lines = []
        for m in sorted(models, key=lambda x: x["created"], reverse=True):
            race_info = RACE_PRESETS.get(m["race"], ("Unknown", "\\U0001f30d", ""))
            lines.append(
                f"  <code>#{m['hash']}</code> \\u2014 <b>{m['name']}</b> "
                f"({race_info[1]} {m['gender']})"
            )

        tg_send(token, cid, (
            f"\\U0001f9ec <b>Your Models ({len(models)})</b>\\n"
            f"\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\n"
            + "\\n".join(lines)
            + "\\n\\n\\U0001f4cb <code>/model use #hash your request</code>"
        ))
        return

    # ── DELETE ──
    elif action == "delete":
        if len(parts) < 2:
            tg_send(token, cid, "\\u26a0\\ufe0f Usage: <code>/model delete #hash</code>")
            return

        model_ref = parts[1]
        hash_val = model_ref[1:] if model_ref.startswith("#") else model_ref

        # Find and remove
        registry_key = f"{cid}_{hash_val}"
        model_data = MODEL_REGISTRY.get(registry_key)

        if not model_data:
            # Try by name
            name_key = f"{cid}_{model_ref.lower()}"
            model_data = MODEL_REGISTRY.get(name_key)
            if model_data:
                hash_val = model_data["hash"]
                registry_key = f"{cid}_{hash_val}"

        if not model_data:
            tg_send(token, cid, f"\\u274c Model '{model_ref}' not found.")
            return

        # Remove both hash key and name key
        name = model_data["name"]
        MODEL_REGISTRY.pop(registry_key, None)
        MODEL_REGISTRY.pop(f"{cid}_{name.lower()}", None)
        tg_send(token, cid, f"\\U0001f5d1\\ufe0f Model '<b>{name}</b>' (#{hash_val}) deleted.")
        return

    else:
        tg_send(token, cid, "\\u274c Unknown action. Use: <code>create</code>, <code>use</code>, <code>list</code>, or <code>delete</code>")

'''

# Insert before generate_custom_dna_response
content = content.replace(
    'def generate_custom_dna_response(token, cid, api_keys, user_request):',
    model_functions + '\ndef generate_custom_dna_response(token, cid, api_keys, user_request):'
)

# ── 3. Add /model to webhook routing ──
content = content.replace(
    '    elif cmd == "/pingpt":\n        cmd_pingpt(token, cid, args, api_keys)\n    elif not text.startswith("/"):',
    '    elif cmd == "/pingpt":\n        cmd_pingpt(token, cid, args, api_keys)\n    elif cmd == "/model":\n        cmd_model(token, cid, args, api_keys)\n    elif not text.startswith("/"):'
)

# Write back
open(filepath, 'w', encoding='utf-8', newline='\n').write(content)
print(f"Done! File now has {len(content.splitlines())} lines")
