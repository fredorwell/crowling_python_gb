import scrapy
from scrapy.http import HtmlResponse
from book_store_parse.items import booksItem


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']

    def __init__(self, search):
        self.start_urls = [f'https://book24.ru/search/?q={search}']

    def parse(self, response: HtmlResponse):
        books_links = response.xpath('//a[contains(@class,"book-preview__title-link")]//@href').getall()

        for link in books_links:
            yield response.follow(link, callback=self.parse_product)
        print()

        next_page = response.xpath('//a[contains(@class,"catalog-pagination__item _text js-pagination-catalog-item")]//@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response: HtmlResponse):
        print()
        book_url = response.url
        book_title = response.xpath('//h1/text()').get()
        book_rate = response.xpath('//div[contains(@class, "rating__rate-value")]//text()').get()
        book_author = response.xpath('//a[@itemprop="author"]//text()').get()
        book_price_old = response.xpath('//div[contains(@class,"item-actions__price-old")]//text()').get()
        book_price_new = response.xpath('//b[@itemprop="price"]/text()').get()
        print()
        yield booksItem(url=book_url, title=book_title, author=book_author, price_old=book_price_old, price_new=book_price_new, rate=book_rate)