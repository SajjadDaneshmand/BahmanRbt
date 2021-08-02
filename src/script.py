# internal
import settings
import database_function as db
from data_catcher import Cars
from robots import BahmanRobot

# mysql_connector_python
from mysql.connector import connect
import mysql


def scrap(data):
    for key, values in data.items():
        # Selecting all car type
        if not key == 'NEW':
            for value in values:
                # catch all model of cars
                for char in settings.persian_ascii_letters:
                    # select all characters
                    num = 0
                    for info in robot.next_page_fetch(key, value, char):
                        num += 1
                        yield value, info
        else:
            for char in settings.persian_ascii_letters:
                # select all characters
                for info in robot.next_page_fetch(key, values, char):
                    yield 'new', info


def insert_into_database():
    for model, info in scrap(dictionary):
        for parameter in info:
            code = parameter[0]
            if len(parameter[1]) != 0:
                number = parameter[1]
            else:
                number = None
            name = parameter[2]
            price = parameter[3]
            model_id = db.get_model_id(conn, model)
            try:
                db.insert_product(conn, code, model_id, name, number, price)
            except mysql.connector.errors.IntegrityError:
                db.update_product(conn, code, price)
        conn.commit()


def main():
    insert_into_database()
    conn.close()


if __name__ == '__main__':
    car_class = Cars(settings.DATA_FILE)
    dictionary = car_class.reader()
    robot = BahmanRobot(settings.URL)
    conn = connect(option_files=settings.INFO_FiLE_PATH)
    main()
