from validators import url as is_url
from page_analyzer.db_manager import is_get_url_by_name


def validate(value):
    error = None
    if not value:
        error = 'URL не введен'
    elif is_url(value):
        error = 'URL не корректный'
    elif is_get_url_by_name(value):
        error = 'URL уже есть в базе'
    return error
