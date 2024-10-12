from validators import url as is_url
from urllib.parse import urlparse
from page_analyzer.db_manager import is_get_url_by_name


def validate(url):
    error = None
    if not url:
        error = 'URL не введен'
    elif not is_url(url) or len(url)>255:
        error = 'Некорректный URL'
    elif is_get_url_by_name(url):
        error = 'Страница уже существует'
    return error

def normalize(url):
    url_data = urlparse(url)
    return f'{url_data.scheme}://{url_data.netloc}'
