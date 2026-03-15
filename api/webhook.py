#!/usr/bin/env python3
"""
PinGPT Telegram Bot — Vercel Serverless Webhook Handler
Generates Pinterest-aesthetic anime prompts via Gemini 2.5 Flash.
"""

import os
import json
import random
import logging
from pathlib import Path
from flask import Flask, request, Response

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

PROMPT_MODEL = "gemini-2.5-flash"

# skill.md lives in project root (one level up from api/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILL_FILE = PROJECT_ROOT / "skill.md"

# ─── Data ─────────────────────────────────────────────────────────────────────

CHARACTERS = [
    "Toji Fushiguro", "Satoru Gojo", "Eren Yeager", "Levi Ackerman",
    "Baki Hanma", "Yuji Itadori", "Aqua Hoshino", "Rin Itoshi",
    "Megumi Fushiguro", "Shoto Todoroki", "Loid Forger", "Killua Zoldyck",
    "Sebastian Michaelis", "Jinshi", "Izuku Midoriya", "Sung Jinwoo",
]

MOODS = [
    "dark", "melancholic", "intense", "serene", "contemplative",
    "defiant", "vulnerable", "exhausted", "haunted", "triumphant",
    "restless", "resigned", "predatory", "peaceful",
]

SETTINGS = [
    "dark gym", "rainy night tokyo", "abandoned warehouse", "sunset soccer field",
    "rooftop at night", "dark alley", "locker room", "foggy waterfront",
    "empty train platform", "boxing gym", "liminal hallway", "mountain cliff edge",
    "underground parking", "night beach", "empty classroom", "dimly lit bar counter",
    "cramped studio apartment", "hospital corridor", "abandoned temple",
    "late-night convenience store", "elevator interior", "fire escape landing",
]

COLORS = [
    "desaturated cool", "cold blue", "warm sepia",
    "monochrome b&w", "teal & orange", "muted green", "blood red accent",
    "faded polaroid", "neon bleed",
]

TIMES = [
    "golden hour", "blue hour", "midnight", "overcast dawn", "3am fluorescent",
    "late afternoon classroom", "neon midnight", "pre-storm yellow",
    "eclipse darkness", "hospital fluorescent",
]

WEATHER = [
    "heavy rain", "snowfall", "dense fog", "cherry blossoms", "autumn leaves",
    "dust and ash", "wind only", "ember sparks", "light drizzle", "fireflies",
]

OUTFITS = [
    "gym wear", "streetwear", "shirtless training", "clean formal",
    "dark minimalist", "casual relaxed", "combat ready", "rain gear",
    "athletic jersey", "post-fight", "layered winter", "traditional japanese",
]

LIGHTING = [
    "single source with rim light", "dual cross-light", "underlight",
    "backlight only", "dappled broken light", "colored neon wash", "overcast flat",
]

ART_STYLES = [
    "clean cel-shading", "clean cel-shading", "clean cel-shading",  # weighted 70%
    "clean cel-shading", "clean cel-shading", "clean cel-shading",
    "clean cel-shading", "ink wash", "sketchy lineart", "watercolor bleed",
]

SLIDE_LABELS = [
    ("🪝", "HOOK"),
    ("🌍", "CONTEXT"),
    ("⚡", "ESCALATION"),
    ("🔍", "TEXTURE"),
    ("💧", "MOOD SHIFT"),
    ("🎬", "PEAK"),
    ("🎬", "PEAK"),
    ("📐", "DRAMATIC SHIFT"),
    ("📐", "DRAMATIC SHIFT"),
    ("👑", "CLOSER"),
]

TIKTOK_SOUNDS = [
    "slowed + reverb dark ambient",
    "phonk beat drop",
    "dark orchestral epic",
    "lofi sad beats",
    "emotional piano + rain",
    "Japanese city pop slowed",
    "dark trap instrumental",
    "cinematic bass boost",
]

# ─── Core Logic ───────────────────────────────────────────────────────────────

def load_skill():
    for path in [SKILL_FILE, Path(__file__).parent / "skill.md"]:
        if path.exists():
            return path.read_text(encoding="utf-8")
    return None


def parse_args(text):
    params = dict(character=None, mood=None, setting=None, color=None,
                  time=None, weather=None, outfit=None, lighting=None,
                  style=None, text_overlay=False)
    if not text:
        return params
    free_words = []
    for part in text.strip().split():
        if ":" in part:
            k, v = part.split(":", 1)
            k = k.lower()
            if k == "text":
                params["text_overlay"] = v.lower() in ("yes", "true", "1")
            elif k in params:
                params[k] = v.replace("_", " ")
        else:
            free_words.append(part)
    if free_words:
        name = " ".join(free_words)
        matched = next((c for c in CHARACTERS if name.lower() in c.lower()), name)
        params["character"] = matched
    return params


