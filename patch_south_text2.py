import json

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'r', encoding='utf-8') as f:
    text = f.read()

# I will use string replace to keep story.json clean and compact!
# 1. Modify risk scope
text = text.replace('\"risk\": {\n      \"scope\": \"universal\",', '\"risk\": {\n      \"scope\": \"south\",')

# 2. Add risk_n
risk_n = ',\n    \"risk_n\": {\n      \"scope\": \"north\",\n      \"text\": [\n        \"风雪迷了眼。向导缩着脖子指着悬崖：「从这道险沟穿过去能抄近路，就是容易遇见伏兵。」\",\n        \"{lord}（内心）：兰斯十里这叫「难度UP」。选了，后面的敌人更强，奖励也更好。\"\n      ],\n      \"choose\": [\n        {\n          \"label\": \"走险沟（敌人变强，但必掉宝箱）\",\n          \"danger\": 1\n        },\n        {\n          \"label\": \"绕大路\"\n        }\n      ]\n    }'

# insert after risk
# wait, it's safer to just inject it before grand_chest
text = text.replace('\"grand_chest\": {', risk_n.lstrip(',\n') + ',\n    \"grand_chest\": {')

# 3. Fix ln_feast
old_feast = '{lord}（内心）：袁绍——爱开会、从不拍板的那种老板。（和南线那位一模一样的吐槽——毕竟是同一个人。）'
new_feast = '{lord}（内心）：袁绍——爱开会、从不拍板的那种老板。'
text = text.replace(old_feast, new_feast)

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'w', encoding='utf-8') as f:
    f.write(text)
print('Fixed!')
