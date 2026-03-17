"""
Patch: Fix model UX
1. Make create natural language (no rigid race keywords)
2. Remove captions from create  
3. Add #hash shortcut in webhook routing
4. Update help text
"""

filepath = r'c:\Users\Administrator\Desktop\PinGPT\api\webhook.py'
content = open(filepath, 'r', encoding='utf-8').read()

# ── 1. Rewrite generate_model_dna to accept free-text description ──
old_dna_func = '''def generate_model_dna(api_keys, race_key, gender, name):
    """Use Gemini to generate an atomic-level DNA profile for a fictional model."""
    from google import genai

    race_name, _, race_baseline = RACE_PRESETS.get(race_key, RACE_PRESETS["mixed"])
    gender_str = GENDER_OPTIONS.get(gender.lower(), "male")

    instruction = (
        f"You are a forensic character designer. Create an EXTREMELY detailed, hyper-specific DNA profile "
        f"for a FICTIONAL {gender_str} character named '{name}' of {race_name} descent.\\n\\n"
        f"BASELINE ETHNIC FEATURES (starting point only \u2014 randomize unique variations):\\n"
        f"{race_baseline}\\n\\n"'''

new_dna_func = '''def generate_model_dna(api_keys, description, name):
    """Use Gemini to generate an atomic-level DNA profile for a fictional model.
    Accepts free-form description like 'nigerian woman', 'japanese businessman', 'mixed race girl with freckles'."""
    from google import genai

    instruction = (
        f"You are a forensic character designer. Create an EXTREMELY detailed, hyper-specific DNA profile "
        f"for a FICTIONAL character named '{name}'.\\n\\n"
        f"USER DESCRIPTION: {description}\\n"
        f"Use this description to determine ethnicity, gender, age range, and base features. "
        f"If gender is not specified, infer from the name. If ethnicity is vague, make creative choices.\\n\\n"'''

content = content.replace(old_dna_func, new_dna_func)

# ── 2. Rewrite cmd_model CREATE section ──
old_create = '''    # \u2500\u2500 CREATE \u2500\u2500
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
            tg_send(token, cid, f"\\u274c Unknown race \'<b>{race}</b>\'. Use <code>/model</code> to see options.")
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
            f"\\u2705 <b>Model \'{name}\' created!</b>\\n"
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
        return'''

new_create = '''    # \u2500\u2500 CREATE \u2500\u2500
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
            return

        # Store in registry
        registry_key = f"{cid}_{model_hash}"
        MODEL_REGISTRY[registry_key] = {
            "name": name,
            "hash": model_hash,
            "description": description,
            "dna": dna,
            "created": time.time(),
        }
        # Also store by name for easy lookup
        name_key = f"{cid}_{name.lower()}"
        MODEL_REGISTRY[name_key] = MODEL_REGISTRY[registry_key]

        # Send DNA + usage instructions (no captions)
        dna_preview = dna[:600] + "..." if len(dna) > 600 else dna
        tg_send(token, cid, (
            f"\\u2705 <b>Model \'{name}\' spawned!</b>\\n"
            f"Hash: <code>#{model_hash}</code>\\n"
            f"\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\n\\n"
            f"<b>DNA:</b>\\n"
            f"<i>{dna_preview}</i>\\n\\n"
            f"\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\n"
            f"<b>Now use your model:</b>\\n"
            f"<code>#{model_hash} smiling in gym</code>\\n"
            f"<code>#{model_hash} LinkedIn headshot in blazer</code>\\n"
            f"<code>#{model_hash} standing in rain, cyberpunk city</code>"
        ))
        return'''

content = content.replace(old_create, new_create)

# ── 3. Update help text ──
old_help = '''            "\\U0001f9ec <b>PinGPT Model Lab</b>\\n"
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
            + "\\n".join(f"  {v[1]} <code>{k}</code> \\u2014 {v[0]}" for k, v in RACE_PRESETS.items())'''

new_help = '''            "\\U0001f9ec <b>PinGPT Model Lab</b>\\n"
            "\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\n\\n"
            "<b>Create a model (natural language):</b>\\n"
            "<code>/model create Aisha nigerian woman</code>\\n"
            "<code>/model create Kenji japanese businessman</code>\\n"
            "<code>/model create Luna mixed race girl with freckles</code>\\n\\n"
            "<b>Use a model (just type #hash):</b>\\n"
            "<code>#a7f2 smiling in gym</code>\\n"
            "<code>#a7f2 LinkedIn headshot in blazer</code>\\n\\n"
            "<b>Other:</b>\\n"
            "<code>/model list</code> \\u2014 see your models\\n"
            "<code>/model delete #a7f2</code> \\u2014 remove a model"'''

content = content.replace(old_help, new_help)

# ── 4. Remove captions from USE section ──
old_use_captions = '''        captions = generate_captions(api_keys, prompt)
        send_captions(token, cid, captions)
        return

    # \u2500\u2500 LIST \u2500\u2500'''

new_use_captions = '''        return

    # \u2500\u2500 LIST \u2500\u2500'''

content = content.replace(old_use_captions, new_use_captions, 1)

# ── 5. Update LIST "no models" text ──
content = content.replace(
    'No models yet. Create one with <code>/model create Name race gender</code>',
    'No models yet. Create one with <code>/model create Name description</code>'
)

# ── 6. Update LIST model display (remove race_info since we no longer store race) ──
old_list_line = '''            race_info = RACE_PRESETS.get(m["race"], ("Unknown", "\\U0001f30d", ""))
            lines.append(
                f"  <code>#{m['hash']}</code> \\u2014 <b>{m['name']}</b> "
                f"({race_info[1]} {m['gender']})"
            )'''

new_list_line = '''            desc = m.get("description", m.get("race", ""))[:40]
            lines.append(
                f"  <code>#{m['hash']}</code> \\u2014 <b>{m['name']}</b> "
                f"(<i>{desc}</i>)"
            )'''

content = content.replace(old_list_line, new_list_line)

# ── 7. Update LIST footer ──
content = content.replace(
    '\\U0001f4cb <code>/model use #hash your request</code>',
    '\\U0001f4cb Type <code>#hash your request</code> to use a model'
)

# ── 8. Add #hash shortcut in webhook routing ──
# Before the "elif not text.startswith("/")" block, add hash detection
old_routing = '''    elif not text.startswith("/"):
        # Check if user has a pending photo session
        cache_key = f"{cid}"'''

new_routing = '''    elif text.startswith("#") and len(text) > 2:
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
            tg_send(token, cid, f"\\u274c Model <code>#{hash_val}</code> not found. Use <code>/model list</code>.")
    elif not text.startswith("/"):
        # Check if user has a pending photo session
        cache_key = f"{cid}"'''

content = content.replace(old_routing, new_routing)

# Write
open(filepath, 'w', encoding='utf-8', newline='\n').write(content)
print(f"Done! {len(content.splitlines())} lines")

# Verify syntax
import py_compile
py_compile.compile(filepath, doraise=True)
print("Syntax OK")
