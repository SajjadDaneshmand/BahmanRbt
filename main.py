# internal
import persian_character

# standard
import time
import csv

# selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# BeautifulSoup
from bs4 import BeautifulSoup


# catch all of table
def table_catcher(src):
    pass

# handeling ajax
def wait_for_ajax(driver, selector):
    return WebDriverWait(driver, 60).until(EC.presence_of_element_located(selector))

# get all number of pages
def number_of_page():
    try:
        number = driver.find_element_by_id('DataPager1_ctl00_TotalPagesLabel')
        return int(number.text)
    except:
        return False

driver = webdriver.Firefox()
driver.get('https://bsrv.bahman.ir/Part.aspx?company=bm')

# catching car list
car_finder = driver.find_element_by_id('drpCarType')
cars_name = car_finder.text.split('\n')

for car in cars_name:
    """Selecting all car type"""
    select = wait_for_ajax(driver, (By.ID, 'drpCarType'))
    selecting = Select(select)
    selecting.select_by_visible_text(car)
    car_model = driver.find_element_by_id('drpCarModel')
    carModels = car_model.text.split('\n')[1:]
    print(car_model)

    if len(carModels) != 0:
        for model in carModels:
            """Selecting all car model"""
            mselect = wait_for_ajax(driver, (By.ID, 'drpCarType'))
            mselecting = Select(mselect)
            mselecting.select_by_visible_text(model)

            for char in persian_character.ppe_characters:
                """Inserting all character to input tag"""
                char_input = wait_for_ajax(driver, (By.ID, 'txtPartName'))
                char_input.send_keys(char)
                clicker = wait_for_ajax(driver, (By.ID, 'btnSearch'))
                clicker.click()
                num_page = number_of_page()

                if num_page:
                    for page in range(num_page):
                        """Scraping all pages"""
                        print(f'I\'m in page: {page + 1}')
                        next = wait_for_ajax(driver, (By.ID, 'dtPager$ctl02$ctl00'))
                        next.click()

                # clearing the input tag
                char_input = driver.find_element_by_id('txtPartName')
                char_input.clear()


