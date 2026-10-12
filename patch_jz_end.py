import json

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('\"……屏幕上跳出一行字：「北线 · 敬请期待」。\", ', '')
text = text.replace('\"下面还有一行小字：「这段故事，留到下次一起开。」\"', '')

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'w', encoding='utf-8') as f:
    f.write(text)

print('Removed placeholder text from jz_end!')
