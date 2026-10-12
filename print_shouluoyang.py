import json
with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

q = next(q for q in d['quests'] if q['id'] == 'shouluoyang')
for k, v in q['squares'].items():
    print(f"{k} [{v.get('type')}] ({v.get('x')}, {v.get('y')}): {v.get('label')} -> {v.get('next')}")
