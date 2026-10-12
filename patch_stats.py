import re

with open(r'F:\workspace\sanguo-cards\docs\CHAPTER-STATS.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace: 
# - 战斗：6 普通 / 1 精英（郭汜），没有首领战。
# with:
# - 战斗：6 普通 / 2 精英（郭汜、李傕），没有首领战。
text = text.replace('战斗：6 普通 / 1 精英（郭汜），没有首领战。', '战斗：6 普通 / 2 精英（郭汜、李傕），没有首领战。')

with open(r'F:\workspace\sanguo-cards\docs\CHAPTER-STATS.md', 'w', encoding='utf-8') as f:
    f.write(text)
print('Patched CHAPTER-STATS.md')
