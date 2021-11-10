import requests
from pathlib import Path
from dotenv import dotenv_values

config = dotenv_values(".config")


def download_picture(url, image_path_to_save=config["images_dir_path"]):
    response = requests.get(picture_url)
    response.raise_for_status()

    Path(config['images_dir_path']).mkdir(parents=True, exist_ok=True)

    with open(f'{image_path_to_save}./shuttle.jpeg', 'wb') as file:
        file.write(response.content)


if __name__ == '__main__':
    picture_url = 'https://www.costakreuzfahrten.at/content/dam/costa/costa-magazine/articles-magazine/travel/bali-travel/bali_m.jpg.image.694.390.low.jpg'

    download_picture(picture_url)
