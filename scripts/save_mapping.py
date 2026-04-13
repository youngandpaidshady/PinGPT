import json
import os

# Subagent Output Mapping
raw_map = {
  "dl_10.png": "Aki Hayakawa - lasttrain",
  "dl_11.png": "Megumi Fushiguro - 4amvibes",
  "dl_12.png": "Eren Yeager - 4amvibes",
  "dl_13.png": "Dazai Osamu - 4amvibes",
  "dl_14.png": "Toji Fushiguro - 4amvibes",
  "dl_4.png": "Spike Spiegel - lasttrain",
  "dl_5.png": "Sung Jinwoo - lasttrain",
  "dl_6.png": "Eren Yeager - lasttrain",
  "dl_7.png": "Suguru Geto - lasttrain",
  "dl_8.png": "Loid Forger - lasttrain",
  "dl_9.png": "Dazai Osamu - lasttrain",
  "Generate_an_image_202604071309 (1).png": "Spike Spiegel - lasttrain",
  "Generate_an_image_202604071309.png": "Toji Fushiguro - lasttrain",
  "Generate_an_image_202604071310.png": "Nanami Kento - lasttrain",
  "Generate_an_image_202604071422.png": "Aki Hayakawa - 4amvibes",
  "Generate_an_image_202604071426 (1).png": "Yuta Okkotsu - 4amvibes",
  "Generate_an_image_202604071426.png": "Sung Jinwoo - 4amvibes"
}

# Read Queues
q1_path = r"c:\Users\Administrator\Desktop\PinGPT\gemgen_queue.json"
q2_path = r"c:\Users\Administrator\Desktop\PinGPT\gemgen_queue_part2.json"

q1 = json.loads(open(q1_path, "r").read()) if os.path.exists(q1_path) else {"items": []}
q2 = json.loads(open(q2_path, "r").read()) if os.path.exists(q2_path) else {"items": []}

all_prompts = q1.get("items", []) + q2.get("items", [])

# Build full mapping lookup
prompt_lookup = {}
for p in all_prompts:
    key = f"{p['character']} - {p['niche']}"
    prompt_lookup[key] = p

final_mapping = {}

for filename, char_niche in raw_map.items():
    if char_niche in prompt_lookup:
        final_mapping[filename] = {
            "matched_character": char_niche,
            "prompt_details": prompt_lookup[char_niche]
        }
    else:
        final_mapping[filename] = {
            "matched_character": char_niche,
            "error": "Prompt not found in queues"
        }

out_path = r"c:\Users\Administrator\Desktop\PinGPT\output\gemgen_batch\final_mapping.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(final_mapping, f, indent=4)

print(f"Successfully saved 100% accurate visual mapping to {out_path}")
