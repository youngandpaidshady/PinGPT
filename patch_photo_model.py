"""
Patch: Add photo-to-model flow
1. Cache image_data in PHOTO_CACHE
2. Add extract_dna_from_photo() - Gemini Vision → dense DNA paragraph
3. Modify cmd_model create to detect pending photos
"""

filepath = r'c:\Users\Administrator\Desktop\PinGPT\api\webhook.py'
content = open(filepath, 'r', encoding='utf-8').read()

# ── 1. Cache image_data in handle_photo ──
old_cache = '''    PHOTO_CACHE[cache_key] = {
        "analysis": analysis,
        "timestamp": time.time(),
    }'''

new_cache = '''    PHOTO_CACHE[cache_key] = {
        "analysis": analysis,
        "image_data": image_data,
        "timestamp": time.time(),
    }'''

content = content.replace(old_cache, new_cache)

# ── 2. Add extract_dna_from_photo() before build_model_prompt ──
extract_func = '''
def extract_dna_from_photo(api_keys, image_data, name):
    """Extract a dense DNA paragraph from a real photo using Gemini Vision.
    This is used when creating a model from an uploaded photo."""
    from google import genai
    import base64

    instruction = (
        f"You are a forensic portrait DNA analyst. Analyze this photo and create an EXTREMELY detailed, "
        f"hyper-specific DNA profile paragraph for this person. Name them '{name}'.\\n\\n"
        f"Generate a SINGLE DENSE PARAGRAPH (300-400 words) describing this EXACT person in forensic detail. "
        f"This paragraph will be used as a text-to-image prompt anchor to recreate this person's likeness.\\n\\n"
        f"INCLUDE ALL OF THESE (do NOT skip any):\\n"
        f"1. FACE: exact shape, width, length, asymmetries you can see\\n"
        f"2. FOREHEAD: height, width, any creases or lines\\n"
        f"3. EYES: shape PER EYE, exact color, spacing, depth, lid type, under-eye features\\n"
        f"4. EYEBROWS: shape, thickness, density, any gaps\\n"
        f"5. NOSE: bridge width/height, tip shape, nostril shape/flare, pore visibility\\n"
        f"6. LIPS: upper/lower thickness ratio, Cupid's bow, pigmentation, philtrum\\n"
        f"7. JAWLINE: definition, angle, chin shape/projection\\n"
        f"8. CHEEKS: bone prominence, fullness, dimples\\n"
        f"9. SKIN (most detail): exact tone + undertone, texture per zone, oil/shine zones, "
        f"EVERY visible blemish with exact position (acne marks, dark spots, moles, PIH), "
        f"scars, under-eye darkness\\n"
        f"10. HAIR: exact shade, texture type (1A-4C), curl pattern, length, style, hairline, density\\n"
        f"11. FACIAL HAIR: type, coverage, density, patchiness\\n"
        f"12. BUILD: body type, shoulders, neck\\n"
        f"13. DISTINGUISHING FEATURES: 2-3 instantly recognizable unique features\\n\\n"
        f"RULES:\\n"
        f"- Describe what you ACTUALLY SEE, not assumptions\\n"
        f"- Include EVERY imperfection — asymmetry, marks, texture, bags, patchiness\\n"
        f"- Output a SINGLE PARAGRAPH, no line breaks, no labels, no bullet points\\n"
        f"- Start with age estimate and gender, then flow through all features\\n"
        f"- Be SPECIFIC: not 'dark skin' but 'deep warm brown skin with golden copper undertone'\\n"
        f"- Position blemishes: 'cluster of 3 PIH spots on left cheek near jawline'\\n"
        f"- End with the 2-3 distinguishing features"
    )

    b64_image = base64.b64encode(image_data).decode("utf-8")

    shuffled = list(api_keys)
    random.shuffle(shuffled)
    last_error = None
    for key in shuffled:
        try:
            client = genai.Client(api_key=key)
            r = client.models.generate_content(
                model=PROMPT_MODEL,
                contents=[{"role": "user", "parts": [
                    {"inline_data": {"mime_type": "image/jpeg", "data": b64_image}},
                    {"text": instruction}
                ]}],
            )
            dna = r.text.strip()
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


'''

content = content.replace(
    'def build_model_prompt(model_dna, user_request):',
    extract_func + 'def build_model_prompt(model_dna, user_request):'
)

# ── 3. Rewrite cmd_model CREATE to detect pending photos ──
old_create_block = '''    # \u2500\u2500 CREATE \u2500\u2500
    if action == "create":
        if len(parts) < 2:
            tg_send(token, cid, (
                "\\u26a0\\ufe0f Usage: <code>/model create Name description</code>\\n\\n"
                "<b>Examples:</b>\\n"
                "<code>/model create Aisha nigerian woman</code>\\n"
                "<code>/model create Kenji japanese businessman</code>\\n"
                "<code>/model create Luna mixed race girl with freckles</code>\\n"
                "<code>/model create Marcus black male, athletic</code>\\n"
                "<code>/model create Sofia mediterranean, olive skin</code>"
            ))
            return

        # Natural language: first word after "create" = name, rest = description
        name = parts[1]
        description = parts[2] if len(parts) > 2 else name  # If no description, use name as hint

        model_hash = generate_model_hash(name, cid)

        tg_send(token, cid, (
            f"\\U0001f9ec <b>Generating DNA for {name}...</b>\\n"
            f"<i>{description[:100]}</i>\\n"
            f"Hash: <code>#{model_hash}</code>"
        ))
        tg_typing(token, cid)

        try:
            dna = generate_model_dna(api_keys, description, name)
        except Exception as e:
            tg_send(token, cid, f"\\u274c DNA generation failed: {str(e)[:200]}")
            return'''

new_create_block = '''    # \u2500\u2500 CREATE \u2500\u2500
    if action == "create":
        if len(parts) < 2:
            tg_send(token, cid, (
                "\\u26a0\\ufe0f Usage: <code>/model create Name description</code>\\n\\n"
                "<b>From text (fictional):</b>\\n"
                "<code>/model create Aisha nigerian woman</code>\\n"
                "<code>/model create Kenji japanese businessman</code>\\n\\n"
                "<b>From photo (copy a face):</b>\\n"
                "1. Send a photo first\\n"
                "2. Then: <code>/model create Tracy</code>\\n"
                "The bot extracts the face DNA from your photo!"
            ))
            return

        name = parts[1]
        description = parts[2] if len(parts) > 2 else None
        model_hash = generate_model_hash(name, cid)

        # Check if there's a pending photo to extract DNA from
        cache_key = f"{cid}"
        has_photo = (cache_key in PHOTO_CACHE and
                     (time.time() - PHOTO_CACHE[cache_key]["timestamp"]) < PHOTO_CACHE_TTL and
                     PHOTO_CACHE[cache_key].get("image_data"))

        if has_photo and not description:
            # ── PHOTO MODE: extract DNA from uploaded photo ──
            tg_send(token, cid, (
                f"\\U0001f4f8 <b>Extracting face DNA from your photo...</b>\\n"
                f"Model: {name}\\n"
                f"Hash: <code>#{model_hash}</code>"
            ))
            tg_typing(token, cid)

            try:
                dna = extract_dna_from_photo(api_keys, PHOTO_CACHE[cache_key]["image_data"], name)
            except Exception as e:
                tg_send(token, cid, f"\\u274c DNA extraction failed: {str(e)[:200]}")
                return

            source = "photo"
        else:
            # ── TEXT MODE: generate fictional DNA ──
            if not description:
                description = name  # Use name as hint
            tg_send(token, cid, (
                f"\\U0001f9ec <b>Generating DNA for {name}...</b>\\n"
                f"<i>{description[:100]}</i>\\n"
                f"Hash: <code>#{model_hash}</code>"
            ))
            tg_typing(token, cid)

            try:
                dna = generate_model_dna(api_keys, description, name)
            except Exception as e:
                tg_send(token, cid, f"\\u274c DNA generation failed: {str(e)[:200]}")
                return

            source = "generated"'''

content = content.replace(old_create_block, new_create_block)

# ── 4. Update the success message to show source ──
old_success = '''        # Send DNA + usage instructions (no captions)
        dna_preview = dna[:600] + "..." if len(dna) > 600 else dna
        tg_send(token, cid, (
            f"\\u2705 <b>Model \'{name}\' spawned!</b>\\n"
            f"Hash: <code>#{model_hash}</code>\\n"'''

new_success = '''        # Send DNA + usage instructions (no captions)
        source_label = "\\U0001f4f8 Extracted from photo" if source == "photo" else "\\U0001f9ec Generated"
        dna_preview = dna[:600] + "..." if len(dna) > 600 else dna
        tg_send(token, cid, (
            f"\\u2705 <b>Model \'{name}\' spawned!</b>\\n"
            f"Hash: <code>#{model_hash}</code> \\u2014 {source_label}\\n"'''

content = content.replace(old_success, new_success)

# ── 5. Update the model data to store source ──
old_store = '''        MODEL_REGISTRY[registry_key] = {
            "name": name,
            "hash": model_hash,
            "description": description,
            "dna": dna,
            "created": time.time(),
        }'''

new_store = '''        MODEL_REGISTRY[registry_key] = {
            "name": name,
            "hash": model_hash,
            "description": description or "from photo",
            "source": source,
            "dna": dna,
            "created": time.time(),
        }'''

content = content.replace(old_store, new_store)

# ── 6. Update help text to mention photo flow ──
old_help_model = '''            "\\U0001f9ec <b>PinGPT Model Lab</b>\\n"'''
new_help_model = '''            "\\U0001f9ec <b>PinGPT Model Lab</b>\\n"'''
# (help already shows the updated examples from the create block, so no change needed)

# Write
open(filepath, 'w', encoding='utf-8', newline='\n').write(content)
print(f"Done! {len(content.splitlines())} lines")

# Verify syntax
import py_compile
py_compile.compile(filepath, doraise=True)
print("Syntax OK")
