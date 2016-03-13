'''
Скрипт строит частотный список словоформ на очищенной википедии на мокшанском языке

'''
from bs4 import BeautifulSoup
import os
import re

'''Предварительная очистка от ставшейся xml-разметки'''
def extract_text(page, filename):
    soup = BeautifulSoup(page, 'html.parser')
    pageText = soup.findAll(text=True)
    text = ''.join(pageText)
    n = open('C:\\Users\\Lena\\Desktop\\wiki\\AA\\txt\\' + filename + '_clean' + '.txt', 'w', encoding='utf-8')
    n.write(text)
    n.close()
    
freqDict = {}
for root, dirs, files in os.walk('C:\\Users\\Lena\\Desktop\\wiki\\AA'):
    for filename in files:
        if re.search('\\.txt', filename) == None:
            f = open(root + '//' + filename, 'r', encoding='utf-8')
            page = f.read()
            cleanText = extract_text(page, filename)
            f.close()
            t = open('C:\\Users\\Lena\\Desktop\\wiki\\AA\\txt\\' + filename + '_clean' + '.txt', 'r', encoding='utf-8')
            page = t.readlines()
            for line in page:
                wordsInLine = line.split()
                wordsInLine = re.findall('\w+', line)
                for word in wordsInLine:
                    word = word.lower()
                    if word in freqDict:
                        freqDict[word] += 1
                    else:
                        freqDict[word] = 1
            t.close()
        
a = open('freqdict.tsv', 'w', encoding='utf-8')
for word in sorted(freqDict, key = lambda x: freqDict[x], reverse=True):
    a.write(word + '\t' + str(freqDict[word]) + '\n')
a.close()       
