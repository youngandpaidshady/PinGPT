"""
Test upgraded pipeline: 5 Gojo prompts with all new systems.
- Scene seed injection
- Emotional arc sequencing
- Anti-repetition memory
- Self-critique loop
"""
import os
import time
from pathlib import Path
from google import genai
from dotenv import load_dotenv

import generate

def run():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("No API key")
        return
    client = genai.Client(api_key=api_key)
    skill_text = generate.SKILL_FILE.read_text(encoding="utf-8")
    scene_seeds = generate.load_scene_seeds()

    print(f"  ✓ Loaded {len(scene_seeds)} scene seeds")

    character = "Satoru Gojo"
    total = 5

    # Generate emotional arc
    beats = generate.generate_emotional_arc(client, character, total)

    # Anti-repetition memory
    batch_memory = {
        "outfits": [], "shadow_colors": [], "palettes": [],
        "expressions": [], "templates": [], "accessory_states": [], "environments": [],
    }

    used_seeds = set()
    results = []

    for i in range(total):
        print(f"\n  ═══ [{i+1}/{total}] ═══")

        # Scene seed
        seed = generate.get_random_scene_seed(scene_seeds, used_seeds)
        if seed:
            used_seeds.add(seed)
            print(f"  🎲  Seed: {seed[:60]}")

        import argparse
        args = argparse.Namespace(
            character=character, mood=None, setting=None, color=None,
            time=None, weather=None, outfit=None, text=False, discover=False,
        )

        user_instruction = generate.build_user_instruction(
            args, scene_seed=seed, batch_memory=batch_memory, emotional_beat=beats[i],
        )

        prompt = generate.generate_prompt(client, skill_text, user_instruction)
        prompt = generate.critique_prompt(client, prompt, skill_text)

        word_count = len(prompt.split())
        results.append((i+1, seed[:40] if seed else "none", prompt, word_count))

        # Update memory
        elements = generate.extract_used_elements(prompt)
        for key in ["outfit", "shadow_color", "palette", "expression", "template", "environment"]:
            if elements.get(key):
                mem_key = key + "s" if not key.endswith("s") else key
                if mem_key == "shadow_colors":
                    mem_key = "shadow_colors"
                elif mem_key == "expressions":
                    mem_key = "expressions"
                elif mem_key == "palettes":
                    mem_key = "palettes"
                elif mem_key == "templates":
                    mem_key = "templates"
                elif mem_key == "outfits":
                    mem_key = "outfits"
                elif mem_key == "environments":
                    mem_key = "environments"
                if mem_key in batch_memory:
                    batch_memory[mem_key].append(elements[key])

        if i < total - 1:
            time.sleep(2)

    # Write results
    with open("gojo_upgraded_output.txt", "w", encoding="utf-8") as f:
        for num, seed, prompt, wc in results:
            f.write(f"=== GOJO #{num} — Seed: {seed} ({wc} words) ===\n")
            f.write(prompt + "\n\n")

        f.write("\n=== ANTI-REPETITION MEMORY STATE ===\n")
        for key, vals in batch_memory.items():
            f.write(f"  {key}: {vals}\n")

    print(f"\n  ✅ DONE — 5 upgraded Gojo prompts → gojo_upgraded_output.txt")

if __name__ == "__main__":
    run()
