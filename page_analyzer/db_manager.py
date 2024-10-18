import psycopg2
from psycopg2.extras import NamedTupleCursor
from flask import current_app, g


RETURN_ALL = True
RETURN_ONE = False
RETURN_NONE = None


def connect():
    if 'conn' not in g:
        g.conn = psycopg2.connect(current_app.config['DATABASE_URL'])
    return g.conn


def close_conn(conn):
    if conn:
        conn.close()


def execute_query(output_all, sql, values=None):
    with g.conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(sql, values)
        if output_all is None:
            return None
        elif output_all:
            return curs.fetchall()
        else:
            return curs.fetchone()


def get_urls():
    sql = """   SELECT urls.id, urls.name,
                    uc.created_at, uc.status_code
                FROM urls
                LEFT JOIN (
                    SELECT id, url_id, status_code, h1,
                        title, description, created_at,
                        max(id) over (partition by url_id) max_id
                    FROM url_checks
                    ) uc ON urls.id = uc.url_id AND uc.max_id = uc.id
                    ORDER BY id DESC"""
    result = execute_query(RETURN_ALL, sql)
    return result


def get_url_by_id(id):
    sql = """SELECT * FROM urls WHERE id = %s LIMIT 1"""
    result = execute_query(RETURN_ONE, sql, (id,))
    return result


def get_url_id_by_name(name):
    sql = """SELECT id FROM urls WHERE name = %s LIMIT 1"""
    result = execute_query(RETURN_ONE, sql, (name,))
    return result


def set_url(url):
    sql = """INSERT INTO urls (name) values (%s) RETURNING id"""
    result = execute_query(RETURN_ONE, sql, (url,))
    g.conn.commit()
    return result


def get_checks_by_id(id):
    sql = """SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC"""
    result = execute_query(RETURN_ALL, sql, (id,))
    return result


def set_check(data):
    sql = """INSERT INTO url_checks (url_id,status_code, h1, title, description)
    values (%s, %s, %s, %s, %s) RETURNING id"""
    result = execute_query(RETURN_ONE, sql, data)
    g.conn.commit()
    return result
