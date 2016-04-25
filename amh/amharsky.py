import re

dic = {}
f = open('alphabet.txt', 'r', encoding='utf-8')

n = 0
consonants = []
for line in f:
    a = line.split()
    if n == 0:
        vowels = a[0:]
        n += 1
        continue
    consonants.append(a[0])
    m = 0
    for letter in a[1:]:
        dic[letter] = a[0] + vowels[m]
        m += 1

f.close()

d = open('text.txt', 'r', encoding = 'utf-8')
n = open('text_trans.txt', 'w', encoding = 'utf-8')
for line in d:
    string = ''
    for letter in line:
        try:
            k = re.sub(letter, dic[letter], letter)
        except KeyError:
            k = letter
        string = string + k
    n.write(string)
n.close()