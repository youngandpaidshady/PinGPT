#!/usr/bin/env python3
"""
PinGPT — Pinterest-Aesthetic Anime Image Generator
Uses Gemini API (Nano Banana 2) to generate watermark-free 4K anime images.

Usage:
    python generate.py                     # Interactive menu
    python generate.py --character "Toji"  # Direct CLI mode
    python generate.py --batch 3           # Batch mode
    python generate.py --series "Levi" 3   # Series mode
"""

import os
import sys
import argparse
import base64
import time
from pathlib import Path
from datetime import datetime

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("\n❌ Missing dependency: google-genai")
    print("   Run: pip install -r requirements.txt\n")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("\n❌ Missing dependency: python-dotenv")
    print("   Run: pip install -r requirements.txt\n")
    sys.exit(1)


# ─── Configuration ────────────────────────────────────────────────────────────

PROMPT_MODEL = "gemini-2.5-flash"
IMAGE_MODEL = "gemini-3.1-flash-image-preview"       # Nano Banana 2
ASPECT_RATIO = "9:16"
IMAGE_SIZE = "4K"
OUTPUT_DIR = Path(__file__).parent / "output"
SKILL_FILE = Path(__file__).parent / "skill.md"

# ─── Character & Option Lists (for interactive menu) ─────────────────────────

CHARACTERS = [
    "Toji Fushiguro", "Satoru Gojo", "Eren Yeager", "Levi Ackerman",
    "Baki Hanma", "Yuji Itadori", "Aqua Hoshino", "Rin Itoshi",
    "Megumi Fushiguro", "Shoto Todoroki", "Loid Forger", "Killua Zoldyck",
    "Sebastian Michaelis", "Jinshi", "Izuku Midoriya", "Sung Jinwoo",
]

MOODS = ["dark", "melancholic", "intense", "serene"]

SETTINGS = [
    "dark gym", "rainy night tokyo", "abandoned warehouse", "sunset soccer field",
    "rooftop at night", "dark alley", "locker room", "foggy waterfront",
    "empty train platform", "boxing gym", "liminal hallway", "mountain cliff edge",
    "underground parking", "night beach",
]

COLORS = [
    "desaturated cool", "cold blue", "warm sepia",
    "monochrome b&w", "teal & orange", "muted green", "blood red accent",
]

TIMES = ["golden hour", "blue hour", "midnight", "overcast dawn", "3am fluorescent"]

OUTFITS = [
    "gym wear", "streetwear", "shirtless training", "clean formal",
    "dark minimalist", "casual relaxed", "combat ready", "rain gear",
    "athletic jersey", "post-fight", "layered winter", "traditional japanese",
]


# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_api_key():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("\n╔═══════════════════════════════════════════════╗")
        print("║  ❌  No API key found                         ║")
        print("╠═══════════════════════════════════════════════╣")
        print("║  1. Get your key from:                       ║")
        print("║     https://aistudio.google.com/apikey        ║")
        print("║  2. Copy .env.example → .env                 ║")
        print("║  3. Paste your key in .env                   ║")
        print("╚═══════════════════════════════════════════════╝\n")
        sys.exit(1)
    return api_key


def load_skill():
    if not SKILL_FILE.exists():
        print(f"❌ skill.md not found at {SKILL_FILE}")
        sys.exit(1)
    return SKILL_FILE.read_text(encoding="utf-8")


def print_header():
    print()
    print("╔═══════════════════════════════════════════════╗")
    print("║          🎴  P i n G P T  v2.0               ║")
    print("║     Pinterest Anime Aesthetic Generator       ║")
    print("║     Nano Banana 2 · 4K · 9:16 Portrait       ║")
    print("╚═══════════════════════════════════════════════╝")
    print()


