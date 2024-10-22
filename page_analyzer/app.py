#!/usr/bin/env python3
from flask import (
    Flask, render_template,
    request, flash, redirect,
    url_for
)
from dotenv import load_dotenv
import os
import page_analyzer.db_manager as db
from page_analyzer.url_functions import (
    validate, normalize, get_html_data
)
from functools import wraps
import requests


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
app.config['DEBUG'] = os.getenv('DEBUG')

DATABASE_URL = app.config['DATABASE_URL']


def render_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            match e.args[0]:
                case 404:
                    return render_template("404.html")
            return render_template("500.html")
    return wrapper


@app.get('/')
@render_exceptions
def index():
    return render_template("index.html")


@app.post('/urls')
@render_exceptions
def set_url():
    url = request.form.get('url')
    original_url = url
    url = normalize(url)
    error = validate(url)
    if error:
        flash(error, 'danger')
        return render_template("index.html", url=original_url), 422
    conn = db.connect(DATABASE_URL)
    id = db.get_url_id_by_name(conn, url)
    if id:
        flash('Страница уже существует', 'info')
    else:
        conn = db.connect(DATABASE_URL)
        id = db.set_url(conn, url)
        flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_url_by_id', id=id))


@app.get('/urls')
@render_exceptions
def get_urls():
    conn = db.connect(DATABASE_URL)
    urls = db.get_urls(conn)
    return render_template("urls.html", urls=urls)


@app.get('/urls/<id>')
@render_exceptions
def get_url_by_id(id):
    conn = db.connect(DATABASE_URL)
    url = db.get_url_by_id(conn, id)
    conn = db.connect(DATABASE_URL)
    checks = db.get_checks_by_id(conn, id)
    if not url:
        raise Exception(404)
    return render_template("url.html", url=url, checks=checks)


@app.post('/urls/<id>/checks')
@render_exceptions
def set_check(id):
    conn = db.connect(DATABASE_URL)
    url = db.get_url_by_id(conn, id)
    url_name = url.name
    try:
        response = requests.get(url_name)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('get_url_by_id', id=id))
    data = [id] + get_html_data(response)
    conn = db.connect(DATABASE_URL)
    db.set_check(conn, data)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_url_by_id', id=id))


if __name__ == "__main__":
    app.run()
