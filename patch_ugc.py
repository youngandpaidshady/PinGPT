"""
UGC Enhancement Patch:
1. Add UGC_SCENES presets
2. Rewrite build_model_prompt() with hyper-realism + UGC awareness
3. Enhance DNA generation with anti-AI realism rules
4. Update #hash routing to detect UGC keywords
5. Update help text
"""

filepath = r'c:\Users\Administrator\Desktop\PinGPT\api\webhook.py'
content = open(filepath, 'r', encoding='utf-8').read()

# ── 1. Add UGC_SCENES + CAMERA_SPECS after GENDER_OPTIONS ──
ugc_data = '''

# ─── UGC Scene Presets ────────────────────────────────────────────────────────
UGC_SCENES = {
    "product-hold": (
        "holding a product naturally in one hand at chest height, "
        "slightly angled toward camera, casual grip not stiff, "
        "looking at camera with genuine relaxed smile, other hand relaxed at side"
    ),
    "unboxing": (
        "sitting at a table opening a package, tissue paper visible, "
        "looking down at the product with genuine excited expression, "
        "hands actively pulling product from box, natural overhead soft lighting"
    ),
    "testimonial": (
        "upper body framing, facing camera directly, mid-sentence expression, "
        "one hand gesturing naturally while speaking, slightly leaning forward, "
        "engaged conversational posture, warm natural lighting from window"
    ),
    "lifestyle": (
        "candid lifestyle moment using the product naturally, "
        "not looking at camera, captured mid-action, shallow depth of field, "
        "natural environment, golden hour or soft indoor lighting"
    ),
    "selfie": (
        "phone held in one hand at slight high angle for selfie, "
        "other hand holding product near face, casual genuine smile, "
        "slightly off-center framing, front-camera perspective with slight wide-angle"
    ),
    "before-after": (
        "split composition, neutral expression on left side, "
        "confident satisfied expression on right side, same lighting both sides, "
        "clean simple background, clinical but warm feel"
    ),
    "morning-routine": (
        "in a bright bathroom or bedroom, natural morning light from window, "
        "wearing casual loungewear, applying or holding a product as part of routine, "
        "relaxed sleepy-calm expression, messy hair, authentic morning vibe"
    ),
    "gym": (
        "post-workout, light sweat sheen on skin, gym mirror or dark gym background, "
        "wearing athletic wear, holding water bottle or supplement, "
        "breathing slightly heavy, genuine tired-but-satisfied expression"
    ),
    "cafe": (
        "sitting at a cafe table, warm indoor lighting, holding coffee or product, "
        "laptop or phone on table, candid mid-sip or mid-thought expression, "
        "blurred cafe background with warm tones, cozy atmosphere"
    ),
    "outdoor": (
        "standing or walking outdoors in natural daylight, "
        "wind slightly affecting hair, holding or wearing the product, "
        "looking off-camera at something interesting, candid street-style shot"
    ),
    "cooking": (
        "in a kitchen, hands actively preparing food or holding ingredients, "
        "wearing casual home clothes, steam or food prep visible, "
        "looking at what they are doing not camera, natural overhead kitchen lighting"
    ),
    "desk": (
        "sitting at a clean desk, laptop open, product nearby on desk, "
        "one hand on keyboard or holding product, focused or looking at camera, "
        "natural window sidelight, modern workspace background"
    ),
}

# Camera specs for hyper-realism
CAMERA_SPECS = [
    "shot on iPhone 15 Pro, 24mm lens, f/1.78 aperture",
    "shot on Sony A7III, 35mm f/1.4, natural light",
    "shot on Canon EOS R5, 50mm f/1.2, shallow depth of field",
    "iPhone 14 Pro selfie camera, front-facing, slight wide-angle distortion",
    "shot on Fujifilm X-T5, 23mm f/1.4, film-like color science",
    "Google Pixel 8 Pro, natural HDR, computational photography",
]

REALISM_MODIFIERS = [
    "visible skin pores on nose and cheeks",
    "natural under-eye darkness and slight puffiness",
    "subtle fabric texture and wrinkles on clothing",
    "natural hair flyaways and stray strands",
    "slight skin oil/shine on T-zone",
    "genuine asymmetric smile, not perfectly symmetrical",
    "real skin texture with micro-imperfections visible",
    "natural catchlights in eyes from environment",
    "subtle vein visibility on hands and temples",
    "clothing sits naturally with weight and drape, not painted on",
]
'''

content = content.replace(
    '\n# \u2500\u2500\u2500 UGC Scene Presets',
    '\n# \u2500\u2500\u2500 UGC Scene Presets'
) if '\u2500\u2500\u2500 UGC Scene Presets' in content else content

