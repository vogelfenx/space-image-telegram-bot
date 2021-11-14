from dotenv import dotenv_values

config = dotenv_values(".config")
secrets = dotenv_values(".secrets")

# .config settings
image_publishing_interval_seconds = int(config['image_publishing_interval_seconds'])
images_dir_path = config['images_dir_path']
telegram_chat_id = config['telegram_chat_id']

# API urls
API_SPACEX_URL = 'https://api.spacexdata.com/v3'
API_NASA_URL = 'https://api.nasa.gov/planetary'
API_NASA_EPIC_URL = 'https://api.nasa.gov/EPIC'

# .secrets settings
TELEGRAM_BOT_TOKEN = secrets['TELEGRAM_BOT_TOKEN']
NASA_API_KEY = secrets['NASA_API_KEY']
