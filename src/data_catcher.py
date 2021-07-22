# internal
import settings

# standard
import json
import time

# selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Cars():
    def __init__(self, path):
        self.path = path
        self.cars_and_models = {}
        self.cars_model = []

    def writer(self):
        opts = Options()
        opts.set_headless()
        assert opts.headless
        driver = webdriver.Firefox(options=opts)
        driver.get('https://bsrv.bahman.ir/Part.aspx?company=bm&AspxAutoDetectCookieSupport=1')
        car_finder = driver.find_element_by_id('drpCarType')
        self.cars_name = car_finder.text.split('\n')

        for car in self.cars_name:
            select = WebDriverWait(driver, settings.delay).until(EC.presence_of_element_located((By.ID, 'drpCarType')))
            selecting = Select(select)
            selecting.select_by_visible_text(car)
            time.sleep(0.5)
            car_model = driver.find_element_by_id('drpCarModel')
            carModels = car_model.text.split('\n')[1:]
            self.cars_model.append(carModels)
        counter = 0

        for car in self.cars_name:
            self.cars_and_models[car] = self.cars_model[counter]
            counter += 1
        all_car_and_model = json.dumps(self.cars_and_models, indent=4, ensure_ascii = False)

        with open(self.path, 'w') as f:
            f.write(all_car_and_model)
        
    def reader(self):
        with open(self.path, 'r') as f:
            all_car_and_model = f.read()
            return json.loads(all_car_and_model)            



if __name__ == '__main__':
    car = Cars('data.json')
    car.writer()






