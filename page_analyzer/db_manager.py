import psycopg2
from psycopg2.extras import NamedTupleCursor


RETURN_ALL = True
RETURN_ONE = False
RETURN_NONE = None


def connect(database_url):
    conn = psycopg2.connect(database_url)
    return conn


def get_id(record):
    return record.id if record else None


def execute_query(database_url, commit, output_all, sql, values=None):
    with connect(database_url) as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(sql, values)
            if output_all is None:
                result = None
            elif output_all:
                result = curs.fetchall()
            else:
                result = curs.fetchone()
            if commit:
                conn.commit()
            return result if result else None


def get_urls(database_url):
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
    commit = False
    result = execute_query(database_url, commit, RETURN_ALL, sql)
    return result


def get_url_by_id(database_url, id):
    sql = """SELECT * FROM urls WHERE id = %s LIMIT 1"""
    commit = False
    result = execute_query(database_url, commit, RETURN_ONE, sql, (id,))
    return result


def get_url_id_by_name(database_url, name):
    sql = """SELECT id FROM urls WHERE name = %s LIMIT 1"""
    commit = False
    result = execute_query(database_url, commit, RETURN_ONE, sql, (name,))
    return get_id(result)


def set_url(database_url, url):
    sql = """INSERT INTO urls (name) values (%s) RETURNING id"""
    commit = True
    result = execute_query(database_url, commit, RETURN_ONE, sql, (url,))
    return get_id(result)


def get_checks_by_id(database_url, id):
    sql = """SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC"""
    commit = False
    result = execute_query(database_url, commit, RETURN_ALL, sql, (id,))
    return result


def set_check(database_url, data):
    sql = """INSERT INTO url_checks (url_id,status_code, h1, title, description)
    values (%s, %s, %s, %s, %s)"""
    commit = True
    execute_query(database_url, commit, RETURN_NONE, sql, data)
