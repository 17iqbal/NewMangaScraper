import cfscrape
import json
import scrapy
import re
from pymongo import MongoClient
client = MongoClient('mongodb://vosoditdeus:root@ds163034.mlab.com:63034/manga')
db = client.manga


from scrapy import Request, Field, Item


class MyItem(Item):
    name = Field()
    link = Field()


class MangaListSpider(scrapy.Spider):
    name = "mangas_info"
    allowed_domains = ['kissmanga.com']
    start_urls = [
        'http://kissmanga.com/',
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
        token, agent = cfscrape.get_tokens('http://kissmanga.com/', 'Your prefarable user agent, _optional_')
        mangas = db.mangas.find()
        for manga in mangas:
            manga_title = manga.title
            manga_url = manga.url
            manga_genres = []
            manga_name = 'None'
            manga_artist = []
            divs = response.xpath('//div[@class="barContent"]')
            for p in divs.xpath('.//p/a/@href'):  # extracts all <p> inside
                data = p.extract()
                arr = data.split()
                for item in arr:
                    if item.find("/Manga/") != -1:
                        if item.split('/Manga/')[1]:
                            manga_name = item.split('/Manga/')[1]
                    if item.find("/Genre/") != -1:
                        if item.split('/Genre/')[1]:
                            manga_genres.append(item.split('/Genre/')[1])
                    if item.find("/AuthorArtist/") != -1:
                        if item.split('/AuthorArtist/')[1]:
                            manga_artist.append(item.split('/AuthorArtist/')[1])
            manga_info = {'Name': manga_name, 'Genres': manga_genres, 'Artist': manga_artist}
            # with open('mangas_info_2.json', 'a') as file:
            #     json.dump(manga_info, file)
            for manga_url in manga.next().url:
                url = 'http://kissmanga.com/%s' % manga_url
                yield Request(url,
                                  cookies=token,
                                  headers={'User-Agent': agent})
