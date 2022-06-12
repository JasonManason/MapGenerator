import json

file = open('nb_rules.json')
data = json.load(file)

for i in data["data"]:
    print(i)


file.close()