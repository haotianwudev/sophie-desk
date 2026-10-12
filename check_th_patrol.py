import json
d = json.load(open(r'F:\workspace\sanguo-cards\godot\data\cards.json', encoding='utf-8'))
if 'th_patrol' in d['scenarios']:
    print("In scenarios!")
if 'th_patrol' in d['enemies']:
    print("In enemies!")
