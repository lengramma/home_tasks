from bs4 import BeautifulSoup
import re


def readtable(lines, sep='\t'):
    result = []
    li = list(filter(lambda x: x[0] != '#', lines))
    for line in li:
        l = line.split('\t')
        result.append(l)

    return result


def sentstoxml(lines, res):
    if len(lines) == 0:
        return

    startind = 0
    val = lines[0][0]
    for i in range(len(lines)):
        if len(lines[i]) > 1:
            if str(lines[i][0]) != val:
                res.append(senttoxml(lines[startind:i], res))
                startind = i
                if startind == len(lines):
                    val = '-1'
                else:
                    val = lines[startind][0]

    res.append(senttoxml(lines[startind:len(lines)], res))

    return res


def senttoxml(lines, res):
    if len(lines) == 0:
        return BeautifulSoup.new_tag(res, "se")

    se = BeautifulSoup.new_tag(res, "se")

    startind = 0
    val = lines[0][1]
    for i in range(len(lines)):
        if lines[i][1] != val:
            se.append(wordtoxml(lines[startind:i], res))
            startind = i
            if startind == len(lines):
                val = '-1'
            else:
                val = lines[startind][1]
    se.append(wordtoxml(lines[startind:len(lines)], res))

    return se


def wordtoxml(lines, res):
    if len(lines) == 0:
        return BeautifulSoup.new_tag(res, "se")

    w = BeautifulSoup.new_tag(res, "w")

    for i in range(len(lines)):
        try:
            w.append(antoxml(lines[i], res))
        except:
            pass

    w.append(lines[0][4])

    return w


def antoxml(line, res):

    ana = BeautifulSoup.new_tag(res, "ana")

    ana['lex'] = line[9]

    morph = re.search('[^A-Z_0-9 ].*', line[13]).group()
    morph = re.sub('^ +(?=[^\s])', '', morph)
    morph = re.sub(' syll.', '', morph)
    if len(morph) != 0:
        ana['morph'] = morph
    else:
        ana['morph'] = ''
    gr = re.search('[A-Z_0-9 ]*', line[13]).group().lower()
    if gr[-1] == ' ':
        gr = gr[:-1]
    ana['gr'] = gr

    ana['trans'] = line[10]

    return ana

def start(xmlfilename, prsfilename):
    data = BeautifulSoup("lxml")
    data.append(BeautifulSoup.new_tag(data, "body"))

    prslines = []

    with open(prsfilename, "r", encoding='utf-8') as file:
        prslines = file.read().split('\n')

    res = sentstoxml(readtable(prslines), data.body)

    with open(xmlfilename, "wb") as file:
        file.write(res.prettify("utf-8"))

