"""
Generate 5 Gojo prompts using the actual Gemini model pipeline.
Saves raw prompts to gojo_model_output.txt for comparison.
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

    # 5 different Gojo prompts — varying settings to test scene intelligence
    configs = [
        {"label": "GOJO #1 — No constraints (pure engine freedom)", "character": "Satoru Gojo", "mood": None, "setting": None, "color": None, "time": None, "weather": None, "outfit": None},
        {"label": "GOJO #2 — No constraints (pure engine freedom)", "character": "Satoru Gojo", "mood": None, "setting": None, "color": None, "time": None, "weather": None, "outfit": None},
        {"label": "GOJO #3 — No constraints (pure engine freedom)", "character": "Satoru Gojo", "mood": None, "setting": None, "color": None, "time": None, "weather": None, "outfit": None},
        {"label": "GOJO #4 — No constraints (pure engine freedom)", "character": "Satoru Gojo", "mood": None, "setting": None, "color": None, "time": None, "weather": None, "outfit": None},
        {"label": "GOJO #5 — No constraints (pure engine freedom)", "character": "Satoru Gojo", "mood": None, "setting": None, "color": None, "time": None, "weather": None, "outfit": None},
    ]

    results = []
    for i, cfg in enumerate(configs):
        print(f"\n  [{i+1}/5] Generating: {cfg['label']}")

        class Args:
            character = cfg["character"]
            mood = cfg["mood"]
            setting = cfg["setting"]
            color = cfg["color"]
            time = cfg["time"]
            weather = cfg["weather"]
            outfit = cfg["outfit"]
            text = False
            discover = False

        user_instruction = generate.build_user_instruction(Args())
        # Add diversity instruction for batch
        user_instruction += f"\n\nThis is prompt {i+1} of 5 in a batch. Each prompt MUST have a completely different scene, environment, outfit, palette, and mood from the others. Apply the Virality Injection Rules and Scene Intelligence Spawner. Generate a unique cinematic micro-story."
        
        prompt = generate.generate_prompt(client, skill_text, user_instruction)
        word_count = len(prompt.split())
        results.append((cfg["label"], prompt, word_count))
        
        if i < len(configs) - 1:
            time.sleep(2)

    # Write results
    with open("gojo_model_output.txt", "w", encoding="utf-8") as f:
        for label, prompt, wc in results:
            f.write(f"=== {label} ({wc} words) ===\n")
            f.write(prompt + "\n\n")
    
    print(f"\n  ✅ DONE — 5 model-generated Gojo prompts → gojo_model_output.txt")

if __name__ == "__main__":
    run()
