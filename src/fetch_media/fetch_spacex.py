from collections import defaultdict

import requests
from common import settings
from common.utilities import get_filename_from_url


def fetch_latest_launch_images():
    request_url = f'{settings.API_SPACEX_URL}/launches/'

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
