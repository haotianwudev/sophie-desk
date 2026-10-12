import json

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('"battle": "hs_jizhou_cavalry"', '"battle": "hs_jizhou_qibing"')

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'w', encoding='utf-8') as f:
    f.write(text)

print('Patched hs_jizhou_cavalry battle id!')
