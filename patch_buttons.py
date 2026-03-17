"""
Patch: Button-driven model UX + DNA refinement
1. Add send_model_scene_picker() function
2. Show scene buttons after model creation
3. Show scene buttons when #hash typed alone
4. Add model_scene callback handler
5. Add model_ctx handler (product context after scene pick)
6. Add USE buttons to /model list
7. Strengthen anti-AI DNA rules
"""

filepath = r'c:\Users\Administrator\Desktop\PinGPT\api\webhook.py'
content = open(filepath, 'r', encoding='utf-8').read()

# ── 1. Add send_model_scene_picker() + MODEL_PENDING before handle_callback_query ──
scene_picker_code = '''
# ─── Model Scene Picker ──────────────────────────────────────────────────────
MODEL_PENDING = {}  # {chat_id: {"hash": str, "scene": str}} — awaiting product/context input

def send_model_scene_picker(token, cid, model_hash, model_name):
    """Send inline keyboard with UGC scene options for a model."""
    buttons = [
        [
            {"text": "\U0001f4e6 Product Hold", "callback_data": f"mscene:{model_hash}:product-hold"},
            {"text": "\U0001f4f8 Selfie", "callback_data": f"mscene:{model_hash}:selfie"},
        ],
        [
            {"text": "\U0001f5e3 Testimonial", "callback_data": f"mscene:{model_hash}:testimonial"},
            {"text": "\U0001f305 Lifestyle", "callback_data": f"mscene:{model_hash}:lifestyle"},
        ],
        [
            {"text": "\U0001f4e6 Unboxing", "callback_data": f"mscene:{model_hash}:unboxing"},
            {"text": "\U0001f3cb Gym", "callback_data": f"mscene:{model_hash}:gym"},
        ],
        [
            {"text": "\u2615 Cafe", "callback_data": f"mscene:{model_hash}:cafe"},
            {"text": "\U0001f324 Outdoor", "callback_data": f"mscene:{model_hash}:outdoor"},
        ],
        [
            {"text": "\U0001f6cf Morning Routine", "callback_data": f"mscene:{model_hash}:morning-routine"},
            {"text": "\U0001f4bb Desk", "callback_data": f"mscene:{model_hash}:desk"},
        ],
        [
            {"text": "\U0001f373 Cooking", "callback_data": f"mscene:{model_hash}:cooking"},
            {"text": "\u2194\ufe0f Before/After", "callback_data": f"mscene:{model_hash}:before-after"},
        ],
        [
            {"text": "\u270d\ufe0f Custom (type anything)", "callback_data": f"mscene:{model_hash}:custom"},
        ],
    ]
    tg_send_with_keyboard(token, cid, (
        f"\\U0001f3ac <b>Pick a scene for {model_name}:</b>\\n"
        f"<code>#{model_hash}</code>"
    ), buttons)


'''

content = content.replace(
    '\ndef handle_callback_query(token, cid, callback_query, api_keys):',
    scene_picker_code + '\ndef handle_callback_query(token, cid, callback_query, api_keys):'
)

# ── 2. Add mscene callback handler inside handle_callback_query ──
old_action_cb = '''    # ACTION CALLBACKS: action:{style_key}:{action_key}
    if data.startswith("action:"):'''

