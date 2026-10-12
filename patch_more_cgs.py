import json

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('\"hs_start\": {\"type\"', '\"hs_start\": {\"cg\": \"c3_recruit_board\", \"type\"')
text = text.replace('\"hs_peiqian\": {\"type\"', '\"hs_peiqian\": {\"cg\": \"c3_bribe_villager\", \"type\"')
text = text.replace('\"hs_encounter\": {\"type\"', '\"hs_encounter\": {\"cg\": \"c3_encounter_ning\", \"type\"')
text = text.replace('\"hs_ignore\": {\"type\"', '\"hs_ignore\": {\"cg\": \"c3_leave_ning\", \"type\"')

text = text.replace('\"hs_zhangyan\": {\"cg\": \"c3_save_ning\", \"type\"', '\"hs_zhangyan\": {\"cg\": \"c3_zhangyan_meet\", \"type\"')
text = text.replace('\"hs_save_fight\": {\"type\"', '\"hs_save_fight\": {\"cg\": \"c3_save_ning\", \"type\"')

text = text.replace('\"hs_timeskip\": {\"type\"', '\"hs_timeskip\": {\"cg\": \"c3_guotu_raid\", \"type\"')
text = text.replace('\"hs_escape\": {\"type\"', '\"hs_escape\": {\"cg\": \"c3_secret_path\", \"type\"')
text = text.replace('\"hs_jieqiao_eve\": {\"type\"', '\"hs_jieqiao_eve\": {\"cg\": \"c3_guojia_map\", \"type\"')
text = text.replace('\"hs_breakout\": {\"type\"', '\"hs_breakout\": {\"cg\": \"c3_breakout\", \"type\"')

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'w', encoding='utf-8') as f:
    f.write(text)
print('Patched story.json with more CGs!')
