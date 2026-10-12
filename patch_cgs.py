import json

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('\"hs_junfa\": {\"type\"', '\"hs_junfa\": {\"cg\": \"c3_xiahoulan_law\", \"type\"')
text = text.replace('\"hs_zhangyan\": {\"type\"', '\"hs_zhangyan\": {\"cg\": \"c3_save_ning\", \"type\"')
text = text.replace('\"hs_alliance\": {\"type\"', '\"hs_alliance\": {\"cg\": \"c3_alliance\", \"type\"')
text = text.replace('\"hs_quyi\": {\"type\"', '\"hs_quyi\": {\"cg\": \"c3_quyi_camp\", \"type\"')
text = text.replace('\"hs_wenchou\": {\"type\"', '\"hs_wenchou\": {\"cg\": \"c3_save_zan\", \"type\"')
text = text.replace('\"hs_end\": {\"type\"', '\"hs_end\": {\"cg\": \"c3_banma_flag\", \"type\"')

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'w', encoding='utf-8') as f:
    f.write(text)
print('Patched CGs!')
