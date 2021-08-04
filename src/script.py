# internal
import settings
import database_function as db
from data_catcher import Cars
from robots import BahmanRobot
from os.path import join
import json

# mysql_connector_python
from mysql.connector import connect
import mysql


def scrap(data):
    status_data = json_loads(join(settings.BASE_DIR, settings.status_file_name))
    company_passed = status_data['company_passed']
    model_passed = status_data['model_passed']
    checker = False

    for key, values in data.items():
        if key in status_data['company_passed']:
            continue
        company_passed.append(key)

        if checker is True:
            model_passed = []
        checker = True

        if not key == 'NEW':
            for value in values:
                if value in status_data['model_passed']:
                    continue
                model_passed.append(value)

                for char in settings.persian_letters:
                    testy = settings.persian_letters[:settings.persian_letters.index(status_data['character'])]
                    if char in testy:
                        continue
                    print(f'\n[=============--<<< {value} >>>--=============]')
                    print(f'[---------------<<< {char} >>>---------------]\n')

                    for info in robot.next_page_fetch(key, value, char):
                        if info:
                            yield value, info
                        else:
                            continue

                    status = {
                        'company_passed': company_passed[:-1],
                        'company': key,
                        'model_passed': model_passed[:-1],
                        'Model': value,
                        'character': char
                    }
                    json_dumps(join(settings.BASE_DIR, settings.status_file_name), status)
        else:
            if 'new' in status_data['model_passed']:
                continue
            model_passed.append('new')

            for char in settings.persian_letters:
                # select all characters
                if char in settings.persian_letters[:settings.persian_letters.index(status_data['character'])]:
                    continue
 
                for info in robot.next_page_fetch(key, values, char):
                    if info:
                        yield 'new', info
                    else:
                        continue

                status = {
                    'company_passed': company_passed[:-1],
                    'company': key,
                    'model_passed': model_passed[:-1],
                    'Model': 'new',
                    'character': char
                }
                json_dumps(join(settings.BASE_DIR, settings.status_file_name), status)


def insert_into_database():
    for model, info in scrap(dictionary):
        print(info)
        for parameter in info:
            code = parameter[0]
            if len(parameter[1]) != 0:
                number = parameter[1]
            else:
                number = None
            name = parameter[2]
            price = int(parameter[3].replace(',', ''))
            model_id = db.get_model_id(conn, model)
            try:
                db.insert_product(conn, code, model_id, name, number, price)
            except mysql.connector.errors.IntegrityError:
                db.update_product(conn, code, price)
        conn.commit()


def json_dumps(path, dic):
    status = json.dumps(dic, indent=4, ensure_ascii=False)
    with open(path, 'w') as f:
        f.write(status)


def json_loads(path):
    with open(path, 'r') as f:
        status = f.read()
        return json.loads(status)


def main():
    insert_into_database()
    conn.close()


if __name__ == '__main__':
    car_class = Cars(settings.DATA_FILE)
    dictionary = car_class.reader()
    robot = BahmanRobot(settings.URL)
    conn = connect(option_files=settings.INFO_FiLE_PATH)
    main()
    status = {
        'company_passed': [],
        'company': 'Dignity',
        'model_passed': [],
        'Model': 'Dignity',
        'character': 'ا'
    }

    json_dumps(join(settings.BASE_DIR, settings.status_file_name), status)
