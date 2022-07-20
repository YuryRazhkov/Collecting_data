# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancies_spider

    def process_item(self, item, spider):

        item['salary'] = self.process_salary(item['salary'])

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def process_salary(self, salary):
        salary_min = None
        salary_max = None

        for i in range(len(salary)):
            salary[i] = salary[i].replace(u'\xa0', u'')

        if salary[0] == ' до ':
            salary_max = salary[1]
        elif len(salary) == 3 and salary[0].isdigit():
            salary_max = salary[0]
        elif salary[0] == 'от ':
            salary_min = salary[1]
        elif len(salary) > 3 and salary[0].isdigit():
            salary_min = salary[0]
            salary_max = salary[2]

        return [salary_min, salary_max]
