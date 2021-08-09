# selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec

from exceptions import InternetConnectionError
from bs4 import BeautifulSoup
import settings
import time


def selector(driver, selector, text):
    element = WebDriverWait(driver, settings.delay).until(ec.presence_of_element_located(selector))
    selecting = Select(element)
    selecting.select_by_visible_text(text)


def select_by_value(driver, selector, value):
    element = WebDriverWait(driver, settings.delay).until(ec.presence_of_element_located(selector))
    selecting = Select(element)
    selecting.select_by_value(value)


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
    element = WebDriverWait(driver, settings.delay).until(ec.presence_of_element_located(selector))
    element.send_keys(character)


def char_remover(driver, selector):
    element = WebDriverWait(driver, settings.delay).until(ec.presence_of_element_located(selector))
    element.clear()


def btn_clicker(driver, selector):
    element = WebDriverWait(driver, settings.delay).until(ec.presence_of_element_located(selector))
    element.click()


def number_of_page(driver):
    time.sleep(0.6)
    try:
        number = driver.find_element_by_id('DataPager1_ctl00_TotalPagesLabel')
        return int(number.text)
    except:
        return False


def table_catcher(src):
    info = []
    row_info = []
    soup = BeautifulSoup(src, 'html.parser')
    try:
        table = soup.find('table')
        body = table.tbody
        for rows in body.find_all('tr'):
            for row in rows.find_all('td'):
                txt = row.text.replace('\n', ' ')
                row_info.append(txt)
            info.append(row_info)
            row_info = []
        return info
    except AttributeError:
        return False


def paging(src, page):
    time.sleep(0.3)
    values = {}
    soup = BeautifulSoup(src, 'html.parser')
    pages = soup.find('span', attrs={'id': 'dtPager'})
    values[str(pages.span.text.strip())] = 'btn disabled'
    for value in pages.find_all('input'):
        val = value.get('value').strip()
        val_name = value.get('name').strip()
        values[val] = val_name
    for i in values:
        if page == i:
            return values.get(i)
    return False


def find_btn_disable(src):
    time.sleep(0.3)
    soup = BeautifulSoup(src, 'html.parser')
    btn_disable = int(soup.find(class_='btn disabled').text.strip())
    time.sleep(0.2)
    return btn_disable


def style_checker(src):
    soup = BeautifulSoup(src, 'html.parser')
    display = soup.find('div', attrs={'id':'LoadingTem'})
    style = display.get('style')
    return style


def dot_finder(src):
    soup = BeautifulSoup(src, 'html.parser')
    pages = soup.find('span', attrs={'id': 'dtPager'})
    checker = False
    for value in pages.find_all('input'):
        val = value.get('value').strip()
        if val == '...':
            if checker is True:
                val_name = value.get('name').strip()
                return val_name
            else:
                checker = True
