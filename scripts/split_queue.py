import json

with open('gemgen_queue.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

items = d['items']
p1 = {"session_id": "lasttrain_batch1", "items": items[:10]}
p2 = {"session_id": "4amvibes_batch2", "items": []}
for i, item in enumerate(items[10:], 1):
    item2 = dict(item)
    item2['id'] = i
    p2['items'].append(item2)

with open('gemgen_queue.json', 'w', encoding='utf-8') as f:
    json.dump(p1, f, indent=2)

with open('gemgen_queue_part2.json', 'w', encoding='utf-8') as f:
    json.dump(p2, f, indent=2)

print(f"Part 1: {len(p1['items'])} items (gemgen_queue.json)")
print(f"Part 2: {len(p2['items'])} items (gemgen_queue_part2.json)")