def pick_from_menu(title, options, allow_random=True, allow_skip=False):
    """Display a numbered menu and return the user's choice."""
    print(f"\n  ┌─ {title}")
    print(  "  │")

    for i, option in enumerate(options, 1):
        print(f"  │  [{i:2d}]  {option}")

    extras = []
    if allow_random:
        extras.append("[0] 🎲 Random")
    if allow_skip:
        extras.append("[S] Skip")

    if extras:
        print(f"  │")
        print(f"  │  {' · '.join(extras)}")

    print(  "  │")

    while True:
        choice = input("  └─▶ ").strip().lower()

        if allow_skip and choice == "s":
            return None
        if allow_random and choice == "0":
            return "random"
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return options[idx]
        except ValueError:
            pass
        print(f"  │  ⚠ Enter 1-{len(options)}" +
              (", 0 for random" if allow_random else "") +
              (", or S to skip" if allow_skip else ""))


def pick_yes_no(prompt_text):
    """Simple yes/no prompt."""
    while True:
        choice = input(f"  └─▶ {prompt_text} (y/n): ").strip().lower()
        if choice in ("y", "yes"):
            return True
        if choice in ("n", "no"):
            return False


def interactive_mode():
    """Run the full interactive menu flow."""
    print("  ┌─────────────────────────────────────────────┐")
    print("  │  What would you like to generate?           │")
    print("  │                                             │")
    print("  │  [1]  🎴  Single Image                      │")
    print("  │  [2]  📦  Batch (multiple images)           │")
    print("  │  [3]  🎬  Series (character story arc)      │")
    print("  │  [4]  🔍  Discover (trending character)     │")
    print("  │                                             │")
    print("  └─────────────────────────────────────────────┘")

    while True:
        mode = input("  ▶ Choose mode [1-4]: ").strip()
        if mode in ("1", "2", "3", "4"):
            break
        print("    ⚠ Enter 1, 2, 3, or 4")

    # Common: pick character
    character = pick_from_menu("Choose Character", CHARACTERS)

    # For series, get count
    count = 1
    if mode == "2":
        while True:
            try:
                count = int(input("\n  ▶ How many images? [1-10]: ").strip())
                if 1 <= count <= 10:
                    break
            except ValueError:
                pass
            print("    ⚠ Enter a number between 1 and 10")
    elif mode == "3":
        while True:
            try:
                count = int(input("\n  ▶ How many in series? [2-5]: ").strip())
                if 2 <= count <= 5:
                    break
            except ValueError:
                pass
            print("    ⚠ Enter a number between 2 and 5")

    # Optional customizations
    mood = pick_from_menu("Choose Mood", MOODS, allow_skip=True)
    setting = pick_from_menu("Choose Setting", SETTINGS, allow_skip=True)
    color = pick_from_menu("Choose Color Grade", COLORS, allow_skip=True)
    time_of_day = pick_from_menu("Choose Time of Day", TIMES, allow_skip=True)
    outfit = pick_from_menu("Choose Outfit", OUTFITS, allow_skip=True)

    print(f"\n  ┌─ Include Japanese Typography?")
    include_text = pick_yes_no("Add text overlay?")

    # Build args namespace
    args = argparse.Namespace(
        character=character if character != "random" else None,
        mood=mood if mood and mood != "random" else None,
        setting=setting if setting and setting != "random" else None,
        color=color if color and color != "random" else None,
        time=time_of_day if time_of_day and time_of_day != "random" else None,
        weather=None,
        outfit=outfit if outfit and outfit != "random" else None,
        text=include_text,
        batch=count if mode == "2" else 1,
        series=character if mode == "3" and character != "random" else (None if mode != "3" else None),
        count=count,
        discover=mode == "4",
    )

    # Show summary
    print("\n  ╔═══════════════════════════════════════════════╗")
    print("  ║  📋  Generation Summary                      ║")
    print("  ╠═══════════════════════════════════════════════╣")
    print(f"  ║  Mode:      {'Series' if mode == '3' else 'Batch' if mode == '2' else 'Discover' if mode == '4' else 'Single':30s}  ║")
    print(f"  ║  Character: {(args.character or '🎲 Random'):30s}  ║")
    print(f"  ║  Mood:      {(args.mood or '🎲 Random'):30s}  ║")
    print(f"  ║  Setting:   {(args.setting or '🎲 Random'):30s}  ║")
    print(f"  ║  Color:     {(args.color or '🎲 Random'):30s}  ║")
    print(f"  ║  Time:      {(args.time or '🎲 Random'):30s}  ║")
    print(f"  ║  Outfit:    {(args.outfit or '🎲 Random'):30s}  ║")
    print(f"  ║  Text:      {'Yes' if args.text else 'No':30s}  ║")
    print(f"  ║  Count:     {count:30d}  ║")
    print("  ╚═══════════════════════════════════════════════╝")
    print()

    if not pick_yes_no("Proceed?"):
        print("\n  Cancelled.\n")
        sys.exit(0)

    return args, mode


