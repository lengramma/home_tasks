import pymysql
import csv

conn = pymysql.connect(host = 'localhost', user = 'guest1', passwd = '', db = 'guest1_grammatchikova_dbl', charset = 'utf8')
cur = conn.cursor()

def create_table():
    cur.execute('CREATE TABLE `text` (`id_text` int(10), `id_student` int(10), `title` varchar(255), `key_words` varchar(255), `id_supervisor` int(10), `year` int(10), PRIMARY KEY(`id_text`)) DEFAULT CHARSET = utf8;')
    cur.execute('CREATE TABLE `teachers` (`id_supervisor` int(10), `name` varchar(255), `title` varchar(255), `department` varchar(255),  `courses` varchar(255), PRIMARY KEY(`id_supervisor`)) DEFAULT CHARSET = utf8;')
    cur.execute('CREATE TABLE `students` (`id_student` int(10), `name` varchar(255), `department` varchar(255),  `entry_year` int(10), PRIMARY KEY(`id_student`)) DEFAULT CHARSET = utf8;')
   
def join_strings(csvFile, name):
    reader = csv.reader(csvFile, delimiter='\t')
    string1 = '(`' + '`, `'.join(next(reader)) + '`)'
    string2 = ''
    # print(string1)
    for row in reader:
        line = '(' + ', '.join(row) + ')'
        if string2 != '':
            string2 = string2 + ', ' + line
        else:
            string2 = line
    # print(string2)
    insert_into(string1, string2, name)
    

def insert_into(string1, string2, name):
    cur.execute('INSERT INTO ' + '`' + name + '`' + ' ' + string1 + ' VALUES ' + string2 + ';')

text = open('text.txt', 'r', encoding='utf-8')
teachers = open('teachers.txt', 'r', encoding='utf-8')
students = open('students.txt', 'r', encoding='utf-8')

create_table()
join_strings(text, 'text')
join_strings(teachers, 'teachers')
join_strings(students, 'students')

conn.commit()




