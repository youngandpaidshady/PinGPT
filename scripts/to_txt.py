import json

with open("gemgen_queue.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("prompts.txt", "w", encoding="utf-8") as out:
    for item in data.get("items", []):
        out.write(f"Prompt {item['id']}:\n{item['prompt']}\n\n")

print("Saved to prompts.txt")
