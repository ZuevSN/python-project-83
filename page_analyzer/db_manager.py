import psycopg2

def connect(database_string):
    conn = psycopg2.connect(database_string)
    print('Соединение установлено')

def disconnect(conn):
    if conn:
        conn.close()
        print('Соединение разорвано')

def execute_query(conn, query):
    if conn:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        cursor.close()
        print(f'Выполнение запроса {query}')
    else:
        print('Соединение не установлено')