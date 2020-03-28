import json

with open("films.json", 'r', encoding='utf-8') as films:
    films_list = json.load(films)

print(len(films_list))