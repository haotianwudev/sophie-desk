import re

# Update CHAPTER-STATS.md
with open(r'F:\workspace\sanguo-cards\docs\CHAPTER-STATS.md', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'\|\s*第四章（北线）\s*\|\s*北海相\s*\(eihai\)\s*\|\s*47.*?\|.*?\|.*?\|.*?\|.*?\|',
              r'| 第四章（北线） | 北海相 (eihai) | 54 | 12 / 5 / 2 | 8 | 0 | 6 兵 |', text)

with open(r'F:\workspace\sanguo-cards\docs\CHAPTER-STATS.md', 'w', encoding='utf-8') as f:
    f.write(text)

# Update STORY.md
with open(r'F:\workspace\sanguo-cards\docs\STORY.md', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('约 47 格', '约 54 格')

with open(r'F:\workspace\sanguo-cards\docs\STORY.md', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated docs")
