import json
import os
import sys

with open("users.json", 'r', encoding='utf-8') as films:
    films_list = json.load(films)

print(len(films_list))

for user in films_list:
    user["recommend"] = True

with open("users.json", 'w', encoding='utf-8') as films:
    json.dump(films_list, films, ensure_ascii=False)
# a = int(input())
# if a == 0:
#     sys.exit()
# else:
#     print("doesnt work")

# print("djvnjdnv")