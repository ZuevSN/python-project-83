import psycopg2

def connect_db(app):
    return psycopg.connect(app.config('DATABASE_URL'))

def close(conn):
    conn.close()

def execute_sql(query):
    pass