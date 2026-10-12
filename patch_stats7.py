import re

with open(r'F:\workspace\sanguo-cards\docs\CHAPTER-STATS.md', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(
    r'\| 第二章 · 洛阳烟云（北线） \| luoyang_n \|.*',
    r'| 第二章 · 洛阳烟云（北线） | luoyang_n | 北方出生 | 43 | 7 / 3 / 2 | 1 choose + 1 lose_goto + 3 rogue_fork | 吕玲绮 | 2/8（新增4张，ln_camp✅、c2_sanying✅） | 0 / 3 / 0 / 1（池子走北线 scope） | 无（接第三章·黑山风云） |',
    text
)

text = re.sub(
    r'\| 第三章 · 黑山风云（北线） \| heishan \|.*',
    r'| 第三章 · 黑山风云（北线） | heishan | 北线：班师冀州 | 55 | 9 / 3 / 1 | 2 choose（军法？/ 救人？），4 组洗牌 | 夏侯兰、张宁 | 0/16（全覆盖） | 0 / 0 / 北线 scope / 4 | 结局六 · 覆巢（不救张白骑线） |',
    text
)

text = re.sub(
    r'\| 第三章 · 驻守洛阳 \| shouluoyang \|.*',
    r'| 第三章 · 驻守洛阳 | shouluoyang | 路线：守洛阳 | 18 | 6 / 2 / 0 | 0 | 朱儁 | 0/6 | 0 / 0 / 18 / 0 | （接长安） |',
    text
)

text = re.sub(
    r'小计：7 普通 / 3 精英 / 2 首领，1 choose \+ 1 lose_goto \+ 3 组 rogue 岔路.*?CG 挂了 4 张字段',
    r'小计：7 普通 / 3 精英 / 2 首领，1 choose + 1 lose_goto + 3 组 rogue 岔路（ln_ambush/ln_mystery_forest、ln_box*、ln_rear_guard/ln_mystery_retreat），CG 挂了 8 张字段',
    text
)

with open(r'F:\workspace\sanguo-cards\docs\CHAPTER-STATS.md', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated table using regex sub!')
