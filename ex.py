import json


def comliment():
    with open("ids.json", 'r', encoding="utf-8") as ids:
        ids_dict = json.load(ids)
    with open("films.json", 'r', encoding="utf-8") as films:
        films_dict = json.load(films)

    for film in films_dict:
        if film["tele_id"] == None:
            last = films_dict.index(film)
            break

    for i in range(last, len(ids_dict)):
        for film_num in range(last, len(films_dict)):
            if films_dict[film_num]['tele_id'] == None and str(film_num) in ids_dict[i].keys():
                films_dict[film_num]["tele_id"] = ids_dict[i][f"{i}"]
        

    with open("films.json", 'w', encoding="utf-8") as films_w:
        json.dump(films_dict, films_w, ensure_ascii=False)
