import urllib.request
import re
import sys

report = open('report.csv', 'w', encoding='utf-8')

def FindPages(page):
    addresses = re.findall('\"(http://vechufa\.ru[^"]*?\.html)\"', page)
    for i in addresses:
        if i not in all_addresses:
            all_addresses.append(i)
    
def DownloadPage(url):
    con = urllib.request.urlopen(url)
    page = con.read()
    page = page.decode("cp1251")
    url_name = re.sub('/', '_', re.findall('/.*?$', url)[0])
    url_name = re.sub(':', '-', url_name)
    text = open(url_name, 'w', encoding='utf-8')
    report.write('\t' + url_name + '\n')
    print(url_name)
    text.write(page)
    FindPages(page)

if len(sys.argv) < 2:
    print('Usage: get_data.py <your URL>')
    quit()
url = sys.argv[1]

pages_number = int(input('Введите количество страниц: '))
all_addresses = []
dl_addresses = []
all_addresses.append(url)

for address in all_addresses:
    if len(dl_addresses) < pages_number:
        if address not in dl_addresses:
            report.write(address)
            DownloadPage(address)
            dl_addresses.append(address)
            print(len(dl_addresses))
    else:
        quit()

    



