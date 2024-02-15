import json
x = '{"firstName": "Elizaveta", "lastName": "Antanenka", "city": "Vilnius", "age": "19"}'
y = json.loads(x)
print(y["firstName"])