def build_instruction(p, discover=False):
    lines = ["Generate a single PinGPT prompt following all the rules in the skill file."]
    if discover:
        lines.append(
            "Use your knowledge to pick a currently popular/trending male anime character "
            "from recent anime seasons. Build an accurate physical description — "
            "hair color/style, eye color, build, facial features, signature traits. "
            "Then generate the PinGPT prompt using that character."
        )
    elif p["character"]:
        is_roster = any(p["character"].lower() in c.lower() for c in CHARACTERS)
        lines.append(f"Character: {p['character']}")
        if not is_roster:
            lines.append(
                f"This character is NOT in the built-in roster. "
                f"Use your knowledge to build an accurate physical description for {p['character']} — "
                f"include their exact hair color/style, eye color, build, facial features, "
                f"and any signature traits (scars, markings, accessories). "
                f"Then apply the same PinGPT aesthetic rules as any roster character."
            )
    if p["mood"]:        lines.append(f"Mood: {p['mood']}")
    if p["setting"]:     lines.append(f"Setting/Environment: {p['setting']}")
    if p["color"]:       lines.append(f"Color grade: {p['color']}")
    if p["time"]:        lines.append(f"Time of day: {p['time']}")
    if p["weather"]:     lines.append(f"Weather: {p['weather']}")
    if p["outfit"]:      lines.append(f"Outfit: {p['outfit']}")
    if p["lighting"]:    lines.append(f"Lighting setup: {p['lighting']}")
    if p["style"]:       lines.append(f"Art style: {p['style']}")
    if p["text_overlay"]:lines.append("Include Japanese typography overlay.")
    lines.append(
        "\nOutput ONLY the raw prompt text that will be sent to the image generator. "
        "No markdown formatting, no blockquotes, no metadata, no Pinterest tags. "
        "Just the pure natural language prompt text, nothing else."
    )
    return "\n".join(lines)


def build_tiktok_instruction(character_name):
    """Build Gemini instruction for 10-slide TikTok carousel."""
    return (
        "Generate a 10-slide TikTok carousel for the character: "
        f"{character_name}. Follow Phase 8 (TikTok Slideshow Mode) in the skill file EXACTLY.\n\n"
        "RULES:\n"
        "- Same character with IDENTICAL physical description across all 10 slides\n"
        "- Same art style across all 10 slides (pick one, stick with it)\n"
        "- Each slide MUST differ in at least 3 of: lighting, composition, pose, environment, outfit, color grade, time\n"
        "- Follow the 10-slide narrative tension curve: HOOK → CONTEXT → ESCALATION → TEXTURE → MOOD SHIFT → PEAK → PEAK → DRAMATIC SHIFT → DRAMATIC SHIFT → CLOSER\n"
        "- Slides 8-9 use extreme camera angles (low-angle, high-angle, silhouette, extreme wide) but SAME art style\n"
        "- Slide 10 is wallpaper-quality hero shot\n\n"
        "OUTPUT FORMAT (follow EXACTLY):\n"
        "For each slide, output on its own line:\n"
        "SLIDE_N_TITLE: [brief 2-4 word scene title]\n"
        "SLIDE_N_PROMPT: [complete image generation prompt — raw text, no markdown]\n\n"
        "After all 10 slides, output:\n"
        "TIKTOK_CAPTION: [2 punchy lines with emojis + question hook + save CTA + series hook]\n"
        "TIKTOK_TAGS: [3-5 hashtags ONLY — 1 broad + 1 niche + 1 trending + 1 character]\n"
        "SOUND_SUGGESTION: [trending audio pairing recommendation]\n\n"
        "Output ONLY in the format above. No extra text, no markdown, no numbering outside the format."
    )


def build_series_instruction(character_name, count):
    """Build Gemini instruction for Pinterest series (story arc)."""
    return (
        f"Generate {count} connected story-arc prompts for the character: {character_name}. "
        "Follow Phase 7 (Series Mode) in the skill file.\n\n"
        "RULES:\n"
        "- Same character with IDENTICAL physical description across all prompts\n"
        "- Vary everything else: environment, outfit, pose, color, time, weather\n"
        "- Narrative arc: Start with intense action → middle is contemplative pause → end is solitary wide shot\n"
        "- Different color grades across prompts\n"
        "- Typography in exactly 1 prompt\n\n"
        "OUTPUT FORMAT (follow EXACTLY):\n"
        "For each prompt, output on its own line:\n"
        f"SERIES_N_TITLE: [brief 2-4 word scene title]\n"
        f"SERIES_N_PROMPT: [complete image generation prompt — raw text, no markdown]\n\n"
        "After all prompts, output:\n"
        "PINTEREST_CAPTION: [2-3 sentence SEO description with emojis]\n"
        "PINTEREST_TAGS: [10 relevant Pinterest hashtags]\n"
        "TIKTOK_CAPTION: [short catchy TikTok caption with emojis]\n"
        "TIKTOK_TAGS: [3-5 TikTok hashtags]\n\n"
        "Output ONLY in the format above. No extra text, no markdown."
    )


