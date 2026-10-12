import json
with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

q = next(q for q in d['quests'] if q['id'] == 'dongui')
for k in ['mimou', 'chaohui', 'luan']:
    node = q['squares'].get(k, {})
    print(f"--- {k} ---")
    print(f"Requires: {node.get('requires')}")
    print(f"Unless: {node.get('unless')}")
    print(f"Text: {node.get('text')}")
