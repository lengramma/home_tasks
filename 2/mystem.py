'''
Скрипт обрабатывает скачанные файлы майстемом и записывает их в двух форматах: plain text и XML

'''
import os
import re

for root, dirs, files in os.walk('C:\\Users\\Lena\\home_tasks\\2\\files_aux'):
    for filename in files:
        command = "C:\\Users\\Lena\\Desktop\\other\\mystem-3.0-win7-64bit\\mystem.exe -cid " + root + "\\" + filename + " " + re.sub("files_aux", "files_mystem", root) + "\\" + filename[:-4] + "_mystem.txt"
        command_xml = "C:\\Users\\Lena\\Desktop\\other\\mystem-3.0-win7-64bit\\mystem.exe -cid --format xml " + root + "\\" + filename + " " + re.sub("files_aux", "files_mystem_xml", root) + "\\" + filename[:-4] + ".xml"
        
        print(command)
        os.makedirs(re.sub("files_aux", "files_mystem", root), exist_ok=True)
        os.system(command)
        
        print(command_xml)
        os.makedirs(re.sub("files_aux", "files_mystem_xml", root), exist_ok=True)
        os.system(command_xml)