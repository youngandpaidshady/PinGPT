import json
try:
    q = json.load(open('gemgen_queue.json', encoding='utf-8'))
    for i, p in enumerate(q[:5]):
        print(f"Prompt {i+1}: {p['prompt']}\n")
except Exception as e:
    print(e)
