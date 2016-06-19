'''
Скрипт исправляет ошибки в тексте оригинала в соответствии с эталоном. Во избежание попадания в итоговый файл ("filename_res") ошибок, фрагменты с нарушенной разметкой и с пропусками выводятся в отдельный файл - "filename_log"

'''
from bs4 import BeautifulSoup
import os

def distance(a, b):
    '''Считается расстояние Левенштейна между a и b'''
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n

    current_row = range(n+1) 
    for i in range(1, m+1):
        previous_row, current_row = current_row, [i]+[0]*n
        for j in range(1,n+1):
            add, delete, change = previous_row[j]+1, current_row[j-1]+1, previous_row[j-1]
            if a[j-1] != b[i-1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


def compareStrings(a, b, ql):
    try:
        q = (ql) * len(a)
        if a == b:
            return [True, 0]
        elif abs(len(a) - len(b)) > q:
            return [False, 0]

        dif = distance(a, b)
        if dif < q:
            return [True, dif]
        else:
            return [False, dif]
    except:
        return [False, -1]


def findStartIndex(par, sample, q):
    for i in range(len(sample)):
        r = compareStrings(par.find(variant_id='0').string, sample[i].find(variant_id='0').string, q)
        if r[0]:
            if r[1] > 0:
                par.find(variant_id='0').string = sample[i].find(variant_id='0').string
            return [True, i]
    return [False, -1]


def compareParagraps(sampleparagraphs, textparagraphs, q):

    if 0 > q < 1:
        print('Incorrect q value')
        return

    result = []
    missing = []
    errors = []
    startind = 0

    for i in range(len(textparagraphs)):

        if startind == len(sampleparagraphs):
            break

        de = compareStrings(textparagraphs[i].find(variant_id='0').string, sampleparagraphs[startind].find(variant_id='0').string, q)
        if de[0] and de[1] == 0:
            result.append(textparagraphs[i])
            startind += 1
            continue
        elif de[0] == True:
            textparagraphs[i].find(variant_id='0').string = sampleparagraphs[startind].find(variant_id='0').string
            result.append(textparagraphs[i])
            startind += 1
            continue
        else:
            try:
                de1 = compareStrings(textparagraphs[i].find(variant_id='0').string, sampleparagraphs[startind-1].find(variant_id='0').string, q)
                de2 = compareStrings(textparagraphs[i+1].find(variant_id='0').string, sampleparagraphs[startind+1].find(variant_id='0').string, q)
                if de1[0] and de2[0]:
                    missing.append(sampleparagraphs[startind])
                    startind += 1
                    continue
            except:
                pass

            indsearch = findStartIndex(textparagraphs[i], sampleparagraphs, q)
            if indsearch[0]:
                startind = indsearch[1] + 1
                result.append(textparagraphs[i])
                continue
            else:
                errors.append(textparagraphs[i])
                continue
    return [result, errors, missing]

def compareandsave(sampleparagraphs, textparagraphs, q, filepath):
    res = compareParagraps(sampleparagraphs, textparagraphs, q)

    filesp = os.path.splitext(filepath)

    tex = BeautifulSoup(features='xml')
    tex.append(BeautifulSoup.new_tag(tex, 'name'))
    tex.append(BeautifulSoup.new_tag(tex, 'body'))
    for par in res[0]:
        tex.body.append(par)

    html = tex.prettify('utf-8')
    with open(filesp[0] + '_res' + filesp[1], 'wb') as file:
        file.write(html)

    log = BeautifulSoup(features='xml')
    log.append(BeautifulSoup.new_tag(log, 'missing'))
    log.append(BeautifulSoup.new_tag(log, 'errors'))
    for par in res[1]:
        log.errors.append(par)
    for par in res[2]:
        log.missing.append(par)

    l = log.prettify('utf-8')
    # file = open(filesp[0] + '_log' + filesp[1], 'w', encoding='utf-8')
    with open(filesp[0] + '_log' + filesp[1], 'wb') as file:
        file.write(l)



def compareTexts(samplefilename, textfolder):
    s = BeautifulSoup(open(samplefilename, 'r', encoding='utf-8'), 'html.parser')
    sampleParagraphs = s.findAll('para')

    files = os.listdir(textfolder)
    files = list(files)

    for file in files:
        filename = textfolder + '//' + file
        try:
            ff = open(filename, 'r', encoding='utf-8') 
            t = BeautifulSoup(ff, 'html.parser') 
            ff.close() 
            textParagraphs = t.findAll('para')
            compareandsave(sampleParagraphs, textParagraphs, 0.15, filename)
        except:
           print('Error occurred in ', filename)

sf = 'C:\\Users\\Lena\\home_tasks\\nabok\\nabok\\Pnin\\pnin_barabtarlo.xml'  #filename of the sample, the full path
tf = 'C:\\Users\\Lena\\home_tasks\\nabok\\nabok\\Pnin\\Pnin_nosik'  #path to the folder with texts
compareTexts(sf, tf)