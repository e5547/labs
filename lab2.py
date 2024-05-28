import json

merged = {}

with open('users1.json') as f:
    jsonified = json.load(f)
    data = jsonified['table']['users']
    for id, info in data.items():
        merged[id] = info
    

with open('users2.json') as f:
    jsonified = json.load(f)
    data = jsonified['table']['users']
    for id, info in data.items():
        if id in merged:
            merged[id].update(info)
        else:
            merged[id] = info
    
print(merged)
