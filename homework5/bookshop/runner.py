from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from book_store_parse.spiders.book24 import Book24Spider
from book_store_parse.spiders.labirint import LabirintSpider
from book_store_parse import settings

if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    # search = input('Введите автора или книгу для поиска: ')
    search = 'Омер Майк'
    process.crawl(Book24Spider, search=search)
    process.crawl(LabirintSpider, search=search)
    process.start()