"""
affiliate_linker.py — Scan gemgen_queue.json for products and generate Amazon affiliate links.

Usage:
    python scripts/affiliate_linker.py                  # Scan and inject links
    python scripts/affiliate_linker.py --dry-run        # Preview without writing

Reads prompts + descriptions, extracts the most linkable product per pin,
generates Amazon search URLs with the Associate tag.
"""

import json
import os
import re
import sys
import urllib.parse

BASE_DIR = r"C:\Users\Administrator\Desktop\PinGPT"
QUEUE_FILE = os.path.join(BASE_DIR, "gemgen_queue.json")
ASSOCIATE_TAG = "pingptbyxo-20"

# ── Product Detection ──────────────────────────────────────────────────────
# Maps keywords found in prompts/descriptions to Amazon search queries.
# Priority: first match wins. Order = most specific → most generic.
PRODUCT_MAP = [
    # Electronics
    (["rgb keyboard", "mechanical keyboard", "keyboard"],       "RGB mechanical keyboard anime gaming"),
    (["over-ear headphones", "headphones around neck"],         "over ear headphones black wireless"),
    (["earphone", "earphones", "earbud", "earbuds"],           "wired earphones black"),
    (["phone", "phone glow", "phone screen"],                  "phone stand desk minimalist black"),
    (["monitor", "screen glow", "monitor glow"],               "gaming monitor 27 inch"),
    (["energy drink", "energy can"],                           "energy drink variety pack"),

    # Fashion
    (["bomber jacket"],                                        "black bomber jacket men"),
    (["trench coat"],                                          "dark trench coat men long"),
    (["hoodie", "oversized hoodie", "dark hoodie"],            "oversized black hoodie men"),
    (["flannel shirt", "flannel"],                             "black flannel shirt men"),
    (["cargo pants"],                                          "black cargo pants men"),
    (["dress shirt", "wrinkled shirt"],                        "slim fit black dress shirt men"),
    (["compression shirt", "fitted shirt"],                    "black compression shirt men"),
    (["crewneck", "sweatshirt"],                               "black crewneck sweatshirt men"),
    (["suit", "tailored suit"],                                "slim fit black suit men"),
    (["gloves", "leather gloves"],                             "black leather gloves men"),
    (["pocket square"],                                        "black pocket square silk"),
    (["scarf", "dark scarf"],                                  "black scarf men winter"),

    # Accessories
    (["dog tags", "dog tag"],                                  "military dog tags stainless steel"),
    (["watch", "leather watch", "wristwatch"],                 "minimalist leather watch men black"),
    (["chain necklace", "necklace"],                           "thin chain necklace men silver"),
    (["backpack", "battered backpack"],                        "black minimalist backpack"),

    # Props
    (["coffee mug", "ceramic mug", "coffee"],                  "ceramic coffee mug black matte"),
    (["lighter", "zippo"],                                     "matte black lighter windproof"),
    (["cigarette", "smoke"],                                   "cigarette case black metal"),
    (["guitar", "guitar pick"],                                "guitar pick set variety"),
    (["basketball"],                                           "indoor outdoor basketball"),
    (["paperback", "book"],                                    "dark academia journal notebook"),
    (["chopsticks"],                                           "japanese chopsticks set black"),
    (["camp chair", "camping"],                                "portable camping chair black"),
    (["marshmallow"],                                          "marshmallow roasting sticks telescoping"),
]


def extract_product(prompt: str, description: str) -> tuple:
    """Find the best product match from prompt + description text."""
    text = (prompt + " " + description).lower()
    for keywords, search_query in PRODUCT_MAP:
        for kw in keywords:
            if kw in text:
                return kw, search_query
    return None, None


def generate_affiliate_link(search_query: str) -> str:
    """Generate an Amazon search URL with the Associate tag."""
    params = urllib.parse.urlencode({
        "k": search_query,
        "tag": ASSOCIATE_TAG,
    })
    return f"https://www.amazon.com/s?{params}"


def run(dry_run=False):
    # Load queue
    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        queue = json.load(f)

    items = queue.get("items", [])
    print(f"\nScanning {len(items)} pins for linkable products...\n")
    print(f"{'#':<4} {'Character':<20} {'Product Found':<25} {'Link'}")
    print("=" * 100)

    linked = 0
    for item in items:
        prompt = item.get("prompt", "")
        desc = item.get("description", "")
        product_kw, search_query = extract_product(prompt, desc)

        if product_kw:
            link = generate_affiliate_link(search_query)
            item["link"] = link
            item["affiliate_product"] = product_kw
            linked += 1
            print(f"{item['id']:<4} {item.get('character',''):<20} {product_kw:<25} {link[:60]}...")
        else:
            item["link"] = ""
            item["affiliate_product"] = ""
            print(f"{item['id']:<4} {item.get('character',''):<20} {'(none found)':<25}")

    print(f"\n{'=' * 100}")
    print(f"Linked: {linked}/{len(items)} pins")

    if not dry_run:
        with open(QUEUE_FILE, "w", encoding="utf-8") as f:
            json.dump(queue, f, indent=2, ensure_ascii=False)
        print(f"Updated: {QUEUE_FILE}")
    else:
        print("(dry run — no files modified)")


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    run(dry_run=dry)
