#!/usr/bin/env python3
from flask import Flask, render_template
from dotenv import load_dotenv
import os
#from page_analyzer.db_manager import db_manager as db
import psycopg2
from psycopg2.extras import DictCursor

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
#app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
DATABASE_URL = os.getenv('DATABASE_URL')


print(os.getcwd())

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/urls')
def urls():
    return render_template("urls.html")


@app.route('/urls/<id>')
def url(id):
    # Execute a SQL query to retrieve the URL with the given ID
    sql = "SELECT * FROM public.urls WHERE id = %s"
    conn = psycopg2.connect(DATABASE_URL)
    with conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(sql, (id,))
            url = curs.fetchone()
    conn.close()
    if url:
        return render_template("url.html", url=url)
    else:
        return "URL not found", 404

def execute_sql(sql):
    conn = psycopg2.connect(DATABASE_URL)
#    sql = "INSERT INTO users (username, phone) VALUES ('tommy', '123456789');"
    with conn:
        with conn.cursor() as curs:
            curs.execute(sql)
    conn.close()

if __name__ == "__main__":
    app.run(debug=True)