# Insert after GENDER_OPTIONS block
content = content.replace(
    '    "woman": "female",\n}',
    '    "woman": "female",\n}' + ugc_data
)

# ── 2. Rewrite build_model_prompt with hyper-realism + UGC ──
old_prompt_builder = '''def build_model_prompt(model_dna, user_request):
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
        f"- Only the SCENE changes (pose, outfit, setting, lighting) \u2014 the person stays identical\\n"
        f"- Photorealistic, real skin texture with pores and imperfections\\n"
        f"- 9:16 portrait, high resolution, no watermark, no text overlay, no AI smoothing"
    )'''

new_prompt_builder = '''def build_model_prompt(model_dna, user_request):
    """Build UGC-grade hyper-realistic image prompt using stored model DNA + user's request."""

    # Detect UGC scene keywords in the request
    ugc_scene = None
    request_lower = user_request.lower()
    for scene_key, scene_desc in UGC_SCENES.items():
        if scene_key.replace("-", " ") in request_lower or scene_key in request_lower:
            ugc_scene = scene_desc
            break

    # Pick random camera spec and realism modifiers
    camera = random.choice(CAMERA_SPECS)
    realism = random.sample(REALISM_MODIFIERS, min(4, len(REALISM_MODIFIERS)))

    scene_block = user_request
    if ugc_scene:
        scene_block = f"{user_request}. Pose and staging: {ugc_scene}"

    return (
        f"IDENTITY DNA (every detail is IMMUTABLE \u2014 do NOT alter):\\n"
        f"{model_dna}\\n\\n"
        f"--- SCENE ---\\n"
        f"{scene_block}\\n\\n"
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
        f"--- ANTI-AI RULES (CRITICAL) ---\\n"
        f"- NO plastic/waxy skin \u2014 real pores, texture, micro-wrinkles must be visible\\n"
        f"- NO perfectly symmetrical face \u2014 preserve natural asymmetry from DNA\\n"
        f"- NO AI glow/bloom \u2014 natural skin finish (matte/oily zones as described)\\n"
        f"- NO generic model face \u2014 THIS specific person with THEIR imperfections\\n"
        f"- NO smooth gradient skin \u2014 real tonal variation, visible capillaries\\n"
        f"- NO stock-photo smile \u2014 genuine, slightly asymmetric expression\\n"
        f"- Every mole, scar, mark, blemish from DNA MUST appear in correct position\\n\\n"
        f"--- IDENTITY LOCK ---\\n"
        f"All facial features, skin marks, blemishes, moles, scars, distinguishing features "
        f"described in the DNA are IMMUTABLE. Only the scene changes. This must look like "
        f"a real photograph of a real person, not an AI render.\\n\\n"
        f"9:16 portrait, high resolution, no watermark, no text overlay, no AI smoothing, "
        f"no beauty filter, raw unprocessed look"
    )'''

content = content.replace(old_prompt_builder, new_prompt_builder)

# ── 3. Enhance DNA generation instruction with anti-AI realism ──
old_dna_rules = '''        f"RULES:\\n"
        f"- Make them look REAL and SPECIFIC, not generic AI-beautiful\\n"
        f"- Include IMPERFECTIONS \u2014 asymmetry, marks, texture, bags, patchiness\\n"
        f"- The description must be UNIQUE to this one fictional person\\n"
        f"- Output a SINGLE PARAGRAPH, no line breaks, no labels, no bullet points\\n"
        f"- Start with age bracket and gender, then flow through all features\\n"
        f"- End with the 2-3 distinguishing features\\n"
        f"- Aim for 300-400 words of pure dense description"'''

new_dna_rules = '''        f"RULES (UGC-GRADE HYPER-REALISM):\\n"
        f"- Make them INDISTINGUISHABLE from a real person \u2014 not AI-pretty\\n"
        f"- MANDATORY imperfections: slightly asymmetric face, visible pores, under-eye bags, "
        f"uneven skin texture zones, at least 2 specific blemishes with positions, natural oil/shine\\n"
        f"- Give them a REAL person's face, not a model's \u2014 interesting features, not perfect proportions\\n"
        f"- Skin must have tonal variation: slightly darker/lighter zones, capillary redness, undertone shifts\\n"
        f"- Include micro-details: stray eyebrow hairs, lash clumps, lip dryness, pore size variation\\n"
        f"- Hair should have flyaways, natural texture inconsistency, not perfectly styled\\n"
        f"- The description must be UNIQUE to this one fictional person\\n"
        f"- Output a SINGLE PARAGRAPH, no line breaks, no labels, no bullet points\\n"
        f"- Start with age bracket and gender, then flow through all features\\n"
        f"- End with the 2-3 distinguishing features that make them INSTANTLY recognizable\\n"
        f"- Aim for 350-450 words of pure dense description \u2014 more detail = more consistency"'''

