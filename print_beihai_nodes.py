import json
with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

q = next(q for q in d['quests'] if q['id'] == 'beihai')
for k, v in q['squares'].items():
    if k in ['bh_m1', 'bh_m2', 'bh_bandit', 'bh_zheng_pre', 'bh_river', 'bh_cross', 'bh_hj_out', 'bh_taishici_meet', 'bh_hj_gate', 'bh_guanhai_pre', 'bh_guanhai', 'bh_porridge', 'bh_kongrong']:
        print(f"{k}: x={v.get('x')} next={v.get('next')}")
