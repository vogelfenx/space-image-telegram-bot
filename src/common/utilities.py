from datetime import datetime
import os.path
from urllib.parse import unquote, urlsplit


def get_datetime_from_string(date):
    return datetime.strptime(date, '%Y-%m-%d %H:%M:%S')


def get_filename_from_url(url):
    path = urlsplit(url).path
    path = unquote(path)
    file_name = os.path.split(path)[1]
    return file_name


def remove_extension_from_filename(filename):
    return os.path.splitext(filename)[0]
