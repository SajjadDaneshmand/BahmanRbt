# internal
import settings
from data_catcher import Cars

# standard
import time


# selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from bs4 import BeautifulSoup
import pandas as pd


# catch all of table
def table_catcher(src, path):
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
        header[0]: code,
        header[1]: number,
        header[2]: name,
        header[3]: price
    }
    dataframe = pd.DataFrame(frame)
    dataframe.to_excel(path)


# get all number of pages
def number_of_page():
    try:
        number = driver.find_element_by_id('DataPager1_ctl00_TotalPagesLabel')
        return int(number.text)
    except:
        return False


def wait_for_page_loading(src):
    pars = BeautifulSoup(src, 'html.parser')
    display = pars.find('div', attrs={'id': 'LoadingTem'})
    style = display.get('style')
    return style


driver = webdriver.Firefox()
driver.set_page_load_timeout(40)
driver.get(settings.URL)

car_class = Cars(settings.DATA_FILE)
data = car_class.reader()


for car in data:
    """Selecting all car type"""

    for model in list(data.values()):
        if len(model) != 0:
            for cary in model:
                """Selecting all car model"""

                for char in settings.persian_ascii_letters:
                    """Inserting all character to input tag"""
                    select = WebDriverWait(driver, settings.delay).until(ec.presence_of_element_located((By.ID, 'drpCarType')))
                    selecting = Select(select)
                    selecting.select_by_visible_text(car)
                    time.sleep(1)
                    model_selector = WebDriverWait(driver, settings.delay).until(ec.presence_of_element_located((By.ID, 'drpCarModel')))
                    model_selecting = Select(model_selector)
                    model_selecting.select_by_visible_text(cary)
                    counter = 1
                    char_input = driver.find_element_by_id('txtPartName')
                    char_input.send_keys(char)
                    WebDriverWait(driver, settings.delay).until(ec.presence_of_element_located((By.ID, 'btnSearch'))).click()

                    while wait_for_page_loading(driver.page_source) != 'display: none':
                        time.sleep(0.5)

                    num_page = number_of_page()
                    counter += 1
                    if num_page > 1:
                        for page in range(num_page):
                            """Scraping all pages"""
                            print(f'I\'m in page: {page + 1}')

                            WebDriverWait(driver, settings.delay).until(ec.presence_of_element_located((By.NAME, 'dtPager$ctl02$ctl00'))).click()
                            page_src = driver.page_source
                            soup = BeautifulSoup(page_src, 'html.parser')
                            btn_disable = int(soup.find(class_='btn disabled').text)
                            form = f'{settings.FILES_FOLDER}{car}-{cary}-({page + 1})-{char}.xlsx'
                            table_catcher(driver.page_source, form)

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
                        form = f'{settings.FILES_FOLDER}{car}-{cary}-(1)-{char}.xlsx'
                        table_catcher(driver.page_source, form)

                    # clearing the input tag
                    char_input = driver.find_element_by_id('txtPartName')
                    char_input.clear()


