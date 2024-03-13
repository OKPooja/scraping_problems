from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from pymongo import MongoClient
import configparser

config = configparser.ConfigParser()
config.read('config/database.conf')

mongo_uri = config.get('mongodb', 'uri')

client = MongoClient(mongo_uri)
db = client["leetcode_problems"]
collection = db["sorting"]

if client.server_info():
    print("Successfully connected to MongoDB")

service = Service(executable_path='C:\Program Files (x86)\chromedriver.exe')
driver = webdriver.Chrome(service=service)

driver.get('https://leetcode.com/tag/sorting')

start_time = time.time()
time.sleep(5)

problems = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/table/tbody')

data = []
cnt = 0
for tr in problems.find_elements(By.XPATH, './tr'):  
    tds = [item.text for item in tr.find_elements(By.XPATH, './td')]  
    data.append({
        "problem": tds[2],
        "difficulty": tds[3],
        "acceptance": tds[4]
    })
    # print(tds[0] + " " + tds[2] )
    cnt += 1
    if(cnt == 250):
        break
    print(cnt)

collection.insert_many(data)

end_time = time.time()

print("Time required to copy the data: {:.2f} seconds".format(end_time - start_time))

driver.quit()