import psycopg2
from psycopg2.extras import DictCursor
from flask import current_app, g


def connect():
    if 'conn' not in g:
        g.conn = psycopg2.connect(current_app.config['DATABASE_URL'])
    return g.conn


def close_conn(conn):
    if conn:
        conn.close()


def read_base(sql, values=None):
    with g.conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute(sql, values)
        result = [dict(row) for row in curs.fetchall()]
    return result


def edit_base(sql, values=None):
    with g.conn.cursor() as curs:
        curs.execute(sql, values)
        g.conn.commit()
        return curs.fetchone()[0]


def get_one_row(data):
    result = data[0] if data else data
    print(f'getonerow{result}')
    return result


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
    result = read_base(sql)
    return result


def get_first_row(data):
    result = data[0] if data else {}
    return result


def get_url_by_id(id):
    sql = """SELECT * FROM urls WHERE id = %s LIMIT 1"""
    result = read_base(sql, (id,))
    return get_first_row(result)


def get_url_id_by_name(name):
    sql = """SELECT id FROM urls WHERE name = %s LIMIT 1"""
    result = read_base(sql, (name,))
    return get_first_row(result).get('id')


def set_url(url):
    sql = """INSERT INTO urls (name) values (%s) RETURNING id"""
    result = edit_base(sql, (url,))
    return result


def get_checks_by_id(id):
    sql = """SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC"""
    result = read_base(sql, (id,))
    return result


def set_check(data):
    sql = """INSERT INTO url_checks (url_id,status_code, h1, title, description)
    values (%s, %s, %s, %s, %s) RETURNING id"""
    result = edit_base(sql, data)
    return result
