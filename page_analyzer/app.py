#!/usr/bin/env python3
from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == "__main__":
    app.run(debug=True)
