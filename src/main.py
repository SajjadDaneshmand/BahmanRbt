# internal
import settings
from data_catcher import cars

# standard
import sqlite3
import time
import csv

# selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# BeautifulSoup and Requests
from bs4 import BeautifulSoup


# catch all of table
def table_catcher(src):
    soup = BeautifulSoup(src, 'html.parser')
    

# handeling ajax
def wait_for_ajax(driver, selector):
    return WebDriverWait(driver, settings.delay).until(EC.presence_of_element_located(selector))

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
driver.get(settings.URL)

car = cars(settings.DATA_FILE)
data = car.reader()


for car in data:
    """Selecting all car type"""
    
    for model in list(data.values()):
        if len(model) != 0:
            for car in model:
                """Selecting all car model"""
                
                for char in settings.persian_ascii_letters:
                    """Inserting all character to input tag"""
                    select = WebDriverWait(driver, settings.delay).until(EC.presence_of_element_located((By.ID, 'drpCarType')))
                    selecting = Select(select)
                    selecting.select_by_visible_text(car)
                    mselect = WebDriverWait(driver, settings.delay).until(EC.presence_of_element_located((By.ID, 'drpCarModel')))
                    mselecting = Select(mselect)
                    mselecting.select_by_visible_text(car)
                    counter = 1
                    char_input = driver.find_element_by_id('txtPartName')
                    char_input.send_keys(char)
                    WebDriverWait(driver, settings.delay).until(EC.presence_of_element_located((By.ID,'btnSearch'))).click()
                    try:
                        while wait_for_page_loading(driver.page_source) != 'display: none':
                            time.sleep(2)
                    except:
                        time.sleep(0.2)

                    num_page = number_of_page()
                    counter += 1
                    if num_page > 1:
                        for page in range(num_page):
                            """Scraping all pages"""
                            print(f'I\'m in page: {page + 1}')

                            WebDriverWait(driver, settings.delay).until(EC.presence_of_element_located((By.NAME, 'dtPager$ctl02$ctl00'))).click()
                            page_src = driver.page_source
                            soup = BeautifulSoup(page_src, 'html.parser')
                            btn_disable = int(soup.find(class_='btn disabled').text)

                            while True:
                                page_src = driver.page_source
                                soup = BeautifulSoup(page_src, 'html.parser')
                                btn_disable_ = int(soup.find(class_='btn disabled').text)
                                time.sleep(0.5)
                                if btn_disable != btn_disable_:
                                    break
                                elif page == (num_page - 1):
                                    driver.get(settings.URL)
                                    break
                    else:
                        pass # TODO: compelete this

                    # clearing the input tag
                    char_input = driver.find_element_by_id('txtPartName')
                    char_input.clear()


