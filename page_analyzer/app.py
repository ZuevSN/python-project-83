#!/usr/bin/env python3
from flask import (
    Flask, render_template,
    request, get_flashed_messages,
    flash, redirect, url_for
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


@app.post('/urls')
def new_url():
    url = request.form.get('url')
    original_url = url
    url = normalize(url)
    error = validate(url)
    print(error)
    if error:
        flash(error, 'error')
        return render_template("index.html", post_=original_url), 422
    id = db.set_url(url)

    flash('Страница успешно добавлена', 'alert-success')
    return redirect(url_for('get_url_by_id', id=id))


@app.route('/urls')
def get_urls():
    urls = db.get_urls()
    print(urls)
    return render_template("urls.html", urls=urls)


@app.route('/urls/<id>')
def get_url_by_id(id):
    url = db.get_url_by_id(id)
    if url:
        return render_template("url.html", url=url)
    else:
        return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