new_action_cb = '''    # MODEL SCENE CALLBACKS: mscene:{hash}:{scene_key}
    if data.startswith("mscene:"):
        parts = data.split(":", 2)
        if len(parts) == 3:
            _, model_hash, scene_key = parts
            registry_key = f"{cid}_{model_hash}"
            model_data = MODEL_REGISTRY.get(registry_key)
            if not model_data:
                tg_answer_callback(token, cb_id, "Model not found")
                return

            if scene_key == "custom":
                # Store pending state, wait for user text
                MODEL_PENDING[str(cid)] = {"hash": model_hash, "name": model_data["name"]}
                tg_answer_callback(token, cb_id, "Type your scene description!")
                tg_send(token, cid, (
                    f"\\u270d\\ufe0f <b>Type what you want {model_data['name']} doing:</b>\\n\\n"
                    f"Examples:\\n"
                    f"\\u2022 <i>smiling at camera on a rooftop at sunset</i>\\n"
                    f"\\u2022 <i>holding a green smoothie in a modern kitchen</i>\\n"
                    f"\\u2022 <i>LinkedIn headshot in navy blazer</i>"
                ))
                return

            scene_desc = UGC_SCENES.get(scene_key, "standing naturally")
            scene_name = scene_key.replace("-", " ").title()
            tg_answer_callback(token, cb_id, f"{scene_name} \\u2714")

            # Check if scene needs a product
            needs_product = scene_key in ("product-hold", "unboxing", "selfie", "morning-routine")
            if needs_product:
                MODEL_PENDING[str(cid)] = {
                    "hash": model_hash,
                    "name": model_data["name"],
                    "scene": scene_key,
                }
                tg_send(token, cid, (
                    f"\\U0001f4e6 <b>What product or item?</b>\\n\\n"
                    f"Examples:\\n"
                    f"\\u2022 <i>coffee cup</i>\\n"
                    f"\\u2022 <i>face serum bottle</i>\\n"
                    f"\\u2022 <i>protein shake</i>\\n"
                    f"\\u2022 <i>wireless headphones</i>"
                ))
                return

            # No product needed — generate directly
            tg_typing(token, cid)
            user_request = f"{scene_name} scene"
            prompt = build_model_prompt(model_data["dna"], user_request)
            tg_send(token, cid, (
                f"\\U0001f3b4 <b>PinGPT \\u2014 {model_data['name']} \\u00d7 {scene_name}</b>\\n"
                f"\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\n\\n"
                f"<code>{prompt}</code>\\n\\n"
                f"\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\n"
                f"\\U0001f512 <i>DNA locked \\u2014 #{model_hash} \\u2192 paste into Gemini!</i>"
            ))
            send_model_scene_picker(token, cid, model_hash, model_data["name"])
        return

    # ACTION CALLBACKS: action:{style_key}:{action_key}
    if data.startswith("action:"):'''

content = content.replace(old_action_cb, new_action_cb)

# ── 3. Make #hash with no request show scene picker ──
old_hash_routing = '''    elif text.startswith("#") and len(text) > 2:
        # #hash shortcut: #a7f2 smiling in gym
        hash_parts = text.split(None, 1)
        hash_val = hash_parts[0][1:]  # Remove #
        user_request = hash_parts[1] if len(hash_parts) > 1 else "standing naturally, neutral expression"
        registry_key = f"{cid}_{hash_val}"
        model_data = MODEL_REGISTRY.get(registry_key)
        if model_data:
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
                f"\\U0001f512 <i>DNA locked \\u2014 #{model_data['hash']} \\u2192 paste into Gemini!</i>"
            ))
        else:
            tg_send(token, cid, f"\\u274c Model <code>#{hash_val}</code> not found. Use <code>/model list</code>.")'''

new_hash_routing = '''    elif text.startswith("#") and len(text) > 2:
        # #hash shortcut
        hash_parts = text.split(None, 1)
        hash_val = hash_parts[0][1:]  # Remove #
        registry_key = f"{cid}_{hash_val}"
        model_data = MODEL_REGISTRY.get(registry_key)
        if model_data:
            if len(hash_parts) > 1:
                # Has a request: #hash smiling in gym → generate directly
                user_request = hash_parts[1]
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
                    f"\\U0001f512 <i>DNA locked \\u2014 #{model_data['hash']} \\u2192 paste into Gemini!</i>"
                ))
            else:
                # No request: #hash alone → show scene picker buttons
                send_model_scene_picker(token, cid, hash_val, model_data["name"])
        else:
            tg_send(token, cid, f"\\u274c Model <code>#{hash_val}</code> not found. Use <code>/model list</code>.")'''

content = content.replace(old_hash_routing, new_hash_routing)

# ── 4. Handle MODEL_PENDING in the free-text routing ──
# When user types text and has a pending model scene, use it
old_freetext = '''    elif not text.startswith("/"):
        # Check if user has a pending photo session
        cache_key = f"{cid}"'''

