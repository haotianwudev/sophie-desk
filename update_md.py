import re

with open(r'F:\workspace\sanguo-cards\docs\CHAPTER-STATS.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the beihai line in the markdown table
# Old: | 第四章（北线） | 北海相 (eihai) | 43 | 5 / 3 / 2 | 4 | 0 | 6 兵 |
# New: | 第四章（北线） | 北海相 (eihai) | 47 | 6 / 5 / 2 | 8 | 0 | 6 兵 |
text = re.sub(r'\|\s*第四章（北线）\s*\|\s*北海相\s*\(eihai\)\s*\|\s*43\s*\|\s*5 / 3 / 2\s*\|\s*4\s*\|\s*0\s*\|',
              r'| 第四章（北线） | 北海相 (eihai) | 47 | 6 / 4 / 2 | 8 | 0 |', text)

# Wait, the number of Elite battles is 4 or 5? 
# Zheng Hao, Jiang Qiao, Gao Shun, Yan Liang, Qushuai. That is 5!
text = re.sub(r'\|\s*第四章（北线）\s*\|\s*北海相\s*\(eihai\)\s*\|\s*43.*?\|.*?\|.*?\|.*?\|.*?\|',
              r'| 第四章（北线） | 北海相 (eihai) | 47 | 6 / 5 / 2 | 8 | 0 | 6 兵 |', text)

with open(r'F:\workspace\sanguo-cards\docs\CHAPTER-STATS.md', 'w', encoding='utf-8') as f:
    f.write(text)
