from datetime import datetime, timedelta
from time import sleep

from common import settings
from fetch_media import fetch_nasa, fetch_spacex
from telegram_bot import publish_to_channel


def main():
    sended_images = []
    while True:
        # fetch images from apis
        try:
            spacex_images = fetch_spacex.fetch_latest_launch_images()
            nasa_apod_images = fetch_nasa.fetch_pictures_of_the_day(images_count=1)
            nasa_epic_images = fetch_nasa.fetch_latest_epic_images()
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

        # publish retrieved images to telegram channel
        chat_id = settings.telegram_chat_id

        for image_name, image in fetched_images.items():
            caption = f'{image["image_date"]} - {image["image_caption"]}'
            image_url = image['image_url']

            if type(image_url) is list:
                publish_to_channel.publish_images_group(chat_id, image_url,
                                                        caption=caption,
                                                        chunk_size=3)
            else:
                publish_to_channel.publish_image(chat_id, image_url,
                                                 caption=caption)
            sleep(4)  # avoid limitation - max 20 messages per minute per group

        print('next posting at', datetime.now() +
              timedelta(seconds=settings.image_publishing_interval_seconds))
        sleep(settings.image_publishing_interval_seconds)


if __name__ == '__main__':
    main()
