import re  

dic = {}
d = open('alphabet.txt', 'r', encoding = 'utf-8')
for line in d:
    a = re.match('(.?)\t.*?\t(.*?)\t', line)
    dic[a.group(1)] = a.group(2)
d.close()

f = open('text.txt', 'r', encoding = 'utf-8')
n = open('text_trans.txt', 'w', encoding = 'utf-8')
for line in f:
    string = ''
    for letter in line:
        try:
            a = re.sub(letter, dic[letter], letter)
        except KeyError:
            a = letter
        string = string + a
    n.write(string)
n.close()


