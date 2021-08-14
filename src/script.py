# internal
import settings
import database_function as db
from data_catcher import Cars
from robots import BahmanRobot
from logs import Logs

# standard
from os.path import join
import json

# mysql_connector_python
from mysql.connector import connect
import mysql


def scrap(data):
    """
    this method get dictionary and searching dictionary's values(model)
    and keys(company) to Bahman site and then, returns all data of
    Bahman as list.
    """
    log = Logs()
    # loads status(where the program was stop) for continue of there
    status_data = json_loads(join(settings.BASE_DIR, settings.status_file_name))
    # company, caught
    company_passed = status_data['company_passed']
    # model, caught
    model_passed = status_data['model_passed']
    checker = False

    # get keys and value from data.json
    for key, values in data.items():
        # check for caught or not
        if key in status_data['company_passed']:
            continue
        company_passed.append(key)
        # updating models
        if checker is True:
            model_passed = []
        checker = True

        # check for 'NEW' word because,
        # this word have a bug in the bahman site.
        if not key == 'NEW':
            for value in values:
                # check model caught or not
                if value in status_data['model_passed']:
                    continue
                status_data = json_loads(join(settings.BASE_DIR, settings.status_file_name))
                model_passed.append(value)
                check_round = 0

                # search all persian characters to bahman site
                for char in settings.persian_letters:
                    char_passed = settings.persian_letters[:settings.persian_letters.index(status_data['character'])]
                    if char in char_passed:
                        check_round += 1
                        continue
                    check_round += 1
                    # this is for debug
                    log.warning(f' model is: {value}')
                    log.warning(f'character is: {char}')

                    # catching data :))
                    for info in robot.next_page_fetch(key, value, char):
                        if info:
                            yield value, info
                        else:
                            continue

                    # save the status to status.json for if the program
                    # crashed, the program started where it had crashed
                    if check_round == len(settings.persian_letters):
                        status = {
                            'company_passed': company_passed[:-1],
                            'company': key,
                            'model_passed': model_passed[:-1],
                            'Model': value,
                            'character': 'ا'
                        }
                    else:
                        status = {
                            'company_passed': company_passed[:-1],
                            'company': key,
                            'model_passed': model_passed[:-1],
                            'Model': value,
                            'character': settings.persian_letters[(settings.persian_letters.index(char) + 1)]
                        }

                    json_dumps(join(settings.BASE_DIR, settings.status_file_name), status)
                    log.info('status saved')
                check_round = 0
        else:
            check_round = 0
            if 'new' in status_data['model_passed']:
                continue
            model_passed.append('new')

            for char in settings.persian_letters:
                # select all characters
                if char in settings.persian_letters[:settings.persian_letters.index(status_data['character'])]:
                    check_round += 1
                    continue
                check_round += 1

                for info in robot.next_page_fetch(key, values, char):
                    if info:
                        yield 'new', info
                    else:
                        continue
                
                print(f'the check round is: {check_round}')
                if check_round == len(settings.persian_letters):
                    status = {
                        'company_passed': company_passed[:-1],
                        'company': key,
                        'model_passed': model_passed[:-1],
                        'Model': 'new',
                        'character': 'ا'
                    }
                else:
                    status = {
                        'company_passed': company_passed[:-1],
                        'company': key,
                        'model_passed': model_passed[:-1],
                        'Model': 'new',
                        'character': settings.persian_letters[(settings.persian_letters.index(char) + 1)]
                    }

                json_dumps(join(settings.BASE_DIR, settings.status_file_name), status)
                log.info('status saved')
                check_round += 1
            check_round = 0


def insert_into_database():
    """
    this function get data of scrap function and
    save data to parts database.
    """

    log = Logs()

    # get model of car and part of that car
    for model, info in scrap(dictionary):
        log.info(f'information is: {info}')
        for parameter in info:
            code = parameter[0]
            # check for number column in Bahman site because
            # if number was empty what that do
            if len(parameter[1]) != 0:
                number = parameter[1]
            else:
                number = None
            name = parameter[2]
            price = int(parameter[3].replace(',', ''))
            model_id = db.get_model_id(conn, model)
            # insert data to parts.Product table if not part exist
            # else update price of that part
            try:
                db.insert_product(conn, code, model_id, name, number, price)
                log.info(f'\'{code}\' was not exist.I inserted')
            except mysql.connector.errors.IntegrityError:
                db.update_product(conn, code, price)

        # save parts
        conn.commit()
        log.info('successfully database updated!')


def json_dumps(path, dic):
    """
    :param path: get path of your json file(if not exist; it create that)
    :param dic: get data you want to save that
    and then saving that file to path
    """
    status = json.dumps(dic, indent=4, ensure_ascii=False)
    with open(path, 'w') as f:
        f.write(status)


def json_loads(path):
    """
    :param path: get path, you want to load that
    :return: the data of the json file in the path sa dict
    """
    with open(path, 'r') as f:
        status = f.read()
        return json.loads(status)


def main():
    """ setup project """
    insert_into_database()
    conn.close()


# running project and some needed variable
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
