import re
from bs4 import BeautifulSoup

class word:
    def __init__(self, old_form="", lex="", transcr="", sem=""):
        self.old_form = old_form
        self.lex = lex
        self.transcr = transcr
        self.sem = sem
        
def dict_list (dict):
    listOfWords = []
    for line in dict:
        if re.search('^#', line) == None:
            a = re.search('^(.*?)\s(.*?)\s\[(.*?)\]\s/(.*)/$', line)
            old_form = a.group(1)
            lex = a.group(2)
            transcr = a.group(3)
            sem = a.group(4)
            sem = re.sub('/', '; ', sem)
            lemma = word(old_form, lex, transcr, sem)
            listOfWords.append(lemma)
        
    return(listOfWords)

def find_word(string, listOfWords):
    subDict = list(filter(lambda x: x.lex[0] == string[0], listOfWords))
    subDict = sorted(subDict, key=lambda x: -len(x.lex))
    analys = []
    maxLen = 0
    if len(subDict) == 0:
        return [False, string[0]]
    try:
        for i in subDict:
            if len(string) >= len(i.lex) >= maxLen:
                index = len(i.lex)
                str = string[:index]
                if i.lex == str:
                    analys.append(i)
                    maxLen = len(i.lex)
        return[True, analys, maxLen]
    except:
        return[False, string[0]]
    
    
def split_and_save(sentence, listOfWords, new):
    while len(sentence) > 0:
        res = find_word(sentence, listOfWords)
        word = BeautifulSoup.new_tag(new, "w")
        if res[0] == True:
            
            for i in res[1]:
                an = BeautifulSoup.new_tag(new, "ana")
                an['lex'] = i.lex
                an['transcr'] = i.transcr
                an['sem'] = i.sem
                word.append(an)
            if res[2] < len(sentence) and res[2] > 0:
                sentence = sentence[res[2]:]
            elif res[2] == 0:
                an = BeautifulSoup.new_tag(new, "ana")
                an['lex'] = sentence[0]
                word.append(an)
                sentence = sentence[1:] 
            else:
                sentence = ''
            new.append(word)
        else:
            if 1 < len(sentence):
                an = BeautifulSoup.new_tag(new, "ana")
                an['lex'] = sentence[0]
                word.append(an)
                sentence = sentence[1:]
            else:
                sentence = ''


filedictionary = 'C:\\Users\\Lena\\home_tasks\\chinese\\cedict_ts.u8'
filetext = 'C:\\Users\\Lena\\home_tasks\\chinese\\stal.xml'
 
result = BeautifulSoup(features='xml')
result.append(BeautifulSoup.new_tag(result, "head"))
result.append(BeautifulSoup.new_tag(result, "body"))

dict = open(filedictionary, 'r', encoding='utf-8')
listOfWords = dict_list(dict)

stal = open(filetext, 'r', encoding='utf-8')
d = BeautifulSoup(stal, 'html.parser')
sentences = d.findAll('se')
for sent in sentences:
    xsent = BeautifulSoup.new_tag(result, "se")
    xsent['sentence'] = sent.string
    try:
        split_and_save(sent.string, listOfWords, xsent)
        result.body.append(xsent)
    except:
        pass
    
l = result.prettify("utf-8")
with open('C:\\Users\\Lena\\home_tasks\\chinese\\stal_parsed.xml', "wb") as file:
    file.write(l)
