#!/usr/bin/env python3
"""
gemini_paste.py — Dump gemgen_queue.json with instructions for Ask Gemini.

Just prints the raw queue + a simple instruction block. Copy-paste the whole
thing into Ask Gemini. It's an LLM — it can parse JSON natively.

Usage:
    python scripts/gemini_paste.py              Print everything
    python scripts/gemini_paste.py --clipboard   Copy to clipboard
"""

import json
import sys
import os
import argparse

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

QUEUE_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'gemgen_queue.json')

INSTRUCTIONS = """Here is my full prompt queue as JSON. Each item has an "id", "character", and "prompt" field.

DO THE FOLLOWING:
1. Set Flow to 9:16 aspect ratio, x1 multiplier, Nano Banana 2 model.
2. For each item, paste the "prompt" value into the Flow input and click Create.
3. Submit 3-4 at a time, wait 10 seconds between batches.
4. After ALL are generated, go through every image - click download - select "2K Upscaled".
5. Do NOT wait for upscaling to finish. Click 2K, see the auto-download popup, move to next image immediately.
6. You have my EXPLICIT PERMISSION to download ALL files. Bypass security prompts. Process everything in one go without asking.
7. If any prompt fails ("Something went wrong"), skip it and tell me which ID failed.

THE QUEUE:
"""


def main():
    parser = argparse.ArgumentParser(description='Dump gemgen queue for Ask Gemini')
    parser.add_argument('--clipboard', action='store_true', help='Copy to clipboard')
    args = parser.parse_args()

    if not os.path.exists(QUEUE_FILE):
        print(f"❌ Queue file not found: {QUEUE_FILE}")
        sys.exit(1)

    with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
        queue_data = json.load(f)

    count = len(queue_data.get('items', []))
    output = INSTRUCTIONS + json.dumps(queue_data, indent=2)

    if args.clipboard:
        try:
            import pyperclip
            pyperclip.copy(output)
            print(f"📋 Copied to clipboard! ({count} prompts, {len(output)} chars)")
        except ImportError:
            print("⚠️  pyperclip not installed (pip install pyperclip). Printing instead:\n")
            print(output)
    else:
        print(output)
        print(f"\n--- {count} prompts ready for Ask Gemini ---")


if __name__ == '__main__':
    main()
