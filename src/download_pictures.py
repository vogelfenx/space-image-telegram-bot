import requests
from pathlib import Path
from dotenv import dotenv_values
from collections import defaultdict

config = dotenv_values(".config")


def fetch_spacex_latest_launch_images():
    api_url = f'{config["API_ROOT_URL"]}/launches/'

    response = requests.get(api_url)
    response.raise_for_status()

    launches = response.json()
    latest_launch_images = defaultdict(list)

    is_latest_launch_images = False
    for launch in reversed(launches):
        for image in launch['links']['flickr_images']:
            latest_launch_images[launch['flight_number']].append(image)
            is_latest_launch_images = True
        if is_latest_launch_images:
            break

    return latest_launch_images


def download_launch_image(url, image_path_to_save=config["images_dir_path"], launch_number=''):
    response = requests.get(url)
    response.raise_for_status()

    Path(config['images_dir_path']).mkdir(parents=True, exist_ok=True)
    pic_name = f'flight-{launch_number}_{url.split("/")[-1]}'
    with open(f'{image_path_to_save}/{pic_name}', 'wb') as file:
        file.write(response.content)


if __name__ == '__main__':

    latest_launch_images = fetch_spacex_latest_launch_images()
    for launch_number, launch_images in latest_launch_images.items():
        for launch_image in launch_images:
            download_launch_image(launch_image, launch_number=launch_number)
