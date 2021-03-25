import scrapy
from scrapy.http import HtmlResponse
from book_store_parse.items import booksItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']

    def __init__(self, search):
         self.start_urls = [f'http://labirint.ru/search/{search}/']

    def parse(self, response: HtmlResponse):
        books_links = response.xpath('//a[@class="cover"]/@href').getall()
        for link in books_links:
            yield response.follow(link, callback=self.parse_product)
        print()

        next_page = response.xpath('//a[contains(@class,"pagination-next__text")]').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


    def parse_product(self, response: HtmlResponse):
        print()
        book_url = response.url
        book_title = response.xpath('//div[@id="product-title"]/h1/text()').get()
        book_author = response.xpath('//div[contains(@class,"authors")]/a/text()').get()
        price = response.xpath('//span[contains(@class,"buying-price-val-number")]/text()').get()

        if price is None:
            book_price_old = response.xpath('//span[contains(@class,"buying-priceold-val-number")]/text()').get()
            book_price_new = response.xpath('//span[contains(@class,"buying-pricenew-val-number")]/text()').get()
        else:
            book_price_old = None
            book_price_new = price

        book_rate = response.xpath('//div[@id="rate"]/text()').get()
        yield booksItem(url=book_url, title=book_title, author=book_author, price_old=book_price_old, price_new=book_price_new, rate=book_rate)