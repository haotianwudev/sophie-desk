import re

with open(r'F:\workspace\sanguo-cards\docs\STORY.md', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update 太行外围 (Taihang)
text = text.replace(
    '主角「以暴制暴」，两寨各打一仗（两场精英战）',
    '打退一波【太行巡山兵】（普通战）后，主角「以暴制暴」，两寨各打一仗（两场精英战）'
)
text = text.replace(
    '听两人从吵架吵到对骂、从对骂吵到一起骂他，天亮时两人勾着肩出来了。记「郑姜：和好」',
    '听两人从吵架吵到对骂、从对骂吵到一起骂他，天亮时两人勾着肩出来了。随后在简陋的山寨大堂里，三人豪迈对饮（【化敌为友】CG）。记「郑姜：和好」'
)

# 2. Update 夜渡黄河 (Yan Liang)
text = text.replace(
    '黄河渡口，袁绍的追兵咬了上来（普通战 · 冀州骑兵）。',
    '黄河渡口，袁绍的追兵咬了上来（普通战 · 冀州骑兵）。随后，一员大将提着大刀列阵，身后满是举着强弩的先登死士——**精英：渡口截杀 · 颜良**（【渡口截杀】CG）。{lord}（内心）：颜良？这可是河北名将啊！打退颜良后，'
)

# 3. Update 北海 (Beihai)
text = text.replace(
    '【初平四年 · 夏】南下路上，满路都是从北海逃出来的百姓：黄巾渠帅**管亥**带着几万饥民围了北海',
    '【初平四年 · 夏】南下路上，满路都是从北海逃出来的百姓：黄巾渠帅**管亥**带着几万饥民围了北海（【百万黄巾】CG）'
)
text = text.replace(
    '城外两战（北海城外 · 黄巾饥兵、城门 · 黄巾狂信徒），主角和赵云几次把力战脱力的太史慈从乱阵里拖出来。',
    '城外（北海城外 · 黄巾饥兵，普通）、城门（黄巾狂信徒，普通），太史慈如同利刃切开黑压压的阵型（【单骑破阵】CG）。冲破狂信徒后，一个穿着道袍的黄巾渠帅拦住去路，狂热念咒——**精英：黄巾渠帅**。主角和赵云几次把力战脱力的太史慈从乱阵里拖出来。'
)
text = text.replace(
    '打赢之后，主角不杀：在阵前架起几十口大锅熬粥',
    '打赢之后，主角不杀：在阵前架起几十口大锅熬粥（【阵前熬粥】CG）'
)

# 4. Update the Table
text = text.replace(
    '| 地图 | 约 45 格',
    '| 地图 | 约 47 格'
)
text = text.replace(
    '太行外围 · 山贼（普通）→ **精英：郑家寨 · 郑好** / **精英：姜家寨 · 姜巧**',
    '太行外围 · 山贼（普通）→ 太行巡山贼（普通）→ **精英：郑家寨 · 郑好** / **精英：姜家寨 · 姜巧**'
)
text = text.replace(
    '黄河渡口 · 冀州骑兵（普通）→ 北海城外 · 黄巾饥兵（普通）→ 城门 · 黄巾狂信徒（普通）→ **首领：北海城下 · 管亥**',
    '黄河渡口 · 冀州骑兵（普通）→ **精英：渡口 · 颜良** → 北海城外 · 黄巾饥兵（普通）→ 城门 · 黄巾狂信徒（普通）→ **精英：黄巾渠帅** → **首领：北海城下 · 管亥**'
)

# Insert the new CGs into the CG list of the table if not present
# Actually, the CG list for Chapter 4 might not exist in the table outline? Let's check if there's a 美術 line.
# Yes, | 美术 | ...
import re
def replace_art(m):
    art_line = m.group(0)
    if '化敌为友' not in art_line:
        return art_line + "新增 CG：化敌为友、渡口截杀、百万黄巾、单骑破阵、阵前熬粥。"
    return art_line

text = re.sub(r'\|\s*美术\s*\|.*\|', replace_art, text)

with open(r'F:\workspace\sanguo-cards\docs\STORY.md', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated STORY.md")
