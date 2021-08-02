# internal
import rtools
import settings
from exceptions import NumberOutOfRange
# standard
import time  # TODO: adding options for sys
import sys

from selenium.webdriver.common.by import By


class Robot:
    def __init__(self, url):
        self.url = url

    def fetch(self, *args, **kwargs):
        pass


class BahmanRobot(Robot):
    def __init__(self, url):
        super().__init__(url)
        # needed var
        self.new_car_element = 'b9a53759-12fe-4ea2-85ab-a8b2a4692d58'
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
        if company == 'NEW':
            rtools.select_by_value(self.driver, self.drpCarModel_element, self.new_car_element)
        else:
            rtools.selector(self.driver, self.drpCarModel_element, model)
        rtools.char_sender(self.driver, self.input_char_element, character)
        rtools.btn_clicker(self.driver, self.search_btn)
        # wait for page loading
        try:
            while rtools.style_checker(self.driver.page_source) != 'display: none':
                time.sleep(0.5)
        except AttributeError:
            time.sleep(0.3)

        max_page = rtools.number_of_page(self.driver)
        if page is None or page == '1':
            return rtools.table_catcher(self.driver.page_source)

        elif int(page) > max_page or int(page) <= 0:
            raise NumberOutOfRange(f'page number should between 1 and {max_page}')

        else:
            btn = rtools.paging(self.driver.page_source, page)
            if btn:
                rtools.btn_clicker(self.driver, (By.NAME, btn))
                page_now = rtools.find_btn_disable(self.driver.page_source)
                while True:
                    time.sleep(0.5)
                    page_now_ = rtools.find_btn_disable(self.driver.page_source)
                    if page_now != page_now_:
                        break
                rtools.char_remover(self.driver, self.input_char_element)
                return rtools.table_catcher(self.driver.page_source)

            else:
                btn = rtools.paging(self.driver.page_source, page)
                checker = 1
                while btn is False:
                    if checker == 1:
                        rtools.btn_clicker(self.driver, (By.NAME, 'dtPager$ctl01$ctl05'))
                    else:
                        rtools.btn_clicker(self.driver, (By.NAME, rtools.dot_finder(self.driver.page_source)))
                    checker += 1
                    page_now = rtools.find_btn_disable(self.driver.page_source)
                    while True:
                        time.sleep(0.5)
                        page_now_ = rtools.find_btn_disable(self.driver.page_source)
                        if page_now != page_now_:
                            break
                    btn = rtools.paging(self.driver.page_source, page)
                    if btn:
                        if btn != 'btn disabled':
                            rtools.btn_clicker(self.driver, (By.NAME, btn))
                            page_now = rtools.find_btn_disable(self.driver.page_source)
                            while True:
                                time.sleep(0.5)
                                page_now_ = rtools.find_btn_disable(self.driver.page_source)
                                if page_now != page_now_:
                                    break
                rtools.char_remover(self.driver, self.input_char_element)
                return rtools.table_catcher(self.driver.page_source)

    def next_page_fetch(self, company, model, character):
        rtools.selector(self.driver, self.drpCarType_element, company)
        time.sleep(0.2)
        if company == 'NEW':
            rtools.select_by_value(self.driver, self.drpCarModel_element, self.new_car_element)
        else:
            rtools.selector(self.driver, self.drpCarModel_element, model)
        rtools.char_sender(self.driver, self.input_char_element, character)
        rtools.btn_clicker(self.driver, self.search_btn)
        page = 'بعدی'
        # wait for page loading
        try:
            while rtools.style_checker(self.driver.page_source) != 'display: none':
                time.sleep(0.3)
        except AttributeError:
            time.sleep(0.2)
        max_page = rtools.number_of_page(self.driver)
        for num in range(max_page):
            yield rtools.table_catcher(self.driver.page_source)
            btn = rtools.paging(self.driver.page_source, page)
            page_now = rtools.find_btn_disable(self.driver.page_source)
            try:
                rtools.btn_clicker(self.driver, (By.NAME, btn))
            except Exception as e:
                print(e)
                sys.exit()
            while True:
                time.sleep(0.2)
                page_now_ = rtools.find_btn_disable(self.driver.page_source)
                if page_now != page_now_ or page_now_ == max_page:
                    break
        rtools.char_remover(self.driver, self.input_char_element)
        self.driver.get(settings.URL)
        return


def main():
    robot = BahmanRobot(settings.URL)
    robot.fetch('Dignity', 'Dignity', 'ا', 18)


if __name__ == '__main__':
    main()