def parse_tiktok_output(raw):
    """Parse the structured 10-slide TikTok output from Gemini."""
    slides = []
    captions = {}
    for line in raw.split("\n"):
        line = line.strip()
        if not line:
            continue
        for i in range(1, 11):
            if line.startswith(f"SLIDE_{i}_TITLE:"):
                if len(slides) < i:
                    slides.append({"title": line.split(":", 1)[1].strip(), "prompt": ""})
            elif line.startswith(f"SLIDE_{i}_PROMPT:"):
                if i - 1 < len(slides):
                    slides[i - 1]["prompt"] = line.split(":", 1)[1].strip()
                else:
                    slides.append({"title": "", "prompt": line.split(":", 1)[1].strip()})
        if line.startswith("TIKTOK_CAPTION:"):
            captions["caption"] = line.split(":", 1)[1].strip()
        elif line.startswith("TIKTOK_TAGS:"):
            captions["tags"] = line.split(":", 1)[1].strip()
        elif line.startswith("SOUND_SUGGESTION:"):
            captions["sound"] = line.split(":", 1)[1].strip()
    return slides, captions


def parse_series_output(raw, count):
    """Parse the structured series output from Gemini."""
    prompts = []
    captions = {}
    for line in raw.split("\n"):
        line = line.strip()
        if not line:
            continue
        for i in range(1, count + 1):
            if line.startswith(f"SERIES_{i}_TITLE:"):
                if len(prompts) < i:
                    prompts.append({"title": line.split(":", 1)[1].strip(), "prompt": ""})
            elif line.startswith(f"SERIES_{i}_PROMPT:"):
                if i - 1 < len(prompts):
                    prompts[i - 1]["prompt"] = line.split(":", 1)[1].strip()
                else:
                    prompts.append({"title": "", "prompt": line.split(":", 1)[1].strip()})
        if line.startswith("PINTEREST_CAPTION:"):
            captions["pin_caption"] = line.split(":", 1)[1].strip()
        elif line.startswith("PINTEREST_TAGS:"):
            captions["pin_tags"] = line.split(":", 1)[1].strip()
        elif line.startswith("TIKTOK_CAPTION:"):
            captions["tik_caption"] = line.split(":", 1)[1].strip()
        elif line.startswith("TIKTOK_TAGS:"):
            captions["tik_tags"] = line.split(":", 1)[1].strip()
    return prompts, captions


def generate_captions(api_keys, prompt_text):
    """Generate Pinterest + TikTok captions from a generated prompt."""
    instruction = (
        "Based on this anime image prompt, generate social media captions.\n\n"
        f"Prompt: {prompt_text}\n\n"
        "Output EXACTLY in this format (no extra text):\n"
        "PINTEREST_TITLE: [short catchy title, 5-8 words]\n"
        "PINTEREST_DESC: [2-3 sentence SEO description with emojis]\n"
        "PINTEREST_TAGS: [10 relevant hashtags starting with #]\n"
        "TIKTOK_CAPTION: [short catchy caption with emojis, 1-2 lines]\n"
        "TIKTOK_TAGS: [10 trending TikTok hashtags starting with #]"
    )
    try:
        from google import genai
        shuffled = list(api_keys)
        random.shuffle(shuffled)
        for key in shuffled:
            try:
                client = genai.Client(api_key=key)
                r = client.models.generate_content(
                    model=PROMPT_MODEL,
                    contents=[{"role": "user", "parts": [{"text": instruction}]}],
                )
                return parse_captions(r.text.strip())
            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    continue
                raise
    except Exception as e:
        logger.error(f"Caption generation error: {e}")
    return None


