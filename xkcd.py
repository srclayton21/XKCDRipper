from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import requests

# Set up
url = "https://xkcd.com"
toFind = 'https:/imgs.xkcd.com/'
html = urlopen(url).read()
soup = BeautifulSoup(html, features = "html.parser")

# Extract URL tag from root of website to get permalink of newest comic
pattern = re.compile(r'\d+')
newUrl = str(soup.find(property="og:url"))
newestXKCDList = pattern.findall(newUrl)
newestXKCD = str(newestXKCDList[0])
print('Latest XKCD number: ' + str(newestXKCD))

# Recursively gather all comic permalinks 
linkArray = []
for i in range(int(newestXKCD)):
#for i in range(10):
    nextComic = url + "/" + str(i) + "/"
    response = requests.get(nextComic)
    localSoup = BeautifulSoup(response.content, features="html.parser")
    links = localSoup.findAll('a')
    for link in links:
        if 'imgs.xkcd.com' in link.get('href'):
         pattern = re.compile(r'<[^>]+>')
         print("Found permalink: " + re.sub(pattern, '', str(link)))
         linkArray.append(re.sub(pattern, '', str(link)))

    
# print every image in linkArray
i = 1
for link in linkArray:
    print('Downloading image: ' + link)
    response = requests.get(link).content
    f = open(str(i) + '.png', 'wb')
    f.write(response)
    f.close()
    i = i+1

print('Fetched ' + str(len(linkArray)) + ' images')

