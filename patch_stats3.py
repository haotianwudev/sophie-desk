import re

with open(r'F:\workspace\sanguo-cards\docs\CHAPTER-STATS.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace luoyang_n row:
# | 第二章 · 洛阳烟云（北线） | luoyang_n | 北方出生 | 43 | 7 / 3 / 2 | 1 choose + 1 lose_goto + 3 rogue_fork | 吕玲绮 | 2/4（ln_camp✅、c2_sanying✅；ln_handhold、c2_lingqi_oath 待画；⚠️甄宓画小了，见下方说明） | 0 / 3 / 0 / 1（池子走北线 scope） | 无（接第三章·黑山风云） |
text = re.sub(
    r'\| 第二章 · 洛阳烟云（北线） \| luoyang_n \| 北方出生 \| 43 \| 7 / 3 / 2 \| .*? \| 吕玲绮 \| 2/4.*? \|',
    r'| 第二章 · 洛阳烟云（北线） | luoyang_n | 北方出生 | 43 | 7 / 3 / 2 | 1 choose + 1 lose_goto + 3 rogue_fork | 吕玲绮 | 2/8（新增4张，ln_camp✅、c2_sanying✅） |',
    text
)

# Replace heishan row:
# | 第三章 · 黑山风云（北线） | heishan | 北线：班师冀州 | 55 | 9 / 3 / 1 | 2 choose（军法？/ 救人？），4 组洗牌 | 夏侯兰、张宁 | 0/1（nd_fuchao） | 0 / 0 / 北线 scope / 4 | 结局六 · 覆巢（不救张白骑线） |
text = re.sub(
    r'\| 第三章 · 黑山风云（北线） \| heishan \| 北线：班师冀州 \| 55 \| 9 / 3 / 1 \| .*? \| 夏侯兰、张宁 \| 0/1.*? \|',
    r'| 第三章 · 黑山风云（北线） | heishan | 北线：班师冀州 | 55 | 9 / 3 / 1 | 2 choose（军法？/ 救人？），4 组洗牌 | 夏侯兰、张宁 | 0/16（全覆盖） |',
    text
)

# Replace shouluoyang row:
text = re.sub(
    r'\| 第三章 · 驻守洛阳 \| shouluoyang \| 路线：守洛阳 \| 18 \| 6 / 1 / 0 \|',
    r'| 第三章 · 驻守洛阳 | shouluoyang | 路线：守洛阳 | 18 | 6 / 2 / 0 |',
    text
)

# Replace the text: 小计：9 普通 / 3 精英 / 1 首领，2 choose，4 组洗牌，CG 只挂了 1 张字段（0 张交付）。
text = text.replace('CG 只挂了 1 张字段（0 张交付）', 'CG 挂了 16 张字段（0 张交付）')

with open(r'F:\workspace\sanguo-cards\docs\CHAPTER-STATS.md', 'w', encoding='utf-8') as f:
    f.write(text)

print('Patched table!')
