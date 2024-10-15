#!/usr/bin/env python3
from flask import (
    Flask, render_template,
    request, flash, redirect,
    url_for
)
from dotenv import load_dotenv
import os
import page_analyzer.db_manager as db
from page_analyzer.additioanal_functions import (
    validate, normalize, get_html_data
)
from functools import wraps
import requests


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


def render_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            print(f'Выполняется {func.__name__}')
            return func(*args, **kwargs)
        except Exception as e:
            match e.args[0]:
                case 404:
                    return render_template("404.html")
            return render_template("500.html")
    return wrapper


@app.route('/')
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
    id = db.get_url_id_by_name(url)
    if id:
        flash('Страница уже существует', 'info')
    else:
        id = db.set_url(url)
        flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_url_by_id', id=id))


@app.route('/urls')
@render_exceptions
def get_urls():
    urls = {}
    urls = db.get_urls()
    return render_template("urls.html", urls=urls)


@app.route('/urls/<id>')
@render_exceptions
def get_url_by_id(id):
    url = checks = {}
    url = db.get_url_by_id(id)
    checks = db.get_checks_by_id(id)
    if not url:
        raise Exception(404)
    return render_template("url.html", url=url, checks=checks)


@app.post('/urls/<id>/checks')
@render_exceptions
def set_check(id):
    url_name = db.get_url_by_id(id)['name']
    try:
        response = requests.get(url_name)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('get_url_by_id', id=id))
    data = [id] + get_html_data(response)
    db.set_check(data)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_url_by_id', id=id))


if __name__ == "__main__":
    app.run(debug=True)
