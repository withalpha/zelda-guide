import json
with open('correct_dishes_mapping.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
print(len(data))
