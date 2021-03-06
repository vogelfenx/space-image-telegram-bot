import os.path
from collections import defaultdict
from urllib.parse import urlsplit, urlunsplit

import requests
from common import settings
from common.utilities import (get_datetime_from_string, get_filename_from_url,
                              remove_extension_from_filename)


def fetch_pictures_of_the_day(images_count=20):
    requests_url = f'{settings.API_NASA_URL}/apod'

    request_parameters = {
        'api_key': settings.NASA_API_KEY,
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
            image_name = remove_extension_from_filename(image_name)
            images[image_name] = {
                'image_date': image['date'],
                'image_caption': image['title'],
                'image_url': image_url,
            }

    return images


def fetch_latest_epic_images():
    request_url_metadata = f'{settings.API_NASA_EPIC_URL}/api/natural/'
    request_url_images = f'{settings.API_NASA_EPIC_URL}/archive/natural'
    request_parameters = {
        'api_key': settings.NASA_API_KEY,
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
        image_url = image_url._replace(query=f'api_key={settings.NASA_API_KEY}')

        images[image_name] = {
            'image_date': image_metadata['date'],
            'image_caption': image_metadata['caption'],
            'image_url': urlunsplit(image_url),
        }

    return images
