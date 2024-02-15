import json
x = '{"firstName": "Elizaveta", "lastName": "Antanenka", "city": "Vilnius"}'
y = json.loads(x)
print(y["firstName"])