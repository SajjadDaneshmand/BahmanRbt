# standard
import time
import csv
import string

# selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select

# bs4
from bs4 import BeautifulSoup


def table_cather(src):
    soup = BeautifulSoup(src, 'html.parser')
    table = soup.find_all()


driver = webdriver.Firefox()
driver.get('https://bsrv.bahman.ir/Part.aspx?company=bm')

select = Select(driver.find_element_by_id('drpCarType'))
car_finder = driver.find_element_by_id('drpCarType')
cars_name = car_finder.text.split('\n')

for car in cars_name:
    select = Select(driver.find_element_by_id('drpCarType'))
    select.select_by_visible_text(car)
    time.sleep(0.5)
    car_model = driver.find_element_by_id('drpCarModel')
    carModels = car_model.text.split('\n')[1:]
    if len(carModels) != 0:
        for model in carModels:
            mselect = Select(driver.find_element_by_id('drpCarModel'))
            mselect.select_by_visible_text(model)
            time.sleep(0.3)
            num_and_letters = string.ascii_lowercase + string.digits
            for char in num_and_letters:
                char_input = driver.find_element_by_id('txtPartName')
                char_input.send_keys(char)
                clicker = driver.find_element_by_id('btnSearch')
                clicker.click()
                time.sleep(10)
                char_input = driver.find_element_by_id('txtPartName')
                char_input.clear()


