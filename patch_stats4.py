import json

with open(r'F:\workspace\sanguo-cards\docs\CHAPTER-STATS.md', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. luoyang_n row
old_ln = '| 第二章 · 洛阳烟云（北线） | luoyang_n | 北方出生 | 43 | 7 / 3 / 2 | 1 choose + 1 lose_goto + 3 rogue_fork | 吕玲绮 | 2/4（ln_camp✅、c2_sanying✅；ln_handhold、c2_lingqi_oath 待画；⚠️甄宓画小了，见下方说明） | 0 / 3 / 0 / 1（池子走北线 scope） | 无（接第三章·黑山风云） |'
new_ln = '| 第二章 · 洛阳烟云（北线） | luoyang_n | 北方出生 | 43 | 7 / 3 / 2 | 1 choose + 1 lose_goto + 3 rogue_fork | 吕玲绮 | 2/8（新增4张，ln_camp✅、c2_sanying✅） | 0 / 3 / 0 / 1（池子走北线 scope） | 无（接第三章·黑山风云） |'
text = text.replace(old_ln, new_ln)

# 2. heishan row
old_hs = '| 第三章 · 黑山风云（北线） | heishan | 北线：班师冀州 | 55 | 9 / 3 / 1 | 2 choose（军法？/ 救人？），4 组洗牌 | 夏侯兰、张宁 | 0/1（nd_fuchao） | 0 / 0 / 北线 scope / 4 | 结局六 · 覆巢（不救张白骑线） |'
new_hs = '| 第三章 · 黑山风云（北线） | heishan | 北线：班师冀州 | 55 | 9 / 3 / 1 | 2 choose（军法？/ 救人？），4 组洗牌 | 夏侯兰、张宁 | 0/16（全覆盖） | 0 / 0 / 北线 scope / 4 | 结局六 · 覆巢（不救张白骑线） |'
text = text.replace(old_hs, new_hs)

# 3. shouluoyang row
old_sl = '| 第三章 · 驻守洛阳 | shouluoyang | 路线：守洛阳 | 18 | 6 / 1 / 0 | 0 | 朱儁 | 0/6 | 0 / 0 / 18 / 0 | （接长安） |'
new_sl = '| 第三章 · 驻守洛阳 | shouluoyang | 路线：守洛阳 | 18 | 6 / 2 / 0 | 0 | 朱儁 | 0/6 | 0 / 0 / 18 / 0 | （接长安） |'
text = text.replace(old_sl, new_sl)

# 4. total row
old_total = '| **合计（已实装）** | 9 条 quest | — | **391** | **73 / 24 / 17**（共 114 场战斗） | — | 27 个可招募卡 | **40/94** | — | 5 个结局卡 + 1 个占位结局 |'
new_total = '| **合计（已实装）** | 9 条 quest | — | **391** | **73 / 25 / 17**（共 115 场战斗） | — | 27 个可招募卡 | **40/113** | — | 5 个结局卡 + 1 个占位结局 |'
text = text.replace(old_total, new_total)

with open(r'F:\workspace\sanguo-cards\docs\CHAPTER-STATS.md', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated table exact matches!')
