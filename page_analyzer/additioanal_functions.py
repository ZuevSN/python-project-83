from validators import url as is_url
from urllib.parse import urlparse
import page_analyzer.db_manager as db
import requests
from bs4 import BeautifulSoup


def validate(url):
    error = None
    if not url:
        error = 'URL не введен'
    elif not is_url(url) or len(url) > 255:
        error = 'Некорректный URL'
    elif db.is_get_url_by_name(url):
        error = 'Страница уже существует'
    return error


def normalize(url):
    url_data = urlparse(url)
    return f'{url_data.scheme}://{url_data.netloc}'


def get_html_data(url_id):
    description = None
    url = db.get_url_by_id(url_id)
    response = requests.get(url['name'])
    status_code = response.status_code
    soup = BeautifulSoup(response.text, 'html.parser')
    h1 = soup.find('h1')
    h1 = h1.text if h1 else None
    title = soup.find('title')
    title = title.text if title else None
    meta_description = soup.find('meta', attrs={'name': 'description'})
    if meta_description:
        description = meta_description.get('content')
    return (url_id, status_code, h1, title, description)
