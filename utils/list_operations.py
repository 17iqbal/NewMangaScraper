# Utils to concat, sort, splice('/Manga/') from items;
import json
from functools import reduce

new_manga_list = []

with open('../mangas_1.json') as mangas_list:
    for line in mangas_list:
        line = line.strip()
        if line != ']' and line != '[' and line != '][' and line != ',':
            line = line[7:]
            line
            new_manga_list.append(line)
    new_manga_list.sort()
    # print(new_manga_list)

mangas_list = open('../mangas_2.json', 'w')
mangas_list.write(' '.join(new_manga_list))


# for item in mangas_list:
#     new_manga_list +=item
#     print(item)

# print(new_manga_list)