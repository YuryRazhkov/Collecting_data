import re

import requests
from lxml import html
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client['news_db']
news = db['news']

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0'}
url = 'https://lenta.ru'
session = requests.Session()
response = session.get(url, headers=headers)
dom = html.fromstring(response.text)

source = url
title = dom.xpath(
    "//a[contains(@class, 'card-mini _longgrid')]//div[@class='card-mini__text']//span[@class='card-mini__title']//text()")
link = dom.xpath("//a[contains(@class, 'card-mini _longgrid')]/@href")
date_time = dom.xpath(
    "//a[contains(@class, 'card-mini _longgrid')]//div[@class='card-mini__text']//div[@class='card-mini__info']//text()")

print(len(title) == len(link) == len(date_time))

for i in range(len(title)):
    if link[i][:5] != 'https':
        link_d = f'{source}{link[i]}'
        source_d = source[8:]
    else:
        link_d = link[i]
        source_d = re.search(r'//(.+?\..+?)/', link[i])[1]

    news.insert_one({
        'source': source_d,
        'title': title[i],
        'link': link_d,
        'date_time': date_time[i]
    })
for item in news.find({}):
    print(item)
client.close()

# sudo mongoexport --db news_db -c news --out task4.json
