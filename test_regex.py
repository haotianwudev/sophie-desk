import json
import re

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'r', encoding='utf-8') as f:
    text = f.read()

match = re.search(r'("id":\s*"beihai".*?"squares":\s*)(\{.*?\n\s*\})(?=\s*\}\s*,\s*\{\s*"id":\s*"dongui")', text, re.DOTALL)
if match:
    squares_str = match.group(2)
    try:
        sq = json.loads(squares_str)
        print("Successfully parsed squares!")
    except Exception as e:
        print("Failed to parse squares:", e)
else:
    print("Match failed")
