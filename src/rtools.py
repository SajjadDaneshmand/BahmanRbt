# selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from exceptions import InternetConnectionError
from bs4 import BeautifulSoup
import pandas as pd
import settings

def selector(driver, selector, text):
    element = WebDriverWait(driver, settings.delay).until(EC.presence_of_element_located(selector))
    selecting = Select(element)
    selecting.select_by_visible_text(text)

def driver(url):
    # opts = Options()
    # opts.set_headless()
    # assert opts.headless
    # driver = webdriver.Firefox(options=opts)
    driver = webdriver.Firefox()
    driver.set_page_load_timeout(40)
    try:
        driver.get(url)
    except TimeoutException:
        raise InternetConnectionError('please check your connection')
    return driver

def char_sender(driver, selector, character):
    element = WebDriverWait(driver, settings.delay).until(EC.presence_of_element_located(selector))
    element.send_keys(character)

def btn_clicker(driver, selector):
    element = WebDriverWait(driver, settings.delay).until(EC.presence_of_element_located(selector))
    element.click()

def number_of_page(driver):
    try:
        number = driver.find_element_by_id('DataPager1_ctl00_TotalPagesLabel')
        return int(number.text)
    except:
        return False

def table_catcher(src,path):
    code = []
    number = []
    name = []
    price = []
    soup = BeautifulSoup(src, 'html.parser')
    table = soup.find('table')
    header = table.thead.tr.text.strip().split('\n')
    body = table.tbody
    for row in body.find_all('tr'):
        row_list = row.text.strip().split('\n')
        code.append(row_list[0])
        number.append(row_list[1])
        name.append(row_list[2])
        price.append(row_list[3])
    frame = {
        header[0]:code,
        header[1]:number,
        header[2]:name,
        header[3]:price
    }
    dataframe = pd.DataFrame(frame)
    dataframe.to_csv(path)

def paging(src, page):
    values = []
    soup = BeautifulSoup(src, 'html.parser')
    pages = soup.find('span', attrs={'id':'dtPager'})
    values.append(str(pages.span.text.strip()))
    for value in pages.find_all('input'):
        val = value.get('value').strip()
        values.append(val) # TODO: create this by dict
    for i in values:
        if str(page) == i:
            return True
        else:
            return False

def wait_for_page_loading(src):
    soup = BeautifulSoup(src, 'html.parser')
    display = soup.find('div', attrs={'id':'LoadingTem'})
    style = display.get('style')
    return style

