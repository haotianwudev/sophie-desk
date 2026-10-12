import json

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

q = next(q for q in d['quests'] if q['id'] == 'luoyang_n')

if 'ln_charge' in q['squares']: q['squares']['ln_charge']['cg'] = 'c2_ln_meet'
if 'ln_banner' in q['squares']: q['squares']['ln_banner']['cg'] = 'c2_ln_sponsor'
if 'ln_caocao' in q['squares']: q['squares']['ln_caocao']['cg'] = 'c2_ln_caocao'
if 'ln_rescue' in q['squares']: q['squares']['ln_rescue']['cg'] = 'c2_ln_bianshui'

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print('Patched luoyang_n CGs in story.json!')
