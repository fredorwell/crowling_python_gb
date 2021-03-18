import requests
from lxml import html
from pprint import pprint
from pymongo import MongoClient

MONGO_URI = "127.0.0.1:27017"
MONGO_DB = "news_parse_hw4"
ua = {'User-Agent': 'Mozilla/5.0 (Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

def parse_yandex_news():
    url = 'https://yandex.ru/news'
    response = requests.get(f'{url}', headers=ua).text
    r = html.fromstring(response)
    news_block = r.xpath("//a[contains(@href,'rubric=index') and @class='mg-card__link']/ancestor::article")
    news_list = []
    for i in news_block:
        news = {}
        news['news_title'] = i.xpath(".//h2[contains(@class, 'mg-card__title')]/text()")
        news['news_url'] = i.xpath(".//a[contains(@class, 'mg-card__link')]/@href")
        news['news_source'] = i.xpath(".//a[contains(@class, 'mg-card__source-link')]/text()")
        news_date = i.xpath(".//span[contains(@class, 'mg-card-source__time')]/text()")
        if "вчера" in news_date[0]:
            news['news_date'] = news_date
        else:
            news_date = " ".join(["сегодня", str(news_date[0])])
            news['news_date'] = news_date
        news_list.append(news)
    return news_list

def parse_lenta_news():
    url = 'https://lenta.ru'
    response = requests.get(f'{url}', headers=ua).text
    r = html.fromstring(response)
    news_block = r.xpath("//div[contains(@class,'b-yellow-box__wrap')]/div[contains(@class,'item')]")
    news_list = []
    for i in news_block:
        news = {}
        news['news_title'] = i.xpath(".//a/text()")
        news_url = i.xpath(".//a/@href")
        news_url = "".join([str(url), str(news_url[0])])
        news['news_url'] = news_url
        news['news_source'] = "lenta.ru"
        # У ленты дата публикации находится внутри новости, по этому тут доп. реквест
        dop_response = requests.get(news_url, headers=ua).text
        dop_r = html.fromstring(dop_response)
        news['news_date'] = dop_r.xpath("//div[contains(@class,'b-topic__info')]//time[contains(@class,'g-date')]/text()")
        news_list.append(news)

    return news_list

# def parse_mail_news():
#     url = 'https://news.mail.ru/'
#     response = requests.get(f'{url}', headers=ua).text
#     r = html.fromstring(response)
#     news_list = []
#     # главная новость
#     # main_news_block = r.xpath("//td[contains(@class,'daynews__main')/@href]")
#     # main_news_title = main_news_block.xpath(".//a/@href")
#     return news_list


result_yandex_news = parse_yandex_news()
pprint(result_yandex_news)
result_lenta_news = parse_lenta_news()
pprint(result_lenta_news)
# result_mail_news = parse_mail_news()
# pprint(result_mail_news)
with MongoClient(MONGO_URI) as client:
    db = client[MONGO_DB]
    news_list = db.news_list_result
    news_list.drop()
    news_list.insert_many(result_yandex_news)
    news_list.insert_many(result_lenta_news)