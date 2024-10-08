import psycopg2

class postgres_manager:
    def __init__(self, database_string):
        self.database_string = database_string
        self.conn = None

    def connect(self):
        self.conn = psycopg2.connect(self.database_string)
        print('Соединение установлено')

    def disconnect(self):
        if self.conn:
            self.conn.close()
            print('Соединение разорвано')

    def execute_query(self, query):
        if self.conn:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
            cursor.close()
            print(f'Выполнение запроса {query}')
        else:
            print('Соединение не установлено')