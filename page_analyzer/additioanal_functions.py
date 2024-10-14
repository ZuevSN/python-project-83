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


def get_html_data(url_id):
    description = None
    url = db.get_url_by_id(url_id)
    print(url)
    response = requests.get(url['name'])
#    status_code = response.status_code
    response.raise_for_status()
    print(status_code)
    soup = BeautifulSoup(response.text, 'html.parser')
    h1 = soup.find('h1')
    h1 = h1.text if h1 else None
    print(h1)
    title = soup.find('title')
    title = title.text if title else None
    print(title)
    meta_description = soup.find('meta', attrs={'name': 'description'})
    if meta_description:
        description = meta_description.get('content')
        print(description)
    return (url_id, status_code, h1, title, description)