content = content.replace(old_dna_rules, new_dna_rules)

# ── 4. Also enhance extract_dna_from_photo for same realism ──
old_photo_rules = '''        f"RULES:\\n"
        f"- Describe what you ACTUALLY SEE, not assumptions\\n"
        f"- Include EVERY imperfection \u2014 asymmetry, marks, texture, bags, patchiness\\n"
        f"- Output a SINGLE PARAGRAPH, no line breaks, no labels, no bullet points\\n"
        f"- Start with age estimate and gender, then flow through all features\\n"
        f"- Be SPECIFIC: not 'dark skin' but 'deep warm brown skin with golden copper undertone'\\n"
        f"- Position blemishes: 'cluster of 3 PIH spots on left cheek near jawline'\\n"
        f"- End with the 2-3 distinguishing features"'''

new_photo_rules = '''        f"RULES (UGC-GRADE HYPER-REALISM):\\n"
        f"- Describe what you ACTUALLY SEE with forensic precision, not assumptions\\n"
        f"- Include EVERY imperfection \u2014 asymmetry, marks, texture, bags, patchiness\\n"
        f"- Capture micro-details: pore size by zone, oil/shine, stray hairs, lip texture, lash clumps\\n"
        f"- Skin tonal variation: where it's slightly darker/redder/more golden\\n"
        f"- Output a SINGLE PARAGRAPH, no line breaks, no labels, no bullet points\\n"
        f"- Start with age estimate and gender, then flow through all features\\n"
        f"- Be SPECIFIC: not 'dark skin' but 'deep warm brown skin with golden copper undertone, "
        f"slight redness around nose, matte finish on forehead with shine on nose bridge'\\n"
        f"- Position EVERY blemish: 'cluster of 3 PIH spots on left cheek near jawline'\\n"
        f"- End with the 2-3 distinguishing features\\n"
        f"- Aim for 350-450 words \u2014 more detail = more consistency across images"'''

content = content.replace(old_photo_rules, new_photo_rules)

# ── 5. Update help text to show UGC scenes ──
old_help = '''            "<b>Use a model (just type #hash):</b>\\n"
            "<code>#a7f2 smiling in gym</code>\\n"
            "<code>#a7f2 LinkedIn headshot in blazer</code>\\n\\n"
            "<b>Other:</b>\\n"
            "<code>/model list</code> \\u2014 see your models\\n"
            "<code>/model delete #a7f2</code> \\u2014 remove a model"'''

new_help = '''            "<b>Use a model (just type #hash):</b>\\n"
            "<code>#a7f2 smiling in gym</code>\\n"
            "<code>#a7f2 LinkedIn headshot in blazer</code>\\n\\n"
            "<b>UGC scenes (auto-detected):</b>\\n"
            "<code>#a7f2 product-hold with coffee cup</code>\\n"
            "<code>#a7f2 testimonial about skincare</code>\\n"
            "<code>#a7f2 selfie with protein shake</code>\\n"
            "<code>#a7f2 morning-routine with face serum</code>\\n"
            "<code>#a7f2 unboxing new headphones</code>\\n"
            "<code>#a7f2 cafe working on laptop</code>\\n\\n"
            "<b>Other:</b>\\n"
            "<code>/model list</code> \\u2014 see your models\\n"
            "<code>/model delete #a7f2</code> \\u2014 remove a model"'''

content = content.replace(old_help, new_help)

# ── 6. Also update the create success message with UGC examples ──
old_success_examples = '''            f"<code>#{model_hash} smiling in gym</code>\\n"
            f"<code>#{model_hash} LinkedIn headshot in blazer</code>\\n"
            f"<code>#{model_hash} standing in rain, cyberpunk city</code>"'''

new_success_examples = '''            f"<code>#{model_hash} smiling in gym</code>\\n"
            f"<code>#{model_hash} product-hold with coffee cup</code>\\n"
            f"<code>#{model_hash} testimonial about skincare</code>\\n"
            f"<code>#{model_hash} selfie with protein shake</code>"'''

content = content.replace(old_success_examples, new_success_examples)

# Write
open(filepath, 'w', encoding='utf-8', newline='\n').write(content)
print(f"Done! {len(content.splitlines())} lines")

# Verify syntax
import py_compile
py_compile.compile(filepath, doraise=True)
print("Syntax OK")
