import json

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'r', encoding='utf-8') as f:
    text = f.read()

old_hs_end = '\"文丑败退，公孙瓒惊魂未定，当场赠五百匹幽州白马：「这份情，伯珪记下了！」\", \"黑白斑马大旗迎风飘扬。去青州，咱们重新安家！\", \"「第四章 · 北海相 敬请期待」。\"'
new_hs_end = '\"文丑败退，公孙瓒惊魂未定，当场赠五百匹幽州白马：「这份情，伯珪记下了！」\", \"黑白斑马大旗迎风飘扬。{lord}：「袁绍在平原势大，无险可守。咱们带人退回太行山，扎紧山门，跟他慢慢耗！」\", \"「第四章 · 双凤乱太行 敬请期待」。\"'

text = text.replace(old_hs_end, new_hs_end)

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated hs_end!')