def parse_captions(raw):
    """Parse the structured caption output."""
    result = {}
    for line in raw.split("\n"):
        line = line.strip()
        if line.startswith("PINTEREST_TITLE:"):
            result["pin_title"] = line.split(":", 1)[1].strip()
        elif line.startswith("PINTEREST_DESC:"):
            result["pin_desc"] = line.split(":", 1)[1].strip()
        elif line.startswith("PINTEREST_TAGS:"):
            result["pin_tags"] = line.split(":", 1)[1].strip()
        elif line.startswith("TIKTOK_CAPTION:"):
            result["tik_caption"] = line.split(":", 1)[1].strip()
        elif line.startswith("TIKTOK_TAGS:"):
            result["tik_tags"] = line.split(":", 1)[1].strip()
    return result if result else None


def send_captions(token, cid, captions):
    """Send Pinterest + TikTok captions as a separate message."""
    if not captions:
        return
    lines = []
    if captions.get("pin_title"):
        lines.append("📌 <b>Pinterest</b>")
        lines.append(f"<b>Title:</b> {captions['pin_title']}")
    if captions.get("pin_desc"):
        lines.append(f"{captions['pin_desc']}")
    if captions.get("pin_tags"):
        lines.append(f"<code>{captions['pin_tags']}</code>")
    lines.append("")
    if captions.get("tik_caption"):
        lines.append("🎵 <b>TikTok</b>")
        lines.append(f"{captions['tik_caption']}")
    if captions.get("tik_tags"):
        lines.append(f"<code>{captions['tik_tags']}</code>")
    tg_send(token, cid, "\n".join(lines))


def call_gemini(api_keys, skill_text, instruction):
    """Call Gemini with auto key rotation on 429 errors."""
    from google import genai
    shuffled = list(api_keys)
    random.shuffle(shuffled)
    last_error = None
    for key in shuffled:
        try:
            client = genai.Client(api_key=key)
            r = client.models.generate_content(
                model=PROMPT_MODEL,
                contents=[{"role": "user", "parts": [
                    {"text": f"You are PinGPT. Follow these instructions exactly:\n\n{skill_text}\n\n---\n\n{instruction}"}
                ]}],
            )
            prompt = r.text.strip().replace("```", "").replace("> ", "").strip()
            if prompt.startswith('"') and prompt.endswith('"'):
                prompt = prompt[1:-1]
            return prompt
        except Exception as e:
            last_error = e
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                logger.info(f"Key exhausted, rotating... ({len(shuffled)} keys left)")
                continue
            raise  # Non-429 errors bubble up immediately
    raise last_error or Exception("All API keys exhausted (429)")


def tg_send(token, chat_id, text, parse_mode="HTML"):
    import urllib.request
    payload = json.dumps({"chat_id": chat_id, "text": text, "parse_mode": parse_mode})
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=payload.encode(), headers={"Content-Type": "application/json"}
    )
    try:
        urllib.request.urlopen(req)
    except Exception as e:
        logger.error(f"TG send error: {e}")


def tg_typing(token, chat_id):
    import urllib.request
    payload = json.dumps({"chat_id": chat_id, "action": "typing"})
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendChatAction",
        data=payload.encode(), headers={"Content-Type": "application/json"}
    )
    try:
        urllib.request.urlopen(req)
    except Exception:
        pass


# ─── Handlers ─────────────────────────────────────────────────────────────────

def cmd_start(token, cid):
    tg_send(token, cid, (
        "🎴 <b>PinGPT v2.0 — Anime Prompt Engine</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "<b>🎴 CREATE</b>\n"
        "• /pingpt — Generate a single prompt (auto-randomized)\n"
        "• /pingpt Toji mood:dark — Specify character + params\n"
        "• /custom Zoro — Any anime character, even unlisted\n"
        "• /discover — AI picks a trending character\n\n"
        "<b>🎬 CONTENT PACKS</b>\n"
        "• /tiktok Eren — 10-slide TikTok slideshow (viral pacing)\n"
        "• /series Levi 3 — Connected story arc (2-5 images)\n"
        "• /batch 5 — Rapid bulk generation\n\n"
        "<b>📋 INFO</b>\n"
        "• /characters — Full character roster + tiers\n"
        "• /help — All parameters, examples, tips\n\n"
        "<b>🛠 TOOLS</b>\n"
        "• /crop — Remove NanoBanana 2 watermark\n\n"
        "💡 <i>Copy prompt → paste into Gemini Chat → 4K image!</i>"
    ))


