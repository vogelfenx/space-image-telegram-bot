from datetime import datetime, timedelta
from time import sleep

from dotenv import dotenv_values

import services

config = dotenv_values('.config')
secrets = dotenv_values('.secrets')

chat_id = config['telegram_chat_id']


def main():
    sended_images = []
    while True:
        # fetch images from apis
        try:
            spacex_images = services.fetch_spacex_latest_launch_images()
            nasa_apod_images = services.fetch_nasa_pictures_of_the_day(images_count=1)
            nasa_epic_images = {}  # services.fetch_latest_nasa_epic_images()
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
        for image_name, image in fetched_images.items():
            caption = f'{image["image_date"]} - {image["image_caption"]}'
            image_url = image['image_url']

            if type(image_url) is list:
                services.publish_images_group_to_chat(chat_id, image_url, caption=caption,
                                                      chunk_size=3)
            else:
                services.publish_image_to_chat(chat_id, image_url, caption=caption)
            sleep(4)  # avoid limitation - max 20 messages per minute per group

        publishing_interval = int(config['image_publishing_interval_seconds'])
        print('next posting at', datetime.now() + timedelta(seconds=publishing_interval))
        sleep(publishing_interval)


if __name__ == '__main__':
    main()
