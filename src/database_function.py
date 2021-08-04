from exceptions import NameNotFound
import sys


def insert_site(conn, name, url):
    query = """
        INSERT INTO Site(name, address) VALUES (%s, %s);
    """
    cursor = conn.cursor()
    value = (name, url)
    cursor.execute(query, value)
    cursor.close()


def insert_company(conn, site_id, name):
    query = """
            INSERT INTO Company(site_id, name)
            VALUES(%s,%s);
    """
    cursor = conn.cursor()
    value = (site_id, name)
    cursor.execute(query, value)
    cursor.close()


def insert_model(conn, company_id, name):
    query = """
            INSERT INTO Model(company_id, name)
            VALUES(%s,%s);
    """
    cursor = conn.cursor()
    value = (company_id, name)
    cursor.execute(query, value)
    cursor.close()


def insert_product(conn, id, model_id, name, number, price):
    query = """
            INSERT INTO Product(id, model_id, name, number, price)
            VALUES(%s,%s,%s,%s,%s);
    """
    cursor = conn.cursor()
    value = (id, model_id, name, number, price)
    cursor.execute(query, value)
    cursor.close()


def update_site(conn, id, name, url):
    query = """
            UPDATE Site SET name = %s, address = %s
            WHERE id = %s;
    """
    cursor = conn.cursor()
    value = (name, url, id)
    cursor.execute(query, value)
    cursor.close()


def update_company(conn, id, name):
    query = """
            UPDATE Company SET name = %s
            WHERE id = %s;
    """
    cursor = conn.cursor()
    value = (name, id)
    cursor.execute(query, value)
    cursor.close()


def update_model(conn, id, name):
    query = """
            UPDATE Model SET name = %s
            WHERE id = %s;
    """
    cursor = conn.cursor()
    value = (name, id)
    cursor.execute(query, value)
    cursor.close()


def update_product(conn, id, price):
    query = """
            UPDATE Product SET price = %s
            WHERE id = %s;
    """
    cursor = conn.cursor()
    value = (price, id)
    cursor.execute(query, value)
    cursor.close()


def get_company_id(conn, name):
    query = "SELECT id FROM Company WHERE name = %s"
    cursor = conn.cursor()
    value = (name,)
    cursor.execute(query, value)
    com_id = cursor.fetchone()[0]
    cursor.close()
    return com_id


def get_model_id(conn, name):
    query = "SELECT id FROM Model WHERE name = %s"
    cursor = conn.cursor()
    value = (name,)
    cursor.execute(query, value)
    mod_id = cursor.fetchone()[0]
    cursor.close()
    return mod_id
