# http://kissmanga.com/MangaList
import cfscrape
from pymongo import MongoClient
import json
import scrapy
from scrapy import Request, Field, Item
import re




client = MongoClient('mongodb://vosoditdeus:root@ds163034.mlab.com:63034/manga')
db = client.manga


class MyItem(Item):
    name = Field()
    link = Field()


class MangaListSpider(scrapy.Spider):
    name = "mangas"
    allowed_domains = ['kissmanga.com']

    start_urls = [
        # 'https://bato.to/search',
        'http://kissmanga.com/MangaList',
    ]

    def start_requests(self):
        cf_requests = []
        for url in self.start_urls:
            token, agent = cfscrape.get_tokens(url, 'Your prefarable user agent, _optional_')
            cf_requests.append(Request(url=url,
                                       cookies=token,
                                       headers={'User-Agent': agent}))
        return cf_requests

    def parse(self, response):
        items = response.xpath('//tr[@class="odd"]//td[position() mod 2 = 1]/a/@href').extract()
        data = [{}]
        test = []
        # db.Chats_FWM.insert_one({
        #     "chat_name": update.message.chat_id,
        #     "message": message,
        #     "type": 'farewell'
        # })
        for item in items:
            # data.append({"title": item.split("/Manga/")[1],
            #             "url": item})
            db.mangas.insert_one({
                "title": item.split("/Manga/")[1],
                "url": item
            })


        # with open('mangas__1.json', 'a') as outfile:
        #     json.dump(data, outfile, indent=4)
        next_page = response.css('div.pagination a::attr(href)').extract()
        page_counter = int(re.search(r'\d+', next_page[-1]).group())
        for url in self.start_urls:
            token, agent = cfscrape.get_tokens(url, 'Your prefarable user agent, _optional_')
            for page in range(2, page_counter):
                url_second = '%s/MangaList?page=%s' % (url, page)
                yield Request(url_second,
                          cookies=token,
                          headers={'User-Agent': agent})
