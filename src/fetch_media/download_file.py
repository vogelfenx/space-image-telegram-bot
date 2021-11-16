from pathlib import Path

import requests
from common import settings
from common.utilities import get_filename_from_url


def download_image(image_url,
                   image_path_to_save=settings.images_dir_path,
                   image_name='',
                   parameters={}):

    response = requests.get(image_url, params=parameters)
    response.raise_for_status()

    if not image_name:
        image_name = f'{get_filename_from_url(image_url)}'

    image_path = Path(image_path_to_save) / image_name
    with open(image_path, 'wb') as file:
        file.write(response.content)
