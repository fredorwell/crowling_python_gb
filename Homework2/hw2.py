from bs4 import BeautifulSoup as bs
import requests
import json


input_vacancy = input('Введите вакансию: ')
# input_vacancy = "менеджер"


if True:
    page = 1
    url = 'https://hh.ru'
    params = {'area': '1',
              'fromSearchLine': 'true',
              'st': 'searchVacancy',
              'from': 'suggest_post',
              'text': input_vacancy}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}


    get_param = f"?area=1&fromSearchLine=true&st=searchVacancy&text={input_vacancy}"
    next_page_url = 'https://hh.ru/search/vacancy/' + get_param
    while True:
        html = requests.get(next_page_url, headers=headers)
        soup = bs(html.text, 'html.parser')
        vacancy_block = soup.find('div', {'class': "vacancy-serp"})
        try:
            next_page_url = url + soup.find('a', {'data-qa': "pager-next"})['href']
            print(f'Парсинг страницы: {page}')
        except:
            next_page_url = ''

        if not vacancy_block:
            next_page_url = ''
            break
        vacancy_info = vacancy_block.find_all('div', {'class': 'vacancy-serp-item'})

        vacancy_result = []
        for i in vacancy_info:

            vacancy_data = {}
            info = {}
            vacancy_title = i.find(
                attrs={'class': 'bloko-link HH-LinkModifier HH-VacancyActivityAnalytics-Vacancy'}).text
            vacancy_link = i.find(attrs={'class': 'bloko-link HH-LinkModifier HH-VacancyActivityAnalytics-Vacancy'})[
                'href']
            vacancy_employer = i.find(attrs={'data-qa': 'vacancy-serp__vacancy-employer'})
            if vacancy_employer is None:
                vacancy_employer = None
            else:
                vacancy_employer = vacancy_employer.text


            wage = i.find(attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})

            if wage is None:
                min_wage = None
                max_wage = None
            else:
                wage = wage.text
                if 'от' in wage:
                    wage_split = wage.split()
                    min_wage = ''.join(wage_split[1:3])
                    max_wage = None
                elif 'до' in wage:
                    wage_split = wage.split()
                    min_wage = ''.join(wage_split[1:3])
                    max_wage = None
                else:
                    wage_split = wage.split(sep='-')
                    min_wage = ''.join(wage_split[0].split())
                    max_wage = ''.join(wage_split[1].split()[0:2])
            vacancy_data['vacancy'] = vacancy_title
            vacancy_data['employer'] = vacancy_employer
            vacancy_data['wage'] = wage
            vacancy_data['min_wage'] = min_wage
            vacancy_data['max_wage'] = max_wage
            vacancy_data['url'] = vacancy_link
            vacancy_result.append(vacancy_data)
        # TODO убери заглушку на 5 страниц
        if next_page_url == '' or page == 5:
            break
        page = page + 1

print(f'Найдено вакансий: {len(vacancy_result)}')
print(vacancy_result)

with open("result.json", 'w') as f:
     json.dump(vacancy_result, f, indent=2, ensure_ascii=False)
