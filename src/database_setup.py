import database_function as db
import settings
from mysql.connector import connect
from data_catcher import Cars


conn = connect(option_files=settings.INFO_FiLE_PATH)
car = Cars(settings.DATA_FILE)
data = car.reader()


def site(conn):
    db.insert_site(conn, settings.SITE, settings.URL)
    conn.commit()


def company(conn):
    for com in data:
        db.insert_company(conn, settings.BAHMAN_ID, com)
    conn.commit()


def model(conn):
    for key, values in data.items():
        for value in values:
            company_id = db.get_company_id(conn, key)
            db.insert_model(conn, company_id, value)
    conn.commit()


def main():
    site(conn)
    company(conn)
    model(conn)
    conn.close()


if __name__ == '__main__':
    main()
