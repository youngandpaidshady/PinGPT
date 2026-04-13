import json

# The manual mapping discovered previously
mapping = {
    "dl_7.png": "Megumi Fushiguro",
    "Vertical_9_16_Portrait__202604080552.png": "Dazai Osamu",
    "9_16_Cinematic_Still__202604080549.png": "Killua Zoldyck",
    "Vertical_9_16_Portrait__202604080549.png": "Yuji Itadori",
    "Generate_an_image_202604080548.png": "Aki Hayakawa",
    "Vertical_9_16_Portrait__202604080548.png": "Yuta Okkotsu",
    "9_16_Cinematic_Still__202604080548.png": "Geto Suguru",
    "Generate_an_image_202604080547.png": "Shoto Todoroki"
    # Excluding Kento Nanami since he has no prompt in the queue
}

with open("c:\\Users\\Administrator\\Desktop\\PinGPT\\gemgen_queue.json", "r") as f:
    queue = json.load(f)["items"]

out = {}
for filename, char_name in mapping.items():
    # find char in queue
    found = next((q for q in queue if q["character"] == char_name), None)
    if found:
        out[filename] = {
            "matched_character": char_name,
            "prompt_details": {
                "title": found["title"],
                "description": found["description"],
                "tags": found["tags"],
                "alt_text": found.get("alt_text", ""),
                "niche": "lasttrain" # Assign a default niche if absent
            }
        }

with open("c:\\Users\\Administrator\\Desktop\\PinGPT\\output\\gemgen_batch\\bulkpin_metadata.json", "w") as f:
    json.dump(out, f, indent=2)

print(f"Generated metadata for {len(out)} images.")
