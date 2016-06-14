import re

dic = {}
f = open('eDIL - Irish Language Dictionary.html', 'r', encoding='utf-8')
text = f.read()
m = re.search('headword_id="(\d*?)">(.*?)</h3>', text)
headword_id = m.group(1)
headword = m.group(2)
tup = (headword, headword_id)
k = re.search('Forms:\n(.*?)</p>', text)
forms = k.group(1)
words = forms.split(', ')
for word in words:
    word = word.strip('\t ')
    dic[word] = tup
print(dic)
print(len(dic))

