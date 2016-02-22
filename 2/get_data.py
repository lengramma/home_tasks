'''
Скрипт собирает со страниц необходимую для метатаблицы информацию, записывает текст в отдельные файлы и раскладывает их по папкам в соответствии с заданной структурой

'''
import urllib.request
import re
import sys
import os
from os import path
import lxml.html
import html
import csv
import json
from bs4 import BeautifulSoup
from csv import DictWriter
import datetime
from datetime import date

def file_structure(date, fullPath, filename):
'''Строится файловая структура'''
    if os.path.exists(fullPath + str(date.year) + '\\' + str(date.month)):
        os.rename(fullPath + filename[:-4] + 'txt', fullPath + str(date.year) + '\\' + str(date.month) + '\\' + filename[:-4] + 'txt')
    else:
        os.makedirs(fullPath + str(date.year) + '\\' + str(date.month), exist_ok=True)
        os.rename(fullPath + filename[:-4] + 'txt', fullPath + str(date.year) + '\\' + str(date.month) + '\\' + filename[:-4] + 'txt')

meta = open('meta.csv', 'w', encoding='utf-8')
fieldnames = ['path', 'author', 'sex', 'birthday', 'header', 'created', 'sphere', 'genre_fi', 'type', 'topic', 'chronotop', 'style', 'audience_age', 'audience_level', 'audience_size', 'source', 'publication', 'publisher', 'publ_year', 'medium', 'country', 'region', 'language']
writer = csv.DictWriter(meta, fieldnames, restval='', extrasaction='raise', delimiter='\t', lineterminator='\n')
writer.writeheader()
# Словарь: ключи - названия html-файлов, значения - их URLы
dictUrl = {}
r = open('report.csv', 'r', encoding='utf-8')
reader = csv.reader(r, delimiter='\t')
for row in reader:
    dictUrl[row[1]] = row[0]
    
for root, dirs, files in os.walk('C:\\Users\\Lena\\home_tasks\\2\\pages'):
    for filename in files:
        new = open(root + '//' + filename, 'r', encoding='utf-8')
        soup = BeautifulSoup(new, 'html.parser')
        # Дата
        findDate = soup.find("div", "full")
        a = []
        for text in findDate.stripped_strings:
            a.append(text)
        date = a[0]
        try:
            date = datetime.datetime.strptime(date, "%d-%m-%Y")
        except ValueError:
            if re.search('Вчера', date, flags=re.IGNORECASE) != None:
                date = datetime.datetime.strptime("17.02.2016", "%d.%m.%Y")
            elif re.search('Сегодня', date, flags=re.IGNORECASE) != None:
                date = datetime.datetime.strptime("18.02.2016", "%d.%m.%Y")
            else:
                date = datetime.datetime.strptime("01.01.1970", "%d.%m.%Y")
        date2 = date.strftime("%d.%m.%Y")
        
        # Заголовок
        header = soup.h1.string
        
        # Автор
        try:
            author = []
            findAuthor = soup.find(style="text-align:right;")
            for text in findAuthor.stripped_strings:
                author.append(text)
            author_norm = author[0].strip(',.')
        except AttributeError:
            author_norm = 'Noname'
        
        # Текст статьи
        findArticle = soup.findAll(style="display:inline;")
        article = []
        for text in findArticle:
            odd = text.find(attrs={'style': re.compile("text-align:right;")})
            odd_list = []
            try:
                for n in odd.stripped_strings:
                    odd_list.append(n)
            except AttributeError:
                pass
            for stri in text.stripped_strings:
                if not stri in odd_list:
                    article.append(stri)
        
        # Тема
        topic = []
        findTopic = soup.find("div", "title-content")
        for text in findTopic.stripped_strings:
            topic.append(text)
            
        url = dictUrl[filename]              
        fullPathUnmarked = 'C:\\Users\\Lena\\home_tasks\\2\\files_unmarked\\'
        fullPathAux = 'C:\\Users\\Lena\\home_tasks\\2\\files_aux\\'
        f = open(fullPathUnmarked + filename[:-4] + 'txt', 'w', encoding='utf-8')
        m = open(fullPathAux + filename[:-4] + 'txt', 'w', encoding='utf-8')
        for line in article:
            m.write(line + '\n')
        f.write('@au ' + author_norm + '\n')
        f.write('@ti ' + header + '\n')
        f.write('@da ' + date2 + '\n')
        f.write('@topic ' + topic[0] + '\n')
        f.write('@url ' + url + '\n')
        for line in article:
            f.write(line + '\n')
        print(filename)
        f.close()
        m.close()
        
        new.close()
        
        file_structure(date, fullPathUnmarked, filename)
        file_structure(date, fullPathAux, filename)
                      
        dictFields = {}
        dictFields['path'] = os.path.relpath(fullPathUnmarked + str(date.year) + '\\' + str(date.month) + '\\' + filename[:-4] + 'txt', start=os.curdir)
        dictFields['author'] = author_norm
        dictFields['header'] = header
        dictFields['created'] = date2
        dictFields['sphere'] = 'публицистика'
        dictFields['topic'] = topic[0]
        dictFields['style'] = 'нейтральный'
        dictFields['audience_age'] = 'н-возраст'
        dictFields['audience_level'] = 'н-уровень'
        dictFields['audience_size'] = 'городская'
        dictFields['source'] = url
        dictFields['publication'] = 'Вечерняя Уфа'
        dictFields['publ_year'] = date.year
        dictFields['medium'] = 'газета'
        dictFields['country'] = 'Россия'
        dictFields['region'] = 'республика Башкортостан'
        dictFields['language'] = 'ru'
        
        writer.writerow(dictFields)

meta.close()
r.close()
