import json

with open("tele_ids.json", "r", encoding='utf-8') as ids:
    ids_list = json.load(ids)

copy = ids_list
counter = 200
ids_list[2005]["2005"] = None
for i in range(2005, 2041):
    ids_list[i][f"{i}"], ids_list[i+1][f"{i+1}"] = ids_list[i+1][f"{i+1}"], ids_list[i][f"{i}"] 

with open("tele_ids.json", "w", encoding='utf-8') as ids:
    json.dump(ids_list, ids, ensure_ascii=False)

index_to_fix = 2005

with open("films.json", 'r', encoding='utf-8') as films:
    films_list = json.load(films)

for film_index in range(index_to_fix, len(films_list)):
    films_list[film_index]['tele_id'] = None

with open("films.json", 'w', encoding='utf-8') as films:
    json.dump(films_list, films, ensure_ascii=False)