from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import json
import time

class Recipe:
    def __init__(self, title, extra, labels, allergens, duration, difficulty, kcal, ingredients, image_url, pdf_url):
        self.title = title
        self.extra = extra
        self.labels = labels
        self.allergens = allergens
        self.duration = duration
        self.difficulty = difficulty
        self.kcal = kcal
        self.ingredients = ingredients
        self.image_url = image_url
        self.pdf_url = pdf_url

data = []

for week in range(1, 52 + 1):

    if week == 37: continue

    browser = webdriver.Chrome()
    browser.maximize_window()

    if week < 10:
        week = "0" + str(week)

    url = 'https://www.hellofresh.be/menus/2017-W' + str(week) + '?locale=nl-BE'
    browser.get(url)

    wrapper = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'web-1eniyeh')))

    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'web-26xi0f')))
    time.sleep(1)
    children = wrapper.find_elements(By.CLASS_NAME, 'web-26xi0f')

    time.sleep(2)

    for child in children:
        child.click()
        time.sleep(.5)

        window_before = browser.window_handles[0]

        browser.find_element(By.CLASS_NAME, 'web-k008qs').click()

        window_after = browser.window_handles[1]
        browser.switch_to.window(window_after)

        time.sleep(.5)

        #OPBOUWEN VAN JSON OBJECT
        title = browser.find_element(By.CSS_SELECTOR, '.cSyxkC').text #OK
        extra = browser.find_element(By.CSS_SELECTOR, '.fsDgUC').text #OK
        
        try:
            labels_wrapper = browser.find_element(By.XPATH, '//*[@id="page"]/div[2]/div[4]/div/div[2]/div[2]/div[1]/div[2]')
            labels = labels_wrapper.find_elements(By.XPATH, '*')

            final_labels = [] #OK

            for i in range(1, len(labels)):
                final_labels.append(labels[i].find_elements(By.XPATH, '*')[len(labels[i].find_elements(By.XPATH, '*')) - 1].text)
        except:
            print("No labels have been found")
        
        try:
            allergens_wrapper = browser.find_element(By.XPATH, '//*[@id="page"]/div[2]/div[4]/div/div[2]/div[2]/div[1]/div[3]')
            allergens = allergens_wrapper.find_elements(By.XPATH, '*')

            final_allergens = [] #OK

            for i in range(1, len(allergens)):
                final_allergens.append(allergens[i].find_elements(By.XPATH, '*')[len(allergens[i].find_elements(By.XPATH, '*')) - 1].text)
        except:
            print("No allergens have been found")

        duration = browser.find_element(By.CSS_SELECTOR, '.kTbyZf > .fFYngF').text #OK
        difficulty = browser.find_element(By.CSS_SELECTOR, '.fXPEkQ > .fFYngF').text #OK

        browser.find_element(By.XPATH, '//*[@id="page"]/div[2]/div[4]/div/div[3]/div[2]/div[2]/div/div[2]/div[1]/div/button[2]').click()
        kcal = browser.find_element(By.XPATH, '//*[@id="page"]/div[2]/div[4]/div/div[3]/div[2]/div[2]/div/div[2]/div[2]/div[2]/span[2]').text #OK

        ingredients_wrapper = browser.find_element(By.XPATH, '//*[@id="page"]/div[2]/div[4]/div/div[3]/div[1]/div/div[2]/div[2]')
        ingredients = ingredients_wrapper.find_elements(By.XPATH, '*')

        final_ingredients = [] #OK

        for i in range(len(ingredients)):
            final_ingredients.append(browser.find_elements(By.CLASS_NAME, 'czDpDG')[i].text)

        image_url = browser.find_element(By.XPATH, '//*[@id="page"]/div[2]/div[3]/img').get_attribute('src') #OK
        pdf_url = browser.find_element(By.CSS_SELECTOR, 'div.sc-5b343ba0-0.geLvPU > a').get_attribute('href') #OK

        data.append(Recipe(title, extra, final_labels, final_allergens, duration, difficulty, kcal, final_ingredients, image_url, pdf_url))
        browser.close()
        browser.switch_to.window(window_before)

    json_string = json.dumps([ob.__dict__ for ob in data], indent=4)
    with open('old_data_be_2017.json', 'w') as outfile:
        outfile.write(json_string)

    browser.quit()