def cmd_help(token, cid):
    tg_send(token, cid, (
        "📖 <b>PinGPT v2.0 — Full Guide</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "<b>🎴 Single Prompt Parameters:</b>\n"
        "<code>mood:</code> dark · melancholic · intense · serene · contemplative · defiant · vulnerable · exhausted · haunted · triumphant · restless · resigned · predatory · peaceful\n"
        "<code>setting:</code> gym · rain · rooftop · alley · warehouse · beach · train · parking · classroom · bar · apartment · hospital · temple · convenience_store\n"
        "<code>color:</code> cold_blue · sepia · monochrome · teal_orange · muted_green · blood_red\n"
        "<code>time:</code> golden_hour · blue_hour · midnight · overcast_dawn · 3am · neon_midnight · pre_storm · eclipse · hospital_fluorescent\n"
        "<code>outfit:</code> streetwear · formal · shirtless · gym_wear · combat · rain_gear · post_fight · winter · traditional\n"
        "<code>weather:</code> rain · snow · fog · wind · cherry_blossoms · embers · drizzle · fireflies\n"
        "<code>text:</code> yes / no (Japanese typography)\n\n"
        "<b>🎬 TikTok Slideshow:</b>\n"
        "<code>/tiktok Toji</code> — 10 slides with viral pacing\n"
        "<code>/tiktok</code> — Random character, 10 slides\n\n"
        "<b>🎴 Pinterest Series:</b>\n"
        "<code>/series Levi 3</code> — 3 connected story-arc prompts\n"
        "<code>/series 5</code> — Random character, 5 prompts\n\n"
        "<b>📋 Examples:</b>\n"
        "<code>/pingpt Eren mood:intense setting:rooftop</code>\n"
        "<code>/tiktok Gojo</code>\n"
        "<code>/series Toji 4</code>\n\n"
        "💡 <i>All parameters are auto-randomized if not specified!</i>"
    ))


def cmd_characters(token, cid):
    tier1 = CHARACTERS[:6]
    tier2 = CHARACTERS[6:]
    lines = ["🎴 <b>Character Roster</b>\n", "<b>⭐ Tier 1:</b>"]
    lines += [f"  • {c}" for c in tier1]
    lines += ["\n<b>🔥 Tier 2:</b>"]
    lines += [f"  • {c}" for c in tier2]
    lines.append("\n💡 <i>You can use any character name, even unlisted ones!</i>")
    tg_send(token, cid, "\n".join(lines))


def cmd_pingpt(token, cid, args_text, api_keys):
    skill = load_skill()
    if not skill:
        tg_send(token, cid, "❌ skill.md not found.")
        return
    tg_typing(token, cid)
    params = parse_args(args_text)
    # Pre-select random values for ALL unset params — prevents Gemini
    # from always defaulting to the first few entries in each dictionary
    if not params["character"]: params["character"] = random.choice(CHARACTERS)
    if not params["mood"]:      params["mood"] = random.choice(MOODS)
    if not params["setting"]:   params["setting"] = random.choice(SETTINGS)
    if not params["color"]:     params["color"] = random.choice(COLORS)
    if not params["time"]:      params["time"] = random.choice(TIMES)
    if not params["outfit"]:    params["outfit"] = random.choice(OUTFITS)
    if not params["lighting"]:  params["lighting"] = random.choice(LIGHTING)
    if not params["style"]:     params["style"] = random.choice(ART_STYLES)
    # Weather ~50% of the time per skill rules
    if not params["weather"] and random.random() < 0.5:
        params["weather"] = random.choice(WEATHER)
    try:
        prompt = call_gemini(api_keys, skill, build_instruction(params))
    except Exception as e:
        tg_send(token, cid, f"❌ API error: {str(e)[:200]}")
        return
    char_display = params["character"]
    mood_display = params["mood"]
    tg_send(token, cid, (
        "🎴 <b>PinGPT Prompt:</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"<code>{prompt}</code>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        f"📋 <b>Character:</b> {char_display} | <b>Mood:</b> {mood_display}\n\n"
        "💡 <i>Copy ↑ → paste into Gemini Chat!</i>"
    ))
    # Generate and send captions as a separate message
    captions = generate_captions(api_keys, prompt)
    send_captions(token, cid, captions)


def cmd_custom(token, cid, args_text, api_keys):
    """Custom character — user types any name."""
    if not args_text:
        tg_send(token, cid, (
            "✏️ <b>Custom Character</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Type any anime character name after /custom:\n\n"
            "<code>/custom Roronoa Zoro</code>\n"
            "<code>/custom Kaneki Ken mood:dark</code>\n"
            "<code>/custom Itachi Uchiha setting:rain</code>\n"
            "<code>/custom Guts mood:intense</code>\n\n"
            "💡 <i>I'll research their appearance and generate an accurate prompt!</i>"
        ))
        return
    cmd_pingpt(token, cid, args_text, api_keys)


