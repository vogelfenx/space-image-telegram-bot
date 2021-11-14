import os
from datetime import datetime, timedelta
from pathlib import Path
from time import sleep

from telegram.error import BadRequest, RetryAfter

from common import settings
from common.utilities import remove_extension_from_filename
from fetch_media import download_file, fetch_nasa, fetch_spacex
from telegram_bot import publish_to_channel


def fetch_images():
    """Fetch images from API sources.
    """
    spacex_images = fetch_spacex.fetch_latest_launch_images()
    nasa_apod_images = fetch_nasa.fetch_pictures_of_the_day(images_count=1)
    nasa_epic_images = fetch_nasa.fetch_latest_epic_images()

    return {**spacex_images,
            **nasa_apod_images,
            **nasa_epic_images}


def filter_images(fetched_images, downloaded_images):
    """ Filter out the images that have already been downloaded.
    """
    try:
        downloaded_images = os.listdir(settings.images_dir_path)
        downloaded_images = [remove_extension_from_filename(image)
                             for image in downloaded_images]
    except FileNotFoundError:
        pass

    filtered_images = {image_name: image for (image_name, image) in fetched_images.items()
                       if image_name not in downloaded_images}
    return filtered_images


def download_images(images):
    """ Download fetched & filtered images.
    """
    Path(settings.images_dir_path).mkdir(parents=True, exist_ok=True)
    for image in images.values():
        download_file.download_image(image['image_url'])


def publish_images_to_channel(images):
    """ Publish retrieved images to telegram channel.
    """
    chat_id = settings.telegram_chat_id

    for image in images.values():
        caption = f'{image["image_date"]} - {image["image_caption"]}'
        image_url = image['image_url']
        try:
            publish_to_channel.publish_image(chat_id, image_url,
                                             caption=caption)
        except BadRequest:
            print('Couldn\'t send the image: ', image_url)
        except RetryAfter:
            continue
        sleep(4)  # avoid limitation - max 20 messages per minute per group


def main():
    downloaded_images = []
    while True:

        try:
            fetched_images = fetch_images()
        except Exception as exception:
            print('Something went wrong. Error:', exception)
            exit(1)

        filtered_images = filter_images(fetched_images, downloaded_images)

        download_images(filtered_images)

        publish_images_to_channel(filtered_images)

        print('next posting at', datetime.now() +
              timedelta(seconds=settings.image_publishing_interval_seconds))
        sleep(settings.image_publishing_interval_seconds)


if __name__ == '__main__':
    main()
