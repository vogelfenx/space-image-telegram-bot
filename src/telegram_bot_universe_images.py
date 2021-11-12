import telegram
from dotenv import dotenv_values
from download_pictures import fetch_nasa_pictures_of_the_day
from time import sleep

config = dotenv_values('.config')
secrets = dotenv_values('.secrets')

bot = telegram.Bot(token=secrets['TELEGRAM_BOT_TOKEN'])
chat_id = '@universe_images'

if __name__ == '__main__':
    image = fetch_nasa_pictures_of_the_day(images_count=5)
    while True:
        for image_date, image_url in image.items():
            bot.send_photo(chat_id, image_url, f'Photo taken on {image_date}')
        sleep(int(config['image_publishing_interval']))
