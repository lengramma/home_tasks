'''
Скрипт скачивает записи со стен пользователей, записывает в файл; для каждого пользователя создаёт таблицу метаданных с полями: post_id - номер записи, text = текст записи, date = дата публикации записи.

'''
import urllib.request
import json
import csv
from csv import DictWriter
import datetime
from time import time, sleep
import re

def vk(method, parameters):
    query = 'https://api.vk.com/method/' + method + '?' + parameters + '&access_token=e11444c94755149ddbdea7ef87d650fcffa27fb020a53c51def0f5cff3e8088a2d80b1db0892ee5edde46'
    con = urllib.request.urlopen(query)
    page = con.read()
    page = page.decode("utf-8")
    return(page)
    
def get_text(id):
    n = 1
    meta = open('C:\\Users\\Lena\\home_tasks\\api_vk\\meta_by_users\\meta_' + id + '.csv', 'w', encoding='utf-8')
    posts = open('C:\\Users\\Lena\\home_tasks\\api_vk\\posts_by_users\\posts_' + id + '.txt', 'a', encoding='utf-8')
    writer = csv.DictWriter(meta, fieldnames, restval='', extrasaction='raise', delimiter='\t', lineterminator='\n')
    writer.writeheader()
    time()
    sleep(0.34)
    wall_query = vk('wall.get', 'owner_id=' + id + '&count=100&filter=owner')
    a = json.loads(wall_query)  
    for i in a['response']:
        if type(i) is dict:
            if i['post_type'] == 'post':
                dictFields = {}
                text = i['text']
                text = re.sub('<br>', ' ', text)
                date = i['date']
                date =  datetime.datetime.fromtimestamp(date)
                dictFields['post_id'] = n
                dictFields['text'] = text
                dictFields['date'] = date               
                writer.writerow(dictFields)
                n += 1
                if text != '':
                    posts.write(text + '\n' + '\n')
    meta.close()
    posts.close()

ids = []
n = open('meta.csv', 'r', encoding='utf-8')
reader = csv.reader(n, delimiter='\t')
fieldnames = ['post_id', 'text', 'date']

for row in reader:
    ids.append(row[0])

for id in ids[1:]:
   get_text(id)
