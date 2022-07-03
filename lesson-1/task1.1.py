'''
1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
сохранить JSON-вывод в файле *.json.
'''
import json
import requests as requests

user_name = "YuryRazhkov"

response = requests.get(f'https://api.github.com/users/{user_name}/repos')

with open('task1.json', 'w', encoding='utf-8') as f:
    json.dump(response.json(), f)
