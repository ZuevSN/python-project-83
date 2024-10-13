#!/usr/bin/env python3
from flask import (
    Flask, render_template,
    request,flash, redirect,
    url_for
)
from dotenv import load_dotenv
import os
import page_analyzer.db_manager as db
from page_analyzer.additioanal_functions import validate, normalize

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template("index.html")

#написать декоратор исключений
@app.post('/urls')
def new_url():
    try:
        url = request.form.get('url')
        original_url = url
        url = normalize(url)
        error = validate(url)
        print(error)
        if error:
            flash(error, 'error')
            return render_template("index.html", url=original_url), 422
        id = db.set_url(url)
        flash('Страница успешно добавлена', 'alert-success')
        return redirect(url_for('get_url_by_id', id=id))
    except Exception as e:
        return render_template("500.html", 500)


@app.route('/urls')
def get_urls():
    try:
        urls = {}
        urls = db.get_urls()
        return render_template("urls.html", urls=urls)
    except Exception as e:
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
    except Exception as e:
        return render_template("500.html"), 500


@app.post('/urls/<id>/checks')
def new_check(id):
    try:
        db.set_check(id)
        flash('Страница успешно проверена', 'alert-success')
        return redirect(url_for('get_url_by_id', id=id))
    except Exception as e:
            return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(debug=True)
