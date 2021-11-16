from time import sleep

from common import settings
from telegram import Bot, InputMediaPhoto

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)


def publish_images_group(chat_id, images,
                         caption='', chunk_size=9):
    """Publish group of images to telegram chat.
    Before sending the images, the function divide list of images into chunks,
    when max size of 9 exceeded, to avoid telegram api limitation
    of send_media_group() - max chunk size 9 & min 2 pieces.
    """

    chunks = [images[i:i + chunk_size] for i in range(0, len(images), chunk_size)]

    if caption:
        bot.send_message(chat_id=chat_id, text=caption)

    for chunk in chunks:
        if len(chunk) > 1:
            chunk = [InputMediaPhoto(media=file) for file in chunk]
            bot.send_media_group(chat_id, media=chunk)
            sleep(60*chunk_size/20)  # max messages per minute per group = 20
        else:
            bot.send_photo(chat_id, chunk[0])


def publish_image(chat_id, image, caption=''):
    bot.send_photo(chat_id, image, caption)