def cmd_discover(token, cid, api_keys):
    """Trending character discovery — Gemini picks a popular character."""
    skill = load_skill()
    if not skill:
        tg_send(token, cid, "❌ skill.md not found.")
        return
    tg_send(token, cid, "🔍 Searching for a trending anime character... ⏳")
    tg_typing(token, cid)
    params = parse_args("")
    try:
        prompt = call_gemini(api_keys, skill, build_instruction(params, discover=True))
    except Exception as e:
        tg_send(token, cid, f"❌ API error: {str(e)[:200]}")
        return
    tg_send(token, cid, (
        "🔍 <b>PinGPT Discover — Trending Character:</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"<code>{prompt}</code>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "💡 <i>Copy ↑ → paste into Gemini Chat!</i>"
    ))


def cmd_batch(token, cid, args_text, api_keys):
    parts = (args_text or "").strip().split(None, 1)
    count, rest = 3, ""
    if parts:
        try:
            count = int(parts[0])
            rest = parts[1] if len(parts) > 1 else ""
        except ValueError:
            rest = args_text or ""
    count = max(1, min(count, 5))

    skill = load_skill()
    if not skill:
        tg_send(token, cid, "❌ skill.md not found.")
        return

    tg_send(token, cid, f"🎴 Generating {count} prompts... ⏳")
    params = parse_args(rest)

    original_params = parse_args(rest)
    for i in range(count):
        tg_typing(token, cid)
        # Randomize ALL unset params per-prompt for maximum variety
        if not original_params["character"]: params["character"] = random.choice(CHARACTERS)
        if not original_params["mood"]:      params["mood"] = random.choice(MOODS)
        if not original_params["setting"]:   params["setting"] = random.choice(SETTINGS)
        if not original_params["color"]:     params["color"] = random.choice(COLORS)
        if not original_params["time"]:      params["time"] = random.choice(TIMES)
        if not original_params["outfit"]:    params["outfit"] = random.choice(OUTFITS)
        if not original_params["lighting"]:  params["lighting"] = random.choice(LIGHTING)
        if not original_params["style"]:     params["style"] = random.choice(ART_STYLES)
        if not original_params["weather"]:
            params["weather"] = random.choice(WEATHER) if random.random() < 0.5 else None
        try:
            prompt = call_gemini(api_keys, skill, build_instruction(params))
            tg_send(token, cid, f"🎴 <b>[{i+1}/{count}]</b>\n\n<code>{prompt}</code>")
        except Exception as e:
            tg_send(token, cid, f"❌ [{i+1}/{count}] Error: {str(e)[:150]}")

    tg_send(token, cid, f"✅ Done! {count} prompts generated.")


def cmd_tiktok(token, cid, args_text, api_keys):
    """TikTok 10-slide carousel with viral pacing."""
    skill = load_skill()
    if not skill:
        tg_send(token, cid, "❌ skill.md not found.")
        return

    # Parse character name (or pick random)
    parts = (args_text or "").strip().split()
    if parts:
        name = " ".join(parts)
        character = next((c for c in CHARACTERS if name.lower() in c.lower()), name)
    else:
        character = random.choice(CHARACTERS)

    tg_send(token, cid, f"🎬 Generating 10-slide TikTok carousel for <b>{character}</b>... ⏳\n\n<i>This takes a moment — building viral pacing structure.</i>")
    tg_typing(token, cid)

    instruction = build_tiktok_instruction(character)
    try:
        raw = call_gemini(api_keys, skill, instruction)
    except Exception as e:
        tg_send(token, cid, f"❌ API error: {str(e)[:200]}")
        return

    slides, captions = parse_tiktok_output(raw)

    # Send each slide as a separate message for easy copy-paste
    for i, slide in enumerate(slides):
        if i < len(SLIDE_LABELS):
            emoji, label = SLIDE_LABELS[i]
        else:
            emoji, label = "🎴", f"SLIDE {i+1}"
        title = slide.get("title", "")
        prompt = slide.get("prompt", "")
        if not prompt:
            continue
        tg_send(token, cid, (
            f"{emoji} <b>[{i+1}/10] {label}</b> — {title}\n"
            f"━━━━━━━━━━━━━━━━━━\n\n"
            f"<code>{prompt}</code>"
        ))

    # Send TikTok captions + tags + sound
    caption_lines = ["\n🎵 <b>TikTok Caption \u0026 Tags:</b>", "━━━━━━━━━━━━━━━━━━"]
    if captions.get("caption"):
        caption_lines.append(f"{captions['caption']}")
    if captions.get("tags"):
        caption_lines.append(f"\n<code>{captions['tags']}</code>")
    if captions.get("sound"):
        caption_lines.append(f"\n🎧 <b>Suggested audio:</b> {captions['sound']}")
    else:
        caption_lines.append(f"\n🎧 <b>Suggested audio:</b> {random.choice(TIKTOK_SOUNDS)}")
    caption_lines.append("\n✅ Done! 10 slides ready for TikTok.")
    tg_send(token, cid, "\n".join(caption_lines))


