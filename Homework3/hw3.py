from pymongo import MongoClient
from hw2 import parsing_hh as parse_hh

# Первое задание
def put_mongo(inp_data):
    MONGO_URI = "127.0.0.1:27017"
    MONGO_DB = "hh_parse_hw3"
    with MongoClient(MONGO_URI) as client:
        db = client[MONGO_DB]
        vacancy_list = db.vacancy_list_result
        vacancy_list.drop()
        vacancy_list.insert_many(inp_data)
    print(f'Данные в базе {MONGO_DB} перезаписаны ')

# Второе задание
def filter_mongo(inp_data):
    MONGO_URI = "127.0.0.1:27017"
    MONGO_DB = "hh_parse_hw3"
    with MongoClient(MONGO_URI) as client:
        db = client[MONGO_DB]
        vacancy_list = db.vacancy_list_result
        wage_fil = inp_data
        if wage_fil == "1":

            for i in vacancy_list.find({"avg_wage": {"$type": 10}}):
                print(i)
        else:
            for i in vacancy_list.find({"avg_wage": {"$gte": wage_fil}}):
                print(i)


inp_vac = input('Введите вакансию: ')
parse_result = parse_hh(inp_vac)
print(f'Найдено вакансий: {len(parse_result)}')
print(parse_result)
option = input('Вы хотите перезаписать данные (1) или отсеить по минимальной зп (2): ')
if option == "1":
    put_mongo(parse_result)
elif option == "2":
    min_wage = input('Введите минимальную зарплату(1 - если вывести вакансии без зп): ')
    filter_mongo(min_wage)