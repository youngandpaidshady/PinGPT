import os
from pathlib import Path
from google import genai
from dotenv import load_dotenv

import generate

def run_test():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("No API key")
        return
    client = genai.Client(api_key=api_key)
    skill_text = generate.SKILL_FILE.read_text(encoding="utf-8")
    
    # Test 1: Warm cozy (Nanami in a cafe — new character, Soft Pack)
    class Args1:
        character = "Nanami Kento"
        mood = "serene"
        setting = "rainy cafe window"
        color = "golden amber"
        time = "blue hour"
        weather = None
        outfit = None
        text = False
        discover = False

    # Test 2: Neon bleed (Toji in subway — Heat Pack)
    class Args2:
        character = "Toji Fushiguro"
        mood = "intense"
        setting = "subway car empty"
        color = "neon bleed"
        time = "midnight"
        weather = None
        outfit = None
        text = False
        discover = False

    # Test 3: Emotional tension (Levi — soft moment, Dark Academia)
    class Args3:
        character = "Levi Ackerman"
        mood = None
        setting = "empty classroom"
        color = None
        time = None
        weather = None
        outfit = "casual relaxed"
        text = False
        discover = False

    tests = [
        ("WARM COZY — Nanami cafe", Args1()),
        ("NEON BLEED — Toji subway", Args2()),
        ("EMOTIONAL TENSION — Levi classroom", Args3()),
    ]

    results = []
    for label, args in tests:
        user_instruction = generate.build_user_instruction(args)
        prompt = generate.generate_prompt(client, skill_text, user_instruction)
        word_count = len(prompt.split())
        results.append((label, prompt, word_count))

    with open("prompt_out.txt", "w", encoding="utf-8") as f:
        for label, prompt, wc in results:
            f.write(f"=== {label} ({wc} words) ===\n")
            f.write(prompt + "\n\n")
    
    print("DONE — 3 test prompts written to prompt_out.txt")

if __name__ == "__main__":
    run_test()