def cmd_series(token, cid, args_text, api_keys):
    """Pinterest series — connected story-arc prompts."""
    skill = load_skill()
    if not skill:
        tg_send(token, cid, "❌ skill.md not found.")
        return

    # Parse: /series Levi 3  or  /series 5  or  /series
    parts = (args_text or "").strip().split()
    count = 3  # default
    character = None

    if parts:
        # Check if last arg is a number (count)
        try:
            count = int(parts[-1])
            name_parts = parts[:-1]
        except ValueError:
            name_parts = parts
        if name_parts:
            name = " ".join(name_parts)
            character = next((c for c in CHARACTERS if name.lower() in c.lower()), name)

    if not character:
        character = random.choice(CHARACTERS)

    count = max(2, min(count, 5))  # clamp 2-5

    tg_send(token, cid, f"🎴 Generating {count}-part Pinterest series for <b>{character}</b>... ⏳")
    tg_typing(token, cid)

    instruction = build_series_instruction(character, count)
    try:
        raw = call_gemini(api_keys, skill, instruction)
    except Exception as e:
        tg_send(token, cid, f"❌ API error: {str(e)[:200]}")
        return

    prompts, captions = parse_series_output(raw, count)

    # Send header
    tg_send(token, cid, f"🎴 <b>PinGPT Series: {character} — {count} Images</b>\n━━━━━━━━━━━━━━━━━━")

    # Send each prompt
    for i, item in enumerate(prompts):
        title = item.get("title", "")
        prompt = item.get("prompt", "")
        if not prompt:
            continue
        tg_send(token, cid, (
            f"🎴 <b>[{i+1}/{count}]</b> — {title}\n\n"
            f"<code>{prompt}</code>"
        ))

    # Send captions
    cap_lines = ["━━━━━━━━━━━━━━━━━━"]
    if captions.get("pin_caption"):
        cap_lines.append(f"📌 <b>Pinterest:</b> {captions['pin_caption']}")
    if captions.get("pin_tags"):
        cap_lines.append(f"<code>{captions['pin_tags']}</code>")
    if captions.get("tik_caption"):
        cap_lines.append(f"\n🎵 <b>TikTok:</b> {captions['tik_caption']}")
    if captions.get("tik_tags"):
        cap_lines.append(f"<code>{captions['tik_tags']}</code>")
    cap_lines.append(f"\n✅ Done! {count}-part series generated.")
    tg_send(token, cid, "\n".join(cap_lines))


def cmd_crop_help(token, cid):
    tg_send(token, cid, (
        "✂️ <b>Auto-Crop Watermark</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Send me any image and I'll automatically crop the bottom 3% "
        "to remove the NanoBanana 2 watermark.\n\n"
        "<b>How to use:</b>\n"
        "• Just send/forward an image to this chat\n"
        "• Or reply to an image with /crop\n\n"
        "💡 <i>Works best with 9:16 portrait images from Gemini Chat.</i>"
    ))


def handle_photo(token, cid, photo_list, msg_id):
    """Download the largest photo, crop bottom 3%, send it back."""
    import urllib.request
    import io

    tg_typing(token, cid)

    # Get the highest-resolution version (last in the array)
    file_id = photo_list[-1]["file_id"]

    # Step 1: Get file path from Telegram
    try:
        url = f"https://api.telegram.org/bot{token}/getFile"
        payload = json.dumps({"file_id": file_id}).encode()
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        resp = urllib.request.urlopen(req)
        file_info = json.loads(resp.read())
        file_path = file_info["result"]["file_path"]
    except Exception as e:
        logger.error(f"getFile error: {e}")
        tg_send(token, cid, "❌ Could not download image.")
        return

    # Step 2: Download the image
    try:
        dl_url = f"https://api.telegram.org/file/bot{token}/{file_path}"
        resp = urllib.request.urlopen(dl_url)
        image_data = resp.read()
    except Exception as e:
        logger.error(f"Download error: {e}")
        tg_send(token, cid, "❌ Could not download image.")
        return

    # Step 3: Crop bottom 3% using Pillow
    try:
        from PIL import Image
        img = Image.open(io.BytesIO(image_data))
        w, h = img.size
        crop_px = int(h * 0.03)
        cropped = img.crop((0, 0, w, h - crop_px))

        # Save to bytes
        buf = io.BytesIO()
        cropped.save(buf, format="PNG")
        buf.seek(0)
    except Exception as e:
        logger.error(f"Crop error: {e}")
        tg_send(token, cid, "❌ Could not process image. Make sure Pillow is installed.")
        return

    # Step 4: Send cropped image back via multipart upload
    try:
        boundary = "----PinGPTBoundary"
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="chat_id"\r\n\r\n{cid}\r\n'
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="caption"\r\n\r\n'
            f"✂️ Watermark cropped! (removed bottom {crop_px}px / 3%)\r\n"
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="reply_to_message_id"\r\n\r\n{msg_id}\r\n'
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="photo"; filename="cropped.png"\r\n'
            f"Content-Type: image/png\r\n\r\n"
        ).encode()
        body += buf.read()
        body += f"\r\n--{boundary}--\r\n".encode()

        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendPhoto",
            data=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        )
        urllib.request.urlopen(req)
    except Exception as e:
        logger.error(f"Send photo error: {e}")
        tg_send(token, cid, "❌ Could not send cropped image.")


