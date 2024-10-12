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
def read_query(conn, query, values=None):
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute(query, values)
#        result = curs.fetchall()
        result = [dict(row) for row in curs.fetchall()]
    return result

@connection
def write_query(conn, query, values=None):
    with conn.cursor() as curs:
        curs.execute(query, values)

def is_get_url_by_name(url):
    query = """SELECT null FROM urls WHERE name = %s"""
    result = read_query(query, (url,))
    return bool(result)

def get_urls():
    query = """SELECT * FROM urls"""
    result = read_query(query)
    return result

def get_url_by_id(id):
    query = """SELECT * FROM urls WHERE id = %s"""
    result = read_query(query, (id,))
    return result[0]

def get_url_by_name(name):
    query = """SELECT * FROM urls WHERE name = %s"""
    result = read_query(query, (name,))
    return result[0]