from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time

locale = 'be' #values: (be - hellofresh.be, us - hellofresh.com)
pages  = 65   #values: (number - amount of pages loaded) (amount of recipes = pages * 8)

class Recipe:
    def __init__(self, image_url, title, extra, duration, difficulty, categories, source):
        self.image_url = image_url
        self.title = title
        self.extra = extra
        self.duration = duration
        self.difficulty = difficulty
        self.categories = categories
        self.source = source

url_be = "https://www.hellofresh.be/recipes/populairste-recepten"
url_us = "https://www.hellofresh.com/recipes/most-popular-recipes"

browser = webdriver.Chrome()
browser.get(url_be)

for i in range(pages):
    buttons = browser.find_elements(By.CLASS_NAME, 'web-3205mz')
    for button in buttons:
        if button.get_attribute('innerHTML') == 'Laad meerdere':
            try:
                button.click()
                time.sleep(1)
            except:
                print("De popup is er!")

parent   = browser.find_element(By.XPATH, '//*[@id="page"]/main/div[1]/div[6]/div/div[3]/div[1]/div')
children = parent.find_elements(By.XPATH, '*')

data = []

for child in children:
    image_url = child.find_element(By.CSS_SELECTOR, '.css-1rj0z6b').get_attribute('src') #OK
    title     = child.find_element(By.CSS_SELECTOR, '.web-1ocn5zm > span').get_attribute('innerHTML') #OK
    extra     = child.find_element(By.CSS_SELECTOR, '.web-1ocn5zm').text.splitlines()[1] #OK
    source    = child.find_element(By.CSS_SELECTOR, '.jZJUzF').get_attribute('href') #OK
    
    details  = child.find_element(By.CSS_SELECTOR, '.web-1ocn5zm + div').text.replace("|", "").split("\n")
    a = details[len(details) - 1].split("  ")

    duration = a[0] #OK
    difficulty = a[1] #OK

    arr = []
    for i in range(len(details) - 1):
        arr.append(details[i].strip())
    categories = arr #OK

    data.append(Recipe(image_url, title, extra, duration, difficulty, categories, source))
    

json_string = json.dumps([ob.__dict__ for ob in data], indent=4)
with open('data_be.json', 'w') as outfile:
    outfile.write(json_string)