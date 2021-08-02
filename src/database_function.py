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
            INSERT INTO site(id, model_id, name, number, price)
            VALUES(%s,%s,%s,%s,%s);
    """
    cursor = conn.cursor()
    value = (id, model_id, name, number, price)
    cursor.execute(query, value)
    cursor.close()


def update_site(conn, id, name, url):
    query = """
            UPDATE Site SET name = %s, address = %s
            WHERE id = '%s';
    """
    cursor = conn.cursor()
    value = (name, url, id)
    cursor.execute(query, value)
    cursor.close()


def update_company(conn, id, name):
    query = """
            UPDATE Company SET name = %s
            WHERE id = '%s';
    """
    cursor = conn.cursor()
    value = (name, id)
    cursor.execute(query, value)
    cursor.close()


def update_model(conn, id, name):
    query = """
            UPDATE site SET name = %s
            WHERE id = '%s';
    """
    cursor = conn.cursor()
    value = (name, id)
    cursor.execute(query, value)
    cursor.close()


def update_product(conn, id, price):
    query = """
            UPDATE site SET price = %s
            WHERE id = '%s';
    """
    cursor = conn.cursor()
    value = (price, id)
    cursor.execute(query, value)
    cursor.close()
