'''
Скрипт делает поисковый запрос к API ВКонтакте, возвращает список id пользователей из Магнитогорска и создаёт для них таблицу метаданнх с социолингвистической информацией: uid - id пользователя, first_name - имя пользователя, last_name - фамилия пользователя, city - номер города (Магнитогорск - 82), bdate - дата рождения пользователя, home_town - родной город.

'''
import urllib.request
import json
import csv
from csv import DictWriter


def vk(method, parameters):
    query = 'https://api.vk.com/method/' + method + '?' + parameters + '&access_token=e11444c94755149ddbdea7ef87d650fcffa27fb020a53c51def0f5cff3e8088a2d80b1db0892ee5edde46'
    con = urllib.request.urlopen(query)
    page = con.read()
    page = page.decode("utf-8")
    return(page)

meta = open('meta.csv', 'w', encoding='utf-8')
fieldnames = ['uid', 'first_name', 'last_name', 'city', 'bdate', 'home_town']
writer = csv.DictWriter(meta, fieldnames, restval='', extrasaction='raise', delimiter='\t', lineterminator='\n')
writer.writeheader()
search_query = vk('users.search', 'city=82&count=1000&fields=bdate,home_town,city')
# print(search_query)
a = json.loads(search_query)

for shto in a['response']:
    if type(shto) is dict:
        writer.writerow(shto)
        
meta.close()
