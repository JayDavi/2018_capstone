import requests
import csv
from bs4 import BeautifulSoup
import re

path = '../Article_Bodies/'

url = ('https://newsapi.org/v2/everything?'
        'q=Gun+Control&'
        'sources=bbc-news,cnn&'
        'page=1&'
        'apikey=5461c5876a0b4717b62219cd40a151a5')

r = requests.get(url)
res = r.json()

reg = re.compile("[^a-zA-Z0-9' ]+")

ide = 1
b = 2
stories = []
bodies = []
print 'start....'
while res['articles'] != []:
    for i in xrange(len(res['articles'])):
        head = res['articles'][i]['title'].encode('ascii','ignore')
        items = [head, ide, 1]
        source = res['articles'][i]['source']['name'].encode('ascii','ignore')
        artURL = res['articles'][i]['url']
        r = requests.get(artURL)
        soup = BeautifulSoup(r.content, "lxml")

        if source == 'CNN':
            body = soup.find_all('div', {'class': 'zn-body__paragraph'})
            s = ''
            for i in body:
                s+= i.text + '\n'

        elif source == 'BBC News':
            body = soup.find_all('div', {'property': 'articleBody'})
            s = ''
            for i in body:
                got = i.find_all('p')
                for j in got:
                    s += j.text + '\n'
        # print '-'*100
        # print head, '\n'

        # print source
        # print s
        # print s
        # print '-'*100
        bod = [reg.sub(' ', s.encode('ascii','ignore')), 1]
        # print head
        # print 'Body at: ', artURL
        # print '\n'
        stories.append(items)
        bodies.append(bod)
        ide += 1
        print 'doing links....', ide

    url = ('https://newsapi.org/v2/everything?'
            'q=Gun+Control&'
            'sources=bbc-news,cnn&'
            'page='+ str(b) +'&'
            'apikey=5461c5876a0b4717b62219cd40a151a5')
    r = requests.get(url)
    res = r.json()
    b += 1
print 'writting to file...'
# with open('CNNAndBBC_heads.csv', 'w') as f:
#     fileW = csv.writer(f)
#     fileW.writerow(['Head', 'BodyID', 'Value'])
#
#     for line in stories:
#         fileW.writerow(line)

with open(path + 'con2vec_For.csv', 'w') as f:
    fileW = csv.writer(f)
    fileW.writerow(['Body', 'Stance'])

    for line in bodies:
        fileW.writerow(line)
print ide
print 'Done!'
