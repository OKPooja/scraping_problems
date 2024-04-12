from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from pymongo import MongoClient
import configparser

config = configparser.ConfigParser()
config.read('config/database.conf')

mongo_uri = config.get('mongodb', 'uri')

client = MongoClient(mongo_uri)
db = client["projectdb"]
collection = db["trees"]

if client.server_info():
    print("Successfully connected to MongoDB")

service = Service(executable_path='C:\Program Files (x86)\chromedriver.exe')
driver = webdriver.Chrome(service=service)

driver.get('https://leetcode.com/tag/tree/')

WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'reactable-data')))

problem_links = driver.find_elements(By.CSS_SELECTOR, '.reactable-data a')

problem_urls = [link.get_attribute('href') + '/description/' for link in problem_links]

cnt = 0
data = []

for problem_url in problem_urls:
    cnt += 1
    if cnt == 13:
        continue

    driver.get(problem_url)
    parts = problem_url.split('/')

    problem_name = parts[-3]
    problem_name = problem_name.replace("-", " ").capitalize()


    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'elfjS')))
    description_element = driver.find_element(By.CLASS_NAME, 'elfjS')
    
    # prob_details = driver.find_element(By.CLASS_NAME, 'w-full')
    # problem_name = prob_details.find_element(By.TAG_NAME, 'a')
    
    print("Description:", description_element.text)
    print("Problem Name:", problem_name)
    data.append({
        "problem_name": problem_name,
        "problem_description": description_element.text,
        "problem_difficulty": "",
        "solved": False,
        "solution": "",
        "solution_language": "",
        "bookmarked": False,
        "category": "Trees"
    })

    if cnt == 25:
        break

collection.insert_many(data)

driver.quit()
