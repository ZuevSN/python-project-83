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


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template("index.html")


# написать декоратор исключений
@app.post('/urls')
def new_url():
    try:
        url = request.form.get('url')
        original_url = url
        url = normalize(url)
        error = validate(url)
        print(error)
        if error:
            flash(error, 'danger')
            return render_template("index.html", url=original_url), 422
        print(url)
        id = db.get_url_by_name(url)
        if id:
            flash('Страница уже существует', 'info')
        else:
            print(url)
            id = db.set_url(url)
            print(db.set_url(url))
            flash('Страница успешно добавлена', 'success')
        print(id)
        return redirect(url_for('get_url_by_id', id=id))
    except Exception:
        return render_template("500.html", 500)


@app.route('/urls')
def get_urls():
    try:
        urls = {}
        urls = db.get_urls()
        return render_template("urls.html", urls=urls)
    except Exception:
        return render_template("500.html", 500)


@app.route('/urls/<id>')
def get_url_by_id(id):
    try:
        url = checks = {}
        url = db.get_url_by_id(id)
        checks = db.get_checks_by_id(id)
        if not url:
            return render_template("404.html"), 404
        return render_template("url.html", url=url, checks=checks)
    except Exception:
        return render_template("500.html"), 500


@app.post('/urls/<id>/checks')
def new_check(id):
    try:
        try:
            data = get_html_data(id)
        except Exception:
            flash('Произошла ошибка при проверке', 'danger')
            return redirect(url_for('get_url_by_id', id=id))
        db.set_check(data)
        flash('Страница успешно проверена', 'success')
        return redirect(url_for('get_url_by_id', id=id))
    except Exception:
        return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)
