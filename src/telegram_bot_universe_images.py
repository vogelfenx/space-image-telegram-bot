import telegram
from dotenv import dotenv_values
from download_pictures import fetch_nasa_pictures_of_the_day

secrets = dotenv_values('.secrets')

bot = telegram.Bot(token=secrets['TELEGRAM_BOT_TOKEN'])
chat_id = '@universe_images'


def send_message_to_chat(chat_id, text):
    bot.send_message(chat_id=chat_id, text=text)


def send_document_to_chat(chat_id, file_url):
    bot.send_document(chat_id=chat_id, document=file_url)


if __name__ == '__main__':
    #send_message_to_chat('@universe_images', 'Hello World form Python')
    image = fetch_nasa_pictures_of_the_day(images_count=1)
    for image_date, image_url in image.items():
        send_message_to_chat(chat_id, image_date)
        send_document_to_chat(chat_id, image_url)
