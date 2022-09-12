from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotSelectableException, ElementClickInterceptedException, TimeoutException
import time
import random
import csv
import pandas as pd


chrome_dpath = "C:/Users/Haris/Webdrivers/chromedriver.exe"
# Path to where I have installed the webdriver.

driver = webdriver.Chrome(chrome_dpath)
driver.implicitly_wait(20)

# class= a-button-input celwidget

driver.get("https://www.amazon.co.uk/")
time.sleep(5)  # Let the user see something!

accept_cokkies = driver.find_element(By.XPATH, '//*[@id="sp-cc-accept"]')
accept_cokkies.click()

search_inputs = ["cat food", "dog food", "car parts", "gym clothes men"]
sample_input = random.choice(search_inputs)

print(sample_input)
s_input = driver.find_element(By.ID, 'twotabsearchtextbox')
s_input.send_keys(sample_input)

go_button = driver.find_element(By.ID, 'nav-search-submit-text')
go_button.click()

s_item_info = []

list_items = wait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))

for item in list_items:
    try:
        ## Finding Product Title
        try:
            s_item_title = driver.find_element(By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[3]/div/div/div/div/div/div/div[2]/div[2]/h2/a/span')
            print(s_item_title.text)
        except Exception as e:
            print(e)
            s_item_title = driver.find_element(By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[3]/div/div/div/div/div/div/div[2]/div[2]/h2/a/span')
            print(s_item_title.text)

        ## Link to Item Description.
        s_item_desc = driver.find_element(By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[3]/div/div/div/div/div/div/div[2]/div[2]/h2/a').get_attribute("href")
        print(s_item_desc)

        ## Finding Product Price.
        s_item_price = driver.find_element(By.CLASS_NAME, 'a-price')
        print(s_item_price.text)

        ## Finding Product Ratings
        s_item_ratings = driver.find_element(By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[3]/div/div/div/div/div/div/div[2]/div[3]/div/span[2]/a/span')
        print(s_item_ratings.text)
        s_item_info.append({
            "title": s_item_title.text,
            "Desc": s_item_desc,
            "Price": s_item_price.text,
            "Ratings": s_item_ratings.text,
        })

        print(s_item_info)

        time.sleep(3)
        print(" writing to csv")
        df = pd.DataFrame(data=s_item_info)
        df.to_csv("scraped_product_info.csv", index=False)

    except:
        raise TimeoutException()
        print("exception")



# driver.implicitly_wait(3)
# url_list = []
# for i in range(int(num_page.text)):
#         page = i + 1
#         url_list.append(driver.current_url)
#         driver.implicitly_wait(4)
#         click_next = driver.find_element(By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[69]/div/div/span/a[3]')
#         print("Page " + str(page) + " grabbed")


driver.quit()