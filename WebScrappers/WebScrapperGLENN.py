import requests
import csv
from bs4 import BeautifulSoup
import re

path = '../Article_Bodies/'

url = ("")
# 46 pages

reg = re.compile("[^a-zA-Z0-9' ]+")

pn = 1
ide = 1
a = []
stories = []
bodies = []
divs = []
print 'start.....'
while pn <= 35:
    url = ("http://www.glennbeck.com"+ "/page/" + str(pn) + "/?s=gun+control&format=read")
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    div = soup.find_all('div', {'class': 'articles'})
    for i in div:
        divs.append(i)
    pn += 1
print 'done pages.....onto appending'
for x in divs:
    a.append(x.find('a').get('href').encode('ascii','ignore'))
print 'done appending.......onto links'
for lin in a:
    newr = requests.get(lin)
    nsoup = BeautifulSoup(newr.content, "lxml")
    articleBod = nsoup.find('div', {'class': 'article-text col-lg-8 col-md-7 col-sm-6 col-xs-12'})
    try:
        articleBody = articleBod.find_all('p')
    except:
        continue
    articleHeader = nsoup.find('h3', {'class': 'article-headline'})

    try:
        artH = articleHeader.text.encode('ascii', 'ignore')
    except:
        pass

    item = [artH, ide, 0]

    s = ''
    for body in articleBody:
        s += body.text.encode('ascii', 'ignore') + '\n'
    bod = [reg.sub(' ', s), 0]

    stories.append(item)
    bodies.append(bod)
    ide += 1
    print 'doing links.....', ide
print '-'*96
print '.....writing to csv'

# with open('Glenn_heads.csv', 'w') as f:
#     fileW = csv.writer(f)
#     fileW.writerow(['Head', 'BodyID', 'Value'])
#     for line in stories:
#         fileW.writerow(line)

with open(path + 'con2vec_Against.csv', 'w') as f:
    fileW = csv.writer(f)
    fileW.writerow(['Body', 'Stance'])
    for line in bodies:
        fileW.writerow(line)
print 'Done!'
