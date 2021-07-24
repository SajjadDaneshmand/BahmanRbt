# internal
import rtools
import settings
import settings as se
from data_catcher import Cars

# standard
import time
import csv
import sys

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd

class Robot():
    def __init__(self, url):
        self.url = url

    def fetch(self, company, model, character, page=None):
        pass


class BahmanRobot(Robot):
    def __init__(self, url):
        self.url = url
        # needed var
        self.drpCarType_element = (By.ID, 'drpCarType')
        self.drpCarModel_element = (By.ID, 'drpCarModel')
        self.input_char_element = (By.ID, 'txtPartName')
        self.search_btn = (By.ID, 'btnSearch')
        self.next_page_btn = (By.NAME, 'dtPager$ctl02$ctl00')

        # create driver
        self.driver = rtools.driver(self.url)

    def fetch(self, company, model, character, page=None):
        page = str(page)
        rtools.selector(self.driver, self.drpCarType_element, company)
        time.sleep(0.2)
        rtools.selector(self.driver, self.drpCarModel_element, model)
        rtools.char_sender(self.driver,self.input_char_element,character)
        rtools.btn_clicker(self.driver, self.search_btn)
        try:
            while rtools.wait_for_page_loading(self.driver.page_source) != 'display: none':
                time.sleep(0.5)
        except:
            time.sleep(0.2)
        self.max_page = rtools.number_of_page(self.driver)
        if page:
            if page == None or page == '1':
                form = f'{settings.FILES_FOLDER}{company}-{model}-({1 if page == None else page})-{character}.csv'
                rtools.table_catcher(self.driver.page_source, form)
            else:
                return rtools.paging(self.driver.page_source, page)

r = BahmanRobot(settings.URL)
print(r.fetch('Dignity', 'Dignity', 'h', 5))