# ─── Core Pipeline ────────────────────────────────────────────────────────────

def build_user_instruction(args):
    parts = ["Generate a single PinGPT prompt following all the rules in the skill file."]

    if args.character:
        parts.append(f"Character: {args.character}")
    if args.mood:
        parts.append(f"Mood: {args.mood}")
    if args.setting:
        parts.append(f"Setting/Environment: {args.setting}")
    if args.color:
        parts.append(f"Color grade: {args.color}")
    if args.time:
        parts.append(f"Time of day: {args.time}")
    if args.weather:
        parts.append(f"Weather: {args.weather}")
    if args.outfit:
        parts.append(f"Outfit: {args.outfit}")
    if args.text:
        parts.append("Include Japanese typography overlay.")
    if args.discover:
        parts.append("Use web search to discover a currently trending anime character.")

    parts.append(
        "\nOutput ONLY the raw prompt text that will be sent to the image generator. "
        "No markdown formatting, no blockquotes, no metadata, no Pinterest tags. "
        "Just the pure natural language prompt text, nothing else."
    )

    return "\n".join(parts)


def generate_prompt(client, skill_text, user_instruction):
    print("  🧠  Generating prompt from skill.md...")

    response = client.models.generate_content(
        model=PROMPT_MODEL,
        contents=[
            {
                "role": "user",
                "parts": [{"text": f"You are PinGPT. Follow these instructions exactly:\n\n{skill_text}\n\n---\n\n{user_instruction}"}]
            }
        ],
    )

    prompt = response.text.strip()
    prompt = prompt.replace("```", "").replace("> ", "").strip()
    if prompt.startswith('"') and prompt.endswith('"'):
        prompt = prompt[1:-1]

    return prompt


def generate_image(client, prompt, index=0):
    print(f"  🎨  Generating 4K image...")

    try:
        response = client.models.generate_content(
            model=IMAGE_MODEL,
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_modalities=["Image"],
                image_config=types.ImageConfig(
                    aspect_ratio=ASPECT_RATIO,
                    image_size=IMAGE_SIZE,
                ),
            ),
        )
    except Exception as e:
        print(f"  ❌  API error: {e}")
        return None

    OUTPUT_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = f"_{index}" if index > 0 else ""
    filename = f"pingpt_{timestamp}{suffix}.png"
    filepath = OUTPUT_DIR / filename

    for part in response.parts:
        if part.inline_data is not None:
            try:
                image_bytes = base64.b64decode(part.inline_data.data)
            except Exception:
                image_bytes = part.inline_data.data
            filepath.write_bytes(image_bytes)
            print(f"  ✅  Saved: {filepath.name}")
            return filepath

    for part in response.parts:
        if hasattr(part, 'as_image'):
            image = part.as_image()
            image.save(str(filepath))
            print(f"  ✅  Saved: {filepath.name}")
            return filepath

    print("  ⚠️  No image generated — the model may have blocked the request.")
    if response.text:
        print(f"     Response: {response.text[:200]}")
    return None


def run_single(client, skill_text, args, index=0):
    user_instruction = build_user_instruction(args)
    prompt = generate_prompt(client, skill_text, user_instruction)

    print(f"  📝  Prompt preview: {prompt[:100]}...")
    print()

    filepath = generate_image(client, prompt, index)
    return prompt, filepath


