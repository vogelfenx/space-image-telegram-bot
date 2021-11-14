import os.path
from collections import defaultdict

import requests
from common import settings
from common.utilities import (get_filename_from_url,
                              remove_extension_from_filename)


def fetch_latest_launch_images():
    request_url = f'{settings.API_SPACEX_URL}/launches/'

    response = requests.get(request_url)
    response.raise_for_status()

    launches = response.json()
    images = defaultdict(list)

    is_latest_launch_with_images = False
    for launch in reversed(launches):
        image_name = ''
        for image in launch['links']['flickr_images']:
            image_name = get_filename_from_url(image)
            image_name = remove_extension_from_filename(image_name)
            images[image_name] = {
                'image_date': launch['launch_date_utc'],
                'image_caption': f'Mission: {launch["mission_name"]}',
                'image_url': image,
            }
            is_latest_launch_with_images = True
        if is_latest_launch_with_images:
            break

    return images
