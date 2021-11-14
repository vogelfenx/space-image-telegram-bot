from datetime import datetime
from os import path
from urllib.parse import unquote, urlsplit


def get_datetime_from_string(date):
    return datetime.strptime(date, '%Y-%m-%d %H:%M:%S')


def get_filename_from_url(url):
    path = urlsplit(url).path
    path = unquote(path)
    file_name = path.split(path)[1]
    return file_name
