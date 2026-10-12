import json

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

q = next(q for q in d['quests'] if q['id'] == 'beihai')
for k, v in q['squares'].items():
    if v.get('type') in ['battle', 'choose']:
        print(f"{k}: {v.get('label')} -> {v.get('next')}")
