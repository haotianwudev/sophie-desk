import json

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('"battle": "bingzhou_langqi"', '"battle": "ln_langqi"')

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'w', encoding='utf-8') as f:
    f.write(text)

print('Patched battle id!')
