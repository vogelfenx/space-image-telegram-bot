import telegram
from dotenv import dotenv_values

secrets = dotenv_values('.secrets')

bot = telegram.Bot(token=secrets['TELEGRAM_BOT_TOKEN'])


def send_message_to_chat(chat_id, text):
    bot.send_message(chat_id=chat_id, text=text)


if __name__ == '__main__':
    send_message_to_chat('@universe_images', 'Hello World form Python')
