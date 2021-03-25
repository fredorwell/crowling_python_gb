# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from book_store_parse.items import booksItem
from pymongo import MongoClient
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
DB_NAME = 'books'

class book_store_parsePipeline:
    def __init__(self):
        self.mongo_client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
        self.db = self.mongo_client[DB_NAME]
    print()
    def process_labirint(self, item, spider):
        collection = self.db[spider.name]
        collection.insert_one(item)
        # collection.update_one({'url': item['url']}, item, upsert=True)
        print()
        return item