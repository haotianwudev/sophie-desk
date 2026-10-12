import json

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'r', encoding='utf-8') as f:
    text = f.read()

target = '\"你一挥马鞭，直指黄河以南：「子龙、奉孝，走——去会一会十八路诸侯！」\", \"……屏幕上跳出一行字：「北线 · 敬请期待」。\", \"下面还有一行小字：「这段故事，留到下次一起开。」\"], \"cg\": \"jz_end\"}'
replacement = '\"你一挥马鞭，直指黄河以南：「子龙、奉孝，走——去会一会十八路诸侯！」\"], \"cg\": \"jz_end\"}'

text = text.replace(target, replacement)

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'w', encoding='utf-8') as f:
    f.write(text)

print('Fixed jz_end cleanly!')
