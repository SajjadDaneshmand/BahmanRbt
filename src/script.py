# internal
import settings
from data_catcher import Cars
from robots import BahmanRobot
import time

car_class = Cars(settings.DATA_FILE)
# car_class.writer()
data = car_class.reader()
next_ = 'بعدی'
robot = BahmanRobot(settings.URL)
for key, values in data.items():
    # Selecting all car type
    for value in values:
        # catch all model of cars
        for char in settings.persian_ascii_letters:
            # select all characters
            num = 0
            for page in robot.fetch(key, value, char, next_):
                num += 1
                print(f'{key}--{value}--{char}--{num}')
                print(page)


