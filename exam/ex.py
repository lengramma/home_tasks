import pandas as pd 
import csv

df = pd.read_excel("C:\\Users\\Lena\\home_tasks\\exam\\tables\\source_post1950_wordcount.xls") 
data = df.as_matrix().tolist() 
print(len(data))

res = [] 

def splitline(line, num): 
    result = [] 
    number = 50000 
    l1 = line.copy() 
    for i in range(num): 
        l = line.copy() 
        if l1[22] > number: 
            l1[22] -= number 
            l[22] = number 
        else: 
            l[22] = l1[22] 
    result.append(l) 
    return result 


for i in range(len(data)): 
    try:
        if 100000 > int(data[i][22]) > 70000: 
            line = data[i] 
            data.remove(line) 
            r = splitline(line, 2) 
            res.append(r) 
        elif int(data[i][22]) > 100000: 
            line = data[i] 
            data.remove(line) 
            r = splitline(line, 3) 
            res.append(r) 
        else: 
            res.append(data[i])
    except:
        pass
        
print(len(data))

f = open('C:\\Users\\Lena\\home_tasks\\exam\\tables\\new_csv.csv', 'w', encoding='utf-8')


writer = csv.writer(f)
writer.writerows(data)

    

'''

f = open('C:\\Users\\Lena\\home_tasks\\exam\\tables\\source_post1950_wordcount.xls', 'r', encoding='utf-8')
'''