#!/usr/bin/env python3
from flask import Flask, render_template, request, flash
from dotenv import load_dotenv
import os
#from page_analyzer.db_manager import db_manager as db
import page_analyzer.db_manager as db
import psycopg2
from psycopg2.extras import DictCursor
from page_analyzer.additioanal_functions import validate

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
#app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
DATABASE_URL = os.getenv('DATABASE_URL')


print(os.getcwd())

@app.route('/')
def index():
    return render_template("index.html")


@app.post('/urls')
def post_url():
    url = request.form.get('url')
    error = validate(url)
    if error:
        flash(error, 'error')
        return render_template("index.html"), 422


@app.route('/urls')
def get_urls():
    result = db.get_urls()
    print(result)
    return render_template("urls.html", urls=result)


@app.route('/urls/<id>')
def get_url_by_id(id):
    result = db.get_url_by_id(id)
    if result:
        return render_template("url.html", url=result)
    else:
        return "URL not found", 404


if __name__ == "__main__":
    app.run(debug=True)
