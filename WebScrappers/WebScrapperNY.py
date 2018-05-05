import requests
import csv
from bs4 import BeautifulSoup
import re

path = '../Article_Bodies/'

url = ("https://www.newyorker.com/search/q/gun%20control")
# 128 pages /page/str(pn)/r,n pn = page number

reg = re.compile("[^a-zA-Z0-9' ]+")

pn = 2
ide = 485
a = []
stories = []
bodies = []
divs = []
print 'start....'
while pn <= 128:
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    div = soup.find_all('div', {'class': 'River__riverItemContent___2hXMG'})
    for i in div:
        divs.append(i)
    url = ("https://www.newyorker.com/search/q/gun%20control" + "/page/" + str(pn) + "/r,n")
    pn += 1
print 'done.........moving to append'
for x in divs:
    a.append(x.find('a', {'class': 'Link__link___3dWao '}).get('href').encode('ascii','ignore'))
print 'done.........moving to links'
for lin in a:
    newr = requests.get('https://www.newyorker.com' + lin)
    nsoup = BeautifulSoup(newr.content, "lxml")
    articleBody = nsoup.find_all('div', {'class': 'ArticleBody__articleBody___1GSGP'})
    articleHeader = nsoup.find('h1', {'class': 'ArticleHeader__hed___GPB7e'})

    try:
        artH = articleHeader.text.encode('ascii', 'ignore')
    except:
        pass

    item = [artH, ide, 1]

    s = ''
    for body in articleBody:
        s += body.text.encode('ascii', 'ignore') + '\n'

    bod = [reg.sub(' ', s), 1]


    stories.append(item)
    bodies.append(bod)
    ide += 1
    print 'getting links.....', ide
print '-'*96
print 'done......writing to csv'
# with open('NewYorker_heads.csv', 'w') as f:
#     fileW = csv.writer(f)
#     fileW.writerow(['Head', 'BodyID', 'Value'])
#     for line in stories:
#         fileW.writerow(line)

with open(path + 'con2vec_For.csv', 'a') as f:
    fileW = csv.writer(f)
    # fileW.writerow(['Body', 'Stance'])
    for line in bodies:
        fileW.writerow(line)
print 'done'
