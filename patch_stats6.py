with open(r'F:\workspace\sanguo-cards\docs\CHAPTER-STATS.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for line in lines:
    if 'luoyang_n' in line or 'heishan' in line or 'shouluoyang' in line:
        print(repr(line))
