from bs4 import BeautifulSoup
import re


def sentolines(el, sentnum=1, wordnum=1, sent_pos=''):
    result = []
    line = []
    line.append(str(sentnum))  # 1 column, sentence number
    line.append(str(wordnum))  # 2 column, word number
    line.append('')  # 3 column, lang

    text = el.text
    text = text.replace('\t', '')
    text = text.replace('\n', '')
    text = text.replace(' ', '')

    # 4 column, graph
    if text[0].isupper():
        line.append('cap')
    else:
        line.append('')

    line.append(text)  # 5 column, word
    line.append('')  # 6 column, indexword

    anals = el.findAll('ana')

    line.append(str(len(anals)))  # 7 column, nvars

    # not sure, how to do it
    line.append(str(len(anals)))  # 8 column, nlems

    ind = 1
    for ana in anals:
        l = line.copy()
        l.append(str(ind))  # 9 column, nvar
        ind +=1

        l.append(ana.get('lex',''))  # 10 column lex
        l.append(ana.get('trans',''))  # 11 column trans
        l.append(ana.get('trans_ru',''))  # 12 column trans

        gram = ana.get('gr')
        if ',' in gram:
            lex, gram = gram.split(',', 1)
        else:
            lex = gram
            gram = ''
        gram = gram.upper()
        gram = re.sub('[^A-Z|0-9]', ' ', gram)
        if ana.get('morph'):
            gram = gram + ' ' + ana.get('morph')

        l.append(lex)  # 12 column lex
        l.append(gram)  # 13 column gram

        l.append('')  # 14 column flex

        l.append('')  # 15 column punctl
        l.append('')  # 16 column punctr
        l.append(sent_pos)  # 17 column sent_pos

        result.append(l)

    return result


def xmltoprs(data, sep='\t'):
    sentences = data.findAll('se') 
    table = []
    for i in range(len(sentences)):
        words = sentences[i].findAll('w')  
        for j in range(len(words)):
            sent_pos = ''
            if j == 0:
                sent_pos = 'bos'
            elif j == len(words) - 1:
                sent_pos = 'eos'
            try:
                table.append(sentolines(words[j],i + 1, j + 1, sent_pos))
            except:
                pass

    result = []

    for t in table:
        for tt in t:
            line = ""
            for l in tt:
                line += str(l) + sep
            result.append(line)

    return result


def start(xmlfilename, prsfilename):
    data = BeautifulSoup(open(xmlfilename, 'r', encoding='utf-8'), 'html.parser')
    res = xmltoprs(data)
    headers = '#sentno	#wordno	#lang	#graph	#word	#indexword	#nvars	#nlems	#nvar	#lem	#trans	#trans_ru	#lex	#gram	#flex	#punctl	#punctr	#sent_pos'
    with open(prsfilename, "w", encoding='utf-8') as file:
        file.write(headers)
        for line in res:
            file.write(line + '\n')
