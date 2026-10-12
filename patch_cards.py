import re
with open(r'F:\workspace\sanguo-cards\godot\data\cards.json', 'r', encoding='utf-8') as f:
    text = f.read()

# Add to scenarios
insert_idx = text.find('\"scenarios\": {') + len('\"scenarios\": {')
new_scenario = '\n    \"c4_lijue_test\": {\"name\": \"拦路迎亲\", \"turn_limit\": 6, \"enemy\": \"lijue\"},'

text = text[:insert_idx] + new_scenario + text[insert_idx:]

with open(r'F:\workspace\sanguo-cards\godot\data\cards.json', 'w', encoding='utf-8') as f:
    f.write(text)
print('Patched cards.json!')
