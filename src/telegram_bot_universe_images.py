from time import sleep

import telegram
from dotenv import dotenv_values
from telegram import InputMediaDocument

from download_pictures import *

config = dotenv_values('.config')
secrets = dotenv_values('.secrets')

bot = telegram.Bot(token=secrets['TELEGRAM_BOT_TOKEN'])
chat_id = config['telegram_chat_id']

if __name__ == '__main__':
    while True:
        #images = fetch_nasa_epic_images()
        images = fetch_spacex_latest_launch_images()
        for image_name, image in images.items():
            caption = f'{image["image_date"]} - {image["image_caption"]}'

            if image['image_group']:
                media_group = []
                for image_url in image['image_urls']:
                    media = InputMediaDocument(media=image_url)
                    media_group.append(media)
                bot.send_message(chat_id, caption)
                bot.send_media_group(chat_id, media=media_group)
            else:
                bot.send_photo(chat_id, image['image_url'], caption)
        exit()
        # sleep(int(config['image_publishing_interval']))
