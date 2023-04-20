import csv
import requests
from bs4 import BeautifulSoup
import asyncio
#from country_data import countries
import json

count = 0
lastPage = None

async def readPage(page, write, cb):
    global count, lastPage
    response = requests.get(page)
    soup = BeautifulSoup(response.content, 'html.parser')
    if firstItem := soup.select_one('ol li a'):
        currentPage = firstItem.text
        if currentPage == lastPage:
            return cb()
        lastPage = currentPage
    for el in soup.select('ol li a'):
        write(el.text, el['href'])
        count += 1
    cb()

output = csv.writer(open('afro-world-universities.csv', 'w', encoding='utf8'))

async def loadList(dom, country, cb):
    global count
    total = 0
    start = 1
    print(f"[{country}] ", end="")
    while True:
        page = f"http://univ.cc/search.php?dom={dom}&key=&start={start}"
        await readPage(page, lambda name, url: output.writerow([country, name, url]), lambda: None)
        start += 50
        total += count
        print('.', end="")
        if count < 50:
            break
    print(total)
    cb()

#countriesCodes = countries.keys()
with open('codes.json', 'r') as json_file:
    countriesCodes = json.load(json_file)
    for country in countriesCodes:
        if len(country) != 2:
            continue
        dom = "edu" if country == "US" else country
        asyncio.run(loadList(dom.lower(), country, lambda: None))

