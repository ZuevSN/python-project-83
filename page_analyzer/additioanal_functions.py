from validators import url as is_url
from urllib.parse import urlparse
import page_analyzer.db_manager as db
import requests
from bs4 import BeautifulSoup


MAX_LENGTH = 255

def validate(url):
    error = None
    if not url:
        error = 'URL обязателен'
    elif len(url) > MAX_LENGTH:
        error = f'URL превышает {MAX_LENGTH} символов'
    elif not is_url(url):
        error = 'Некорректный URL'
    return error


def normalize(url):
    url_data = urlparse(url)
    return f'{url_data.scheme}://{url_data.netloc}'


def get_html_data(response):
    data = []
    status_code = response.status_code
    data.append(status_code)
    soup = BeautifulSoup(response.text, 'html.parser', from_encoding='utf-8')
    h1 = soup.find('h1')
    h1 = h1.text if h1 else None
    data.append(h1)
    title = soup.find('title')
    title = title.text if title else None
    data.append(title)
    description = None
    meta_description = soup.find('meta', attrs={'name': 'description'})
    if meta_description:
        description = meta_description.get('content')
    data.append(description)
    return data