new_freetext = '''    elif not text.startswith("/"):
        # Check if user has a pending model scene context
        pending_key = str(cid)
        if pending_key in MODEL_PENDING:
            pending = MODEL_PENDING.pop(pending_key)
            model_hash = pending["hash"]
            model_name = pending["name"]
            registry_key = f"{cid}_{model_hash}"
            model_data = MODEL_REGISTRY.get(registry_key)
            if model_data:
                scene_key = pending.get("scene")
                if scene_key:
                    # Product/context for a scene
                    scene_desc = UGC_SCENES.get(scene_key, "")
                    user_request = f"{scene_key.replace('-', ' ')} with {text}. {scene_desc}"
                else:
                    # Custom free-text scene
                    user_request = text

                tg_send(token, cid, (
                    f"\\U0001f9ec <b>Using {model_name} (#{model_hash})</b>\\n"
                    f"<i>{user_request[:100]}</i>"
                ))
                tg_typing(token, cid)
                prompt = build_model_prompt(model_data["dna"], user_request)
                tg_send(token, cid, (
                    f"\\U0001f3b4 <b>PinGPT \\u2014 {model_name}</b>\\n"
                    f"\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\n\\n"
                    f"<code>{prompt}</code>\\n\\n"
                    f"\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\n"
                    f"\\U0001f512 <i>DNA locked \\u2014 #{model_hash} \\u2192 paste into Gemini!</i>"
                ))
                # Show scene picker again for another round
                send_model_scene_picker(token, cid, model_hash, model_name)
            return

        # Check if user has a pending photo session
        cache_key = f"{cid}"'''

content = content.replace(old_freetext, new_freetext)

# ── 5. Show scene picker after model creation ──
old_create_success_end = '''            f"<code>#{model_hash} smiling in gym</code>\\n"
            f"<code>#{model_hash} product-hold with coffee cup</code>\\n"
            f"<code>#{model_hash} testimonial about skincare</code>\\n"
            f"<code>#{model_hash} selfie with protein shake</code>"
        ))
        return'''

new_create_success_end = '''            f"Tap a scene below or type <code>#{model_hash} your request</code>"
        ))
        # Show scene picker buttons
        send_model_scene_picker(token, cid, model_hash, name)
        return'''

content = content.replace(old_create_success_end, new_create_success_end)

# ── 6. Add USE buttons to /model list ──
old_list_footer = '''            + "\\n\\n\\U0001f4cb Type <code>#hash your request</code> to use a model"
        ))
        return'''

new_list_footer = '''            + "\\n\\n\\U0001f4cb Tap a model or type <code>#hash your request</code>"
        ))
        # Add USE buttons for each model
        if models:
            use_buttons = []
            row = []
            for m in sorted(models, key=lambda x: x["created"], reverse=True)[:6]:
                row.append({"text": f"\\u25b6\\ufe0f {m['name']}", "callback_data": f"mscene:{m['hash']}:custom"})
                if len(row) == 2:
                    use_buttons.append(row)
                    row = []
            if row:
                use_buttons.append(row)
            tg_send_with_keyboard(token, cid, "\\U0001f447 <b>Quick use:</b>", use_buttons)
        return'''

content = content.replace(old_list_footer, new_list_footer)

# ── 7. Strengthen anti-AI in build_model_prompt ──
old_anti_ai = '''        f"--- ANTI-AI RULES (CRITICAL) ---\\n"
        f"- NO plastic/waxy skin \\u2014 real pores, texture, micro-wrinkles must be visible\\n"
        f"- NO perfectly symmetrical face \\u2014 preserve natural asymmetry from DNA\\n"
        f"- NO AI glow/bloom \\u2014 natural skin finish (matte/oily zones as described)\\n"
        f"- NO generic model face \\u2014 THIS specific person with THEIR imperfections\\n"
        f"- NO smooth gradient skin \\u2014 real tonal variation, visible capillaries\\n"
        f"- NO stock-photo smile \\u2014 genuine, slightly asymmetric expression\\n"
        f"- Every mole, scar, mark, blemish from DNA MUST appear in correct position\\n\\n"'''

new_anti_ai = '''        f"--- ANTI-AI RULES (MANDATORY \u2014 violation = failure) ---\\n"
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
        f"- This must look like a REAL PHOTOGRAPH taken by a real camera of a REAL PERSON\\n\\n"'''

content = content.replace(old_anti_ai, new_anti_ai)

# Write
open(filepath, 'w', encoding='utf-8', newline='\n').write(content)
print(f"Done! {len(content.splitlines())} lines")

# Verify syntax
import py_compile
py_compile.compile(filepath, doraise=True)
print("Syntax OK")