def register_menu(token):
    """Register bot commands menu with Telegram (called once on /start)."""
    import urllib.request
    commands = [
        {"command": "pingpt", "description": "🎴 Generate a single prompt"},
        {"command": "custom", "description": "✏️ Any anime character"},
        {"command": "discover", "description": "🔍 Trending character pick"},
        {"command": "tiktok", "description": "🎬 10-slide TikTok slideshow"},
        {"command": "series", "description": "🎴 Pinterest story-arc series"},
        {"command": "batch", "description": "📦 Rapid bulk generation"},
        {"command": "characters", "description": "👥 Character roster + tiers"},
        {"command": "help", "description": "📖 Parameters, examples, tips"},
        {"command": "crop", "description": "✂️ Remove watermark"},
    ]
    try:
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/setMyCommands",
            data=json.dumps({"commands": commands}).encode(),
            headers={"Content-Type": "application/json"},
        )
        urllib.request.urlopen(req, timeout=3)
    except Exception:
        pass  # Non-critical, menu will still work on next /start


# ─── Flask App ────────────────────────────────────────────────────────────────

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return "🎴 PinGPT Bot is running!"


@app.route("/api/webhook", methods=["POST"])
def webhook():
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    api_keys_str = os.environ.get("GEMINI_API_KEYS", os.environ.get("GEMINI_API_KEY", ""))
    api_keys = [k.strip() for k in api_keys_str.split(",") if k.strip()]

    if not token or not api_keys:
        return Response("Missing env vars", status=500)

    update = request.get_json(force=True) or {}
    msg = update.get("message", {})
    text = msg.get("text", "")
    cid = msg.get("chat", {}).get("id")
    msg_id = msg.get("message_id")
    photo = msg.get("photo")

    if not cid:
        return Response("OK", status=200)

    # Handle photo messages — auto-crop
    if photo:
        handle_photo(token, cid, photo, msg_id)
        return Response("OK", status=200)

    # Handle /crop on a reply
    if text.startswith("/crop"):
        reply = msg.get("reply_to_message", {})
        reply_photo = reply.get("photo")
        if reply_photo:
            handle_photo(token, cid, reply_photo, reply.get("message_id", msg_id))
        else:
            cmd_crop_help(token, cid)
        return Response("OK", status=200)

    if not text:
        return Response("OK", status=200)

    # Route commands
    cmd = text.split()[0].lower() if text.startswith("/") else None
    args = text.split(None, 1)[1] if len(text.split(None, 1)) > 1 else ""

    if cmd == "/start":
        register_menu(token)
        cmd_start(token, cid)
    elif cmd == "/help":
        cmd_help(token, cid)
    elif cmd == "/characters":
        cmd_characters(token, cid)
    elif cmd == "/custom":
        cmd_custom(token, cid, args, api_keys)
    elif cmd == "/discover":
        cmd_discover(token, cid, api_keys)
    elif cmd == "/tiktok":
        cmd_tiktok(token, cid, args, api_keys)
    elif cmd == "/series":
        cmd_series(token, cid, args, api_keys)
    elif cmd == "/batch":
        cmd_batch(token, cid, args, api_keys)
    elif cmd == "/pingpt":
        cmd_pingpt(token, cid, args, api_keys)
    elif not text.startswith("/"):
        # Treat plain text as /pingpt
        cmd_pingpt(token, cid, text, api_keys)

    return Response("OK", status=200)


# Local dev server
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / ".env")
    app.run(port=5000, debug=True)
