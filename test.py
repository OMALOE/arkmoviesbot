import json
import os
import sys

with open("films.json", 'r', encoding='utf-8') as films:
    films_list = json.load(films)

print(len(films_list))

# a = int(input())
# if a == 0:
#     sys.exit()
# else:
#     print("doesnt work")

# print("djvnjdnv")