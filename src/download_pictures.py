from collections import defaultdict
from os.path import split
from pathlib import Path
from urllib.parse import unquote, urlsplit, urlunsplit
import requests
from dotenv import dotenv_values
from datetime import datetime

config = dotenv_values(".config")
secrets = dotenv_values(".secrets")


def get_datetime_from_string(date):
    return datetime.strptime(date, '%Y-%m-%d %H:%M:%S')


def get_filename_from_url(url):
    path = urlsplit(url).path
    path = unquote(path)
    file_name = split(path)[1]
    return file_name


def fetch_nasa_epic_images():
    request_url_metadata = f'{config["API_NASA_EPIC_URL"]}/api/natural/'
    request_url_images = f'{config["API_NASA_EPIC_URL"]}/archive/natural'
    request_parameters = {
        'api_key': secrets["NASA_API_KEY"],
    }

    response = requests.get(request_url_metadata, params=request_parameters)
    response.raise_for_status()
    recent_images_metadata = response.json()

    images = defaultdict(list)
    for image_metadata in recent_images_metadata:
        image_name = image_metadata['image']

        image_date = get_datetime_from_string(image_metadata['date'])
        image_date = (f'{image_date.year}/'
                      f'{image_date.strftime("%m")}/'
                      f'{image_date.strftime("%d")}'
                      )

        image_url = urlsplit(f'{request_url_images}/{image_date}/png/{image_name}.png')
        image_url = image_url._replace(query=f'api_key={secrets["NASA_API_KEY"]}')

        images[image_name] = {
            'image_date': image_metadata['date'],
            'image_caption': image_metadata['caption'],
            'image_url': urlunsplit(image_url),
        }

    return images


def fetch_nasa_pictures_of_the_day(images_count=20):
    requests_url = f'{config["API_NASA_URL"]}/apod'

    request_parameters = {
        'api_key': secrets["NASA_API_KEY"],
        'count': images_count,
    }
    response = requests.get(requests_url, params=request_parameters)
    response.raise_for_status()

    response_images = response.json()

    images = defaultdict(list)
    for image in response_images:
        image_type = image['media_type']

        if image_type == 'image':
            image_url = image['url']
            image_name = get_filename_from_url(image_url)
            images[image_name] = {
                'image_date': image['date'],
                'image_caption': image['title'],
                'image_url': image_url,
            }

    return images


def fetch_spacex_latest_launch_images():
    request_url = f'{config["API_SPACEX_URL"]}/launches/'

    response = requests.get(request_url)
    response.raise_for_status()

    launches = response.json()
    images = defaultdict(list)
    image_urls = []

    is_latest_launch_images = False
    for launch in reversed(launches):
        image_name = ''
        for image in launch['links']['flickr_images']:
            image_name = get_filename_from_url(image)
            image_urls.append(image)
            is_latest_launch_images = True
        if image_name:
            images[image_name] = {
                'image_date': launch['launch_date_utc'],
                'image_caption': f'{launch["mission_name"]} - {launch["details"]}',
                'image_urls': image_urls,
                'image_group': True,
            }

        if is_latest_launch_images:
            break

    return images


def download_image(image_url,
                   image_path_to_save='data/images',
                   image_prefix='',
                   parameters={}):

    response = requests.get(image_url, params=parameters)
    response.raise_for_status()

    Path(image_path_to_save).mkdir(parents=True, exist_ok=True)

    image_name = f'{image_prefix}_{get_filename_from_url(image_url)}'

    with open(f'{image_path_to_save}/{image_name}', 'wb') as file:
        file.write(response.content)


def publish_images_to_telegram_chat():
    pass


if __name__ == '__main__':

    try:
        latest_launch_images = fetch_spacex_latest_launch_images()
        for launch_number, launch_images in latest_launch_images.items():
            for launch_image in launch_images:
                download_image(launch_image,
                               image_prefix=launch_number,
                               image_path_to_save=config['spacex_images_dir_path'])

        nasa_images = fetch_nasa_pictures_of_the_day()
        for image_date, image in nasa_images.items():
            download_image(image,
                           image_prefix=image_date,
                           image_path_to_save=config['nasa_images_dir_path'])

        nasa_epic_images = fetch_nasa_epic_images()
        for image_date, images in nasa_epic_images.items():
            for image in images:
                download_image(image,
                               image_prefix=image_date,
                               image_path_to_save=f'{config["nasa_images_dir_path"]}/epic',
                               parameters={'api_key': secrets["NASA_API_KEY"], })
    except Exception as exception:
        print('Что-то пошло не так, ошибка:', exception)
