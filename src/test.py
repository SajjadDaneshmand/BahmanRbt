from robots import BahmanRobot
from bs4 import BeautifulSoup
from datetime import datetime
import settings
import time

robot = BahmanRobot(settings.URL)
robot.fetch('Dignity', 'Dignity', 'ا')
page_source = robot.page_source()
soup = BeautifulSoup(page_source, 'html.parser')
item_label = soup.find('span', attrs={'id': 'DataPager1_ctl00_TotalItemsLabel'})

while True:
    robot.fetch('Dignity', 'Dignity', 'ا')
    page_source = robot.page_source()
    soup = BeautifulSoup(page_source, 'html.parser')
    item_label_ = soup.find('span', attrs={'id': 'DataPager1_ctl00_TotalItemsLabel'})
    if item_label != item_label_:
        print(f'at time: {datetime.now().time()} bahman site has an update. the old row was: {item_label}\nand '
              f'now the row are: {item_label_}')
        item_label = item_label_
        time.sleep(3)

