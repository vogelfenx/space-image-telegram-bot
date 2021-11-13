# Telegram bot for posting space images to telegram channel  

This project implemented a module to fetch & publish space images to telegram channel using Telegram Bot API.
The theme of the images is all about space and the universe. 
The images are fetched from different sources:
  - [r/SpaceX API](https://docs.spacexdata.com/)
  - [NASA API](https://api.nasa.gov/)

## First steps
1. Clone / download the repository
2. Read install and configuration steps
3. Read user manual. 

## How to install & configure
1. Install Python3 and project dependencies  
    Python3 should be already installed.   
    
    The project uses Pipenv tool, that automatically creates a virtual environment and install all project dependencies.  
    Please refer to Pipenv [documentation](https://pypi.org/project/pipenv/) to install it.

    When Pipenv is installed, use the following command to create virtual environment and install dependencies:
    ```
    pipenv install --dev
    ```
    To activate this project's virtualenv, run:
    ```
    pipenv shell
    ``` 

2. Create Telegram Bot & generate authentication token.
    Telegram Bot is needed to publish messages (e.g. images, posts etc.) to your channel. 

    Please read the official [documentation](https://core.telegram.org/bots#3-how-do-i-create-a-bot) in order to create a bot using BotFather.

    Once you've created a bot and received your authentication token, add the bot to your channel and make it an administrator. Afterward the channel id should be placed in configuration file ``.config``:
    ```
    ...
    telegram_chat_id='@your_channel_id'
    ...
    ```

    Finally, place the generated authentication token in a file named `.secrets`. The file should be located in root directory of the project.
    The authentication token should look like:
    ```
    TELEGRAM_BOT_TOKEN=2109472554:DDE8MfhNK8J_x75Fx-A_RZ7b3mYK3PhOO10
    ```

3. Generate NASA API key
    This module works with NASA API, which requires a API key.  
    To generate a API key follow the instructions in the official NASA documentation [page](https://api.nasa.gov/).

    Finally, place the key in the `.secrets` file like:
    ```
    NASA_API_KEY=AeFGjzewVGGySj5MLksqOcJf8HwrcXmkeslbNshh
    ```

## Usage and configuration
1. To run the module use the following command within created virtual environment:
    ```
    python3 main.py  
    ```
    This module fetches images with meta information such as date, description and directly posts it to your channel.

2. Another configurations:  
    Use the configuration file `.config` to configure more precise settings. 

    The first part of the file specifies the API root URLs and should not be changed or changed carefully. 
    ```
    API_SPACEX_URL=https://api.spacexdata.com/v3
    API_NASA_URL=https://api.nasa.gov/planetary
    API_NASA_EPIC_URL=https://api.nasa.gov/EPIC
    ```

    The rest of the file is used to configure settings such as the location to save images, the publishing interval time, and the channel ID.

    ````
    images_dir_path=data/images
    telegram_chat_id='@your_channel_id'
    image_publishing_interval_seconds=86400
    ````
    You are free to change it!

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
