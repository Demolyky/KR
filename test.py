import json

with open('file.json', 'r', encoding='utf-8') as FILE:
    parsen = json.load(FILE)
    print(parsen.loads("Y"))
