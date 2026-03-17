"""
Fix prompt delivery + refine DNA:
1. Add message chunking to tg_send (split at 4000 chars)
2. Trim build_model_prompt — compact the rules, keep DNA + scene priority
3. Strengthen anti-AI in DNA generation itself (bake it into the DNA paragraph, not just rules)
"""

filepath = r'c:\Users\Administrator\Desktop\PinGPT\api\webhook.py'
content = open(filepath, 'r', encoding='utf-8').read()

# ── 1. Add message chunking to tg_send ──
old_tg_send = '''def tg_send(token, chat_id, text, parse_mode="HTML"):
    import urllib.request
    payload = json.dumps({"chat_id": chat_id, "text": text, "parse_mode": parse_mode})
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=payload.encode(), headers={"Content-Type": "application/json"}
    )
    try:
        urllib.request.urlopen(req)
    except Exception as e:
        logger.error(f"TG send error: {e}")'''

new_tg_send = '''def tg_send(token, chat_id, text, parse_mode="HTML"):
    import urllib.request
    # Telegram max message length is 4096 chars — split if needed
    MAX_LEN = 4000  # Leave some margin
    chunks = []
    while len(text) > MAX_LEN:
        # Try to split at last newline before limit
        split_at = text.rfind("\\n", 0, MAX_LEN)
        if split_at == -1:
            split_at = MAX_LEN
        chunks.append(text[:split_at])
        text = text[split_at:].lstrip("\\n")
    chunks.append(text)

    for chunk in chunks:
        if not chunk.strip():
            continue
        payload = json.dumps({"chat_id": chat_id, "text": chunk, "parse_mode": parse_mode})
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=payload.encode(), headers={"Content-Type": "application/json"}
        )
        try:
            urllib.request.urlopen(req)
        except Exception as e:
            logger.error(f"TG send error: {e}")'''

content = content.replace(old_tg_send, new_tg_send)

# ── 2. Compact the build_model_prompt — less bloat, same effect ──
old_prompt = '''def build_model_prompt(model_dna, user_request):
    """Build UGC-grade hyper-realistic image prompt using stored model DNA + user's request."""

    # Pick random camera spec and realism modifiers
    camera = random.choice(CAMERA_SPECS)
    realism = random.sample(REALISM_MODIFIERS, min(4, len(REALISM_MODIFIERS)))

    return (
        f"IDENTITY DNA (every detail is IMMUTABLE — do NOT alter):\\n"
        f"{model_dna}\\n\\n"
        f"--- SCENE ---\\n"
        f"{user_request}\\n"
        f"(Stage this scene naturally — realistic pose, natural body language, "
        f"environment-appropriate lighting. Make it look candid, not posed.)\\n\\n"
        f"--- HYPER-REALISM REQUIREMENTS ---\\n"
        f"Camera: {camera}\\n"
        f"Realism details that MUST be visible:\\n"
        f"- {realism[0]}\\n"
        f"- {realism[1]}\\n"
        f"- {realism[2]}\\n"
        f"- {realism[3] if len(realism) > 3 else 'natural ambient occlusion and contact shadows'}\\n"
        f"- Clothing has real fabric weight, natural creases, not CGI-smooth\\n"
        f"- Background has natural depth of field blur, not uniform\\n"
        f"- Lighting matches environment (no studio flat-light unless specified)\\n\\n"
        f"--- ANTI-AI RULES (MANDATORY \u2014 violation = failure) ---\\n"
        f"- ZERO AI smoothing \u2014 every pore, bump, texture variation must render\\n"
        f"- ZERO symmetry correction \u2014 the face MUST be naturally asymmetric (one eye slightly bigger, "
        f"jawline slightly uneven, one eyebrow marginally higher)\\n"
        f"- ZERO beauty filter/glow \u2014 no ambient bloom, no skin luminosity, no ethereal backlight\\n"
        f"- ZERO perfect teeth \u2014 real teeth alignment, not veneers\\n"
        f"- ZERO stock expression \u2014 genuine micro-expression with tension in specific facial muscles\\n"
        f"- Skin MUST have: visible pores (especially nose/cheeks), tonal variation between zones, "
        f"visible capillaries near nose wings, natural oil/matte zones, under-eye texture\\n"
        f"- Hair MUST have: flyaways, stray strands, natural frizz, inconsistent curl pattern, "
        f"not every strand perfectly placed\\n"
        f"- Clothing MUST have: real fabric weight, natural wrinkles from wearing, seams visible, "
        f"not digitally pressed or painted on\\n"
        f"- Hands MUST have: visible knuckle wrinkles, nail texture, vein visibility, "
        f"correct finger proportions (AI always fails hands)\\n"
        f"- Background MUST have: natural depth blur falloff, not uniform gaussian \u2014 "
        f"real lens bokeh with shape and chromatic fringing\\n"
        f"- Every mole, scar, mark, blemish from DNA MUST appear at exact described position\\n"
        f"- This must look like a REAL PHOTOGRAPH taken by a real camera of a REAL PERSON\\n\\n"
        f"--- IDENTITY LOCK ---\\n"
        f"All facial features, skin marks, blemishes, moles, scars, distinguishing features "
        f"described in the DNA are IMMUTABLE. Only the scene changes. This must look like "
        f"a real photograph of a real person, not an AI render.\\n\\n"
        f"9:16 portrait, high resolution, no watermark, no text overlay, no AI smoothing, "
        f"no beauty filter, raw unprocessed look"
    )'''

new_prompt = '''def build_model_prompt(model_dna, user_request):
    """Build UGC-grade hyper-realistic image prompt using stored model DNA + user's request."""

    camera = random.choice(CAMERA_SPECS)

    return (
        f"{model_dna}\\n\\n"
        f"SCENE: {user_request}. Candid, not posed. Natural body language.\\n\\n"
        f"PHOTO SPECS: {camera}. 9:16 portrait. RAW unprocessed look.\\n\\n"
        f"MANDATORY REALISM (non-negotiable):\\n"
        f"- Real skin: visible pores on nose/cheeks, tonal variation between zones, "
        f"natural oil on T-zone, matte on jaw. Under-eye texture and slight darkness.\\n"
        f"- Real hair: flyaways, stray strands, frizz, inconsistent curl. Not every strand placed.\\n"
        f"- Real face: NATURALLY ASYMMETRIC. One eye slightly bigger, jaw slightly uneven. "
        f"No symmetry correction. No beauty filter.\\n"
        f"- Real clothing: fabric weight, wearing wrinkles, visible seams. Not painted on.\\n"
        f"- Real background: natural lens bokeh, not uniform blur. Chromatic fringing.\\n"
        f"- Every mole, scar, mark, blemish from description above MUST appear at correct position.\\n"
        f"- ZERO AI smoothing, ZERO glow/bloom, ZERO stock-photo expression.\\n"
        f"- This is a REAL PHOTOGRAPH of a REAL PERSON, not an AI render."
    )'''

content = content.replace(old_prompt, new_prompt)

# ── 3. Strengthen DNA generation — tell it to bake anti-AI into the paragraph itself ──
old_dna_opening = (
    'f"You are a forensic character designer. Create an EXTREMELY detailed, hyper-specific DNA profile '
    'f"for a FICTIONAL character named \'{name}\'.\\n\\n"'
)
new_dna_opening = (
    'f"You are creating a REAL-LOOKING character profile for UGC content generation. '
    'f"Create an EXTREMELY detailed, hyper-specific physical description '
    'f"for a FICTIONAL character named \'{name}\'. The description must make AI image generators '
    'f"produce a person who looks INDISTINGUISHABLE from a real photograph — not AI-pretty, not smooth, not perfect.\\n\\n"'
)
content = content.replace(old_dna_opening, new_dna_opening)

# Write
open(filepath, 'w', encoding='utf-8', newline='\n').write(content)
print(f"Done! {len(content.splitlines())} lines")

# Verify syntax
import py_compile
py_compile.compile(filepath, doraise=True)
print("Syntax OK")
