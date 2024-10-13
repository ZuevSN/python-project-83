import psycopg2
from psycopg2.extras import DictCursor
import os
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = psycopg2.connect(DATABASE_URL)
        print('Соединение установлено')
        try:
            print(f'Выполняется {func.__name__}')
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
            print('Соединение разорвано')
        return result
    return wrapper


@connection
def read_base(conn, sql, values=None):
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute(sql, values)
        result = [dict(row) for row in curs.fetchall()]
    return result

@connection
def edit_base(conn, sql, values=None):
    with conn.cursor() as curs:
        curs.execute(sql, values)
        conn.commit()
        return curs.fetchone()[0]

#сделать фабрику функций
def is_get_url_by_name(url):
    sql = """SELECT null FROM urls WHERE name = %s"""
    result = read_base(sql, (url,))
    return bool(result)

def get_urls():
    sql = """SELECT * FROM urls ORDER BY id DESC"""
    result = read_base(sql)
    return result

def get_url_by_id(id):
    sql = """SELECT * FROM urls WHERE id = %s"""
    result = read_base(sql, (id,))
    return result[0]

def get_url_by_name(name):
    sql = """SELECT * FROM urls WHERE name = %s"""
    result = read_base(sql, (name,))
    return result[0]

def set_url(url):
    sql = """INSERT INTO urls (name) values (%s) RETURNING id"""
    result = edit_base(sql,(url,))
    return result

def get_checks_by_id(id):
    sql = """SELECT * FROM url_checks WHERE url_id = %s"""
    result = read_base(sql, (id,))
    return result

def set_check(url_id):
    sql = """INSERT INTO url_checks (url_id) values (%s) RETURNING id"""
    result = edit_base(sql,(url_id,))
    return result