def run_series(client, skill_text, character, count):
    print(f"\n  🎬  Series Mode: {character} — {count} images")
    print("  " + "━" * 45)

    series_instruction = (
        f"Generate a PinGPT series of {count} connected prompts for {character}. "
        f"Follow the Series Mode rules from the skill file exactly. "
        f"Output each prompt separated by the marker '---PROMPT---'. "
        f"Output ONLY the raw prompt texts, no metadata, no numbering, no markdown."
    )

    response = client.models.generate_content(
        model=PROMPT_MODEL,
        contents=[
            {
                "role": "user",
                "parts": [{"text": f"You are PinGPT. Follow these instructions exactly:\n\n{skill_text}\n\n---\n\n{series_instruction}"}]
            }
        ],
    )

    prompts = [p.strip() for p in response.text.split("---PROMPT---") if p.strip()]

    for i, prompt in enumerate(prompts):
        print(f"\n  [{i+1}/{len(prompts)}] Generating...")
        filepath = generate_image(client, prompt, i + 1)
        if filepath:
            print(f"       ↳ {filepath.name}")
        if i < len(prompts) - 1:
            time.sleep(1)

    print(f"\n  🎬  Series complete! {len(prompts)} images → {OUTPUT_DIR}/")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="PinGPT",
        description="🎴 Pinterest-Aesthetic Anime Image Generator (Nano Banana 2, 4K)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate.py                              Interactive menu
  python generate.py -c "Toji" -m dark             Toji, dark mood
  python generate.py -s gym --color cold_blue      Gym, cold blue palette
  python generate.py -b 3                          3 random images
  python generate.py --series "Levi" --count 3     Levi 3-image series
  python generate.py -d                            Discover trending character
        """
    )

    parser.add_argument("-c", "--character", help="Character name")
    parser.add_argument("-m", "--mood", help="Mood: dark, melancholic, intense, serene")
    parser.add_argument("-s", "--setting", help="Environment: gym, rain, rooftop, etc.")
    parser.add_argument("--color", help="Color grade: cold_blue, sepia, monochrome, etc.")
    parser.add_argument("-t", "--time", help="Time: golden_hour, midnight, blue_hour, etc.")
    parser.add_argument("-w", "--weather", help="Weather: rain, snow, fog, wind, etc.")
    parser.add_argument("-o", "--outfit", help="Outfit: streetwear, formal, shirtless, etc.")
    parser.add_argument("--text", action="store_true", help="Force typography overlay")
    parser.add_argument("-b", "--batch", type=int, default=1, help="Number of images")
    parser.add_argument("--series", help="Series mode — character name")
    parser.add_argument("--count", type=int, default=3, help="Images in series (default: 3)")
    parser.add_argument("-d", "--discover", action="store_true", help="Discover trending character")

    args = parser.parse_args()

    print_header()

    # If no arguments provided, launch interactive mode
    has_args = any([
        args.character, args.mood, args.setting, args.color,
        args.time, args.weather, args.outfit, args.text,
        args.batch > 1, args.series, args.discover
    ])

    if not has_args:
        args, mode = interactive_mode()
    else:
        mode = "3" if args.series else ("2" if args.batch > 1 else "1")

    # Setup
    api_key = load_api_key()
    client = genai.Client(api_key=api_key)
    skill_text = load_skill()

    print(f"\n  ✓ API connected ({IMAGE_MODEL})")
    print(f"  ✓ Resolution: {IMAGE_SIZE} @ {ASPECT_RATIO}")
    print(f"  ✓ Output → {OUTPUT_DIR}/\n")

    # Execute
    if mode == "3" and args.series:
        run_series(client, skill_text, args.series, args.count)
    else:
        total = args.batch
        for i in range(total):
            if total > 1:
                print(f"\n  ─── Image {i+1}/{total} ───")
            run_single(client, skill_text, args, i)
            if i < total - 1:
                time.sleep(1)
        print(f"\n  🎴  Done! {total} image(s) → {OUTPUT_DIR}/\n")


if __name__ == "__main__":
    main()
