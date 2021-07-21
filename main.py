# internal
import persian_character

# standard
import hashlib
import sqlite3
import time
import csv

# selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# BeautifulSoup and Requests
from bs4 import BeautifulSoup


# catch all of table
def table_catcher(src):
    pass

# handeling ajax
def wait_for_ajax(driver, selector):
    return WebDriverWait(driver, delay).until(EC.presence_of_element_located(selector))

# get all number of pages
def number_of_page():
    try:
        number = driver.find_element_by_id('DataPager1_ctl00_TotalPagesLabel')
        return int(number.text)
    except:
        return False

def wait_for_page_loading(src):
    soup = BeautifulSoup(src, 'html.parser')
    display = soup.find('div', attrs={'id':'LoadingTem'})
    style = display.get('style')
    return style

driver = webdriver.Firefox()
driver.get('https://bsrv.bahman.ir/Part.aspx?company=bm')

# catching car list
car_finder = driver.find_element_by_id('drpCarType')
cars_name = car_finder.text.split('\n')

delay = 60

for car in cars_name:
    """Selecting all car type"""
    select = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'drpCarType')))
    selecting = Select(select)
    selecting.select_by_visible_text(car)
    car_model = driver.find_element_by_id('drpCarModel')
    carModels = car_model.text.split('\n')[1:]

    if len(carModels) != 0:
        for model in carModels:
            """Selecting all car model"""
            mselect = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'drpCarModel')))
            mselecting = Select(mselect)
            mselecting.select_by_visible_text(model)

            for char in persian_character.persian_ascii_letters:
                """Inserting all character to input tag"""
                char_input = driver.find_element_by_id('txtPartName')
                char_input.send_keys(char)
                WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID,'btnSearch'))).click()
                try:
                    while wait_for_page_loading(driver.page_source) != 'display: none':
                        time.sleep(2)
                        continue
                except:
                    time.sleep(0.2)
                num_page = number_of_page()

                if num_page > 1:
                    for page in range(num_page):
                        """Scraping all pages"""
                        print(f'I\'m in page: {page + 1}')

#                        if page == (num_page - 1):
#                            break
#                        else:
                        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, 'dtPager$ctl02$ctl00'))).click()
                        page_src = driver.page_source
                        soup = BeautifulSoup(page_src, 'html.parser')
                        btn_disable = int(soup.find(class_='btn disabled').text)

                        while True:
                            page_src = driver.page_source
                            soup = BeautifulSoup(page_src, 'html.parser')
                            btn_disable_ = int(soup.find(class_='btn disabled').text)
                            time.sleep(0.5)
                            if btn_disable != btn_disable_ or page == (num_page - 1):
                                break
                else:
                    pass # TODO: compelete this

                # clearing the input tag
                char_input = driver.find_element_by_id('txtPartName')
                char_input.clear()


