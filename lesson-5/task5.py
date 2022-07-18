import time

from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

user_login = 'study.ai_172@mail.ru'
user_password = 'NextPassword172#'
base_url = 'https://mail.ru/'

client = MongoClient('localhost', 27017)

db = client['mail']
msgs_collection = db['msgs']

s = Service('../chromedriver')
driver = webdriver.Chrome(service=s)

driver.get(base_url)
time.sleep(2)
button_login = driver.find_element(By.XPATH,
                                   "//button[@class='resplash-btn resplash-btn_primary resplash-btn_mailbox-big svelte-vawtzz']")
button_login.send_keys(Keys.ENTER)
time.sleep(2)

iframe = driver.find_element(By.XPATH, "//iframe[contains(@class, '__iframe')]")
driver.switch_to.frame(iframe)
time.sleep(2)
login = driver.find_element(By.XPATH, ".//input[@name = 'username']")

login.send_keys(user_login)
login.send_keys(Keys.ENTER)
time.sleep(2)
password = driver.find_element(By.NAME, 'password')
password.send_keys(user_password)
password.send_keys(Keys.ENTER)
time.sleep(2)

driver.switch_to.default_content()
time.sleep(2)
msg = driver.find_element(By.CLASS_NAME, 'js-letter-list-item')
msg.click()

time.sleep(2)
# next_btn = driver.find_element(By.XPATH, "//span[contains(@title, 'Следующее')]")

while True:
    try:
        next_btn = driver.find_element(By.CLASS_NAME, 'button2_arrow-down')
        time.sleep(2)
        msg_dict = {}

        msg_author = driver.find_element(By.CLASS_NAME, 'letter-contact')
        msg_date = driver.find_element(By.XPATH, '//div[@class="letter__date"]')
        msg_subj = driver.find_element(By.XPATH, '//h2')
        msg_text = driver.find_element(By.CLASS_NAME, 'letter__body')

        msg_dict['msg_author'] = msg_author.text
        msg_dict['msg_date'] = msg_date.text
        msg_dict['msg_subj'] = msg_subj.text
        msg_dict['msg_text'] = msg_text.text
        time.sleep(2)

        msgs_collection.insert_one(msg_dict)

        next_btn.click()

        time.sleep(2)
    except:
        print('end pars')

client.close()
