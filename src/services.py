import shutil
from collections import defaultdict
from datetime import datetime
from os import listdir
from os.path import split
from pathlib import Path
from time import sleep
from urllib.parse import unquote, urlsplit, urlunsplit

import requests
import telegram
from dotenv import dotenv_values
from telegram import InputMediaPhoto

config = dotenv_values(".config")
secrets = dotenv_values(".secrets")

images_dir_path = config['images_dir_path']

bot = telegram.Bot(token=secrets['TELEGRAM_BOT_TOKEN'])


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def get_datetime_from_string(date):
    return datetime.strptime(date, '%Y-%m-%d %H:%M:%S')


def get_filename_from_url(url):
    path = urlsplit(url).path
    path = unquote(path)
    file_name = split(path)[1]
    return file_name


def fetch_latest_nasa_epic_images():
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
                'image_url': image_urls,
            }

        if is_latest_launch_images:
            break

    return images


def download_image(image_url,
                   image_path_to_save=images_dir_path,
                   image_name='',
                   parameters={}):

    response = requests.get(image_url, params=parameters)
    response.raise_for_status()

    if not image_name:
        image_name = f'{get_filename_from_url(image_url)}'

    with open(f'{image_path_to_save}/{image_name}', 'wb') as file:
        file.write(response.content)


def publish_images_group_to_chat(chat_id, images,
                                 caption='', chunk_size=9):
    """Publish group of images to telegram chat.
    Before sending the images, the function divide list of images into chunks,
    when max size of 9 exceeded, to avoid telegram api limitation
    of send_media_group() - max chunk size 9 & min 2 pieces.
    """

    chunks = [images[i:i + chunk_size] for i in range(0, len(images), chunk_size)]

    if caption:
        bot.send_message(chat_id=chat_id, text=caption)

    for chunk in chunks:
        if len(chunk) > 1:
            chunk = [InputMediaPhoto(media=file) for file in chunk]
            bot.send_media_group(chat_id, media=chunk)
            sleep(60*chunk_size/20)  # max messages per minute per group = 20
        else:
            bot.send_photo(chat_id, chunk[0])


def publish_image_to_chat(chat_id, image, caption=''):
    image = image
    bot.send_photo(chat_id, image, caption)


if __name__ == '__main__':
    chat_id = config['telegram_chat_id']

    sended_images = []
    while True:
        # fetch images from apis
        try:
            spacex_images = fetch_spacex_latest_launch_images()
            nasa_apod_images = fetch_nasa_pictures_of_the_day(images_count=2)
            nasa_epic_images = fetch_latest_nasa_epic_images()
        except Exception as exception:
            print('Something went wrong. Error:', exception)
            exit(1)

        fetched_images = {**spacex_images,
                          **nasa_apod_images,
                          **nasa_epic_images}

        # filter images that were already posted
        fetched_images = {image_name: image for (image_name, image) in fetched_images.items()
                          if image_name not in sended_images}
        sended_images += [image for image in fetched_images.keys()]

        # download fetched images into specified directory
        shutil.rmtree(images_dir_path, ignore_errors=True)
        Path(images_dir_path).mkdir(parents=True, exist_ok=True)

        for image_name, image in fetched_images.items():
            image_url = image['image_url']
            if type(image_url) is list:
                for image in image_url:
                    download_image(image)
            else:
                download_image(image_url)

        # publish retrieved images to telegram channel
        images = listdir(images_dir_path)
        images = [f'{images_dir_path}/{image}' for image in images]
        images = [open(image, 'rb') for image in images]

        try:
            publish_images_group_to_chat(chat_id, images, chunk_size=2)
        except Exception as exception:
            print('Something went wrong. Error: ', exception)
            exit(1)

        sleep(int(config['image_publishing_interval_seconds']))
