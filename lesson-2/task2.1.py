'''
Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы получаем должность)
с сайтов HH(обязательно) и/или Superjob(по желанию). Приложение должно анализировать несколько страниц сайта
(также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
Наименование вакансии.
Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
Ссылку на саму вакансию.
Сайт, откуда собрана вакансия. (можно прописать статично hh.ru или superjob.ru)
'''

import re
from pprint import pprint

import requests
from bs4 import BeautifulSoup

vacancy = 'python junior developer'
link = 'https://hh.ru/search/vacancy'
pages_to_scrap = 5
params = {
    'search_field': ['name', 'description'],
    'text': vacancy,
    # 'salary': '',
    # 'clusters': 'true',
    # 'ored_clusters': 'true',
    # 'enable_snippets': 'true',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0'
}

vacancys_dict = {}
n = 1
for i in range(0, int(pages_to_scrap)):
    print(f'scrapping page {i + 1}')
    params['page'] = i
    html = requests.get(link, params=params, headers=headers)
    site = re.search(r'https://(\S*?)/', link)[1]
    soup = BeautifulSoup(html.text, "html.parser")
    vac_request = soup.find_all('div', 'vacancy-serp-item-body')
    for i in vac_request:
        a = str((i.select('a')))
        name_vac = re.search(r'target=\"_blank\">(.*?)</a>, <', a)[1]
        link_vac = re.search(r'href=\"(\S*)\"', a)[1]
        info_dict = {}
        info_dict['name_vac'] = name_vac
        info_dict['link_vac'] = link_vac
        info_dict['site'] = site
        salary = re.search(r'vacancy-serp__vacancy-compensation\">(.*?)</span>', str(i))
        if salary == None:
            salary_min = None
            salary_max = None
            curancy = None
            info_dict['salary_min'] = salary_min
            info_dict['salary_max'] = salary_max
            info_dict['curancy'] = curancy
        elif salary[1][0:2] == 'от':
            curancy = salary[1].split('-->')[-1]
            salary = re.search(r'от <!-- -->(.*)<!-- --> <!-- -->', str(salary[1]))
            salary_min = salary[1]
            salary_max = None
            salary_min = int(''.join(salary_min.split()))
            info_dict['salary_min'] = salary_min
            info_dict['salary_max'] = salary_max
            info_dict['curancy'] = curancy
        elif salary[1][0:2].isnumeric():
            curancy = salary[1].split('-->')[-1]
            salary = salary[1].split(' – ')
            salary_min = salary[0]
            salary_max = (salary[1].split(' ')[0])
            salary_min = int(''.join(salary_min.split()))
            salary_max = int(''.join(salary_max.split()))
            info_dict['salary_min'] = salary_min
            info_dict['salary_max'] = salary_max
            info_dict['curancy'] = curancy
        elif salary[1][0:2] == 'от':
            curancy = salary[1].split('-->')[-1]
            salary = re.search(r'до <!-- -->(.*)<!-- --> <!-- -->', str(salary[1]))
            salary_min = None
            salary_max = salary[1]
            salary_min = int(''.join(salary_min.split()))
            info_dict['salary_min'] = salary_min
            info_dict['salary_max'] = salary_max
            info_dict['curancy'] = curancy
        else:
            info_dict['salary_min'] = 'hz'
            info_dict['salary_max'] = 'hz'
            info_dict['curancy'] = 'hz'

        vacancys_dict[n] = info_dict
        n += 1

pprint(vacancys_dict)
