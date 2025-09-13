import os
import json
from dotenv import load_dotenv
from typing import Dict, Any
from errors import ERRORS, SUCCESS, FILE_404_ERROR, KEY_ERROR


def _get_config() -> Dict[str, Any]:
    try:
        with open("data/config.json", "r") as json_file:
            config = json.load(json_file)
        return config

    except FileNotFoundError:
        print(ERRORS[FILE_404_ERROR])
        exit()


def _load_env() -> int:
    if not load_dotenv():
        return FILE_404_ERROR

    return SUCCESS


config = _get_config()
error = _load_env()
if error:
    print(ERRORS[error])
    exit()

try:
    DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
    WEATHER_API_KEY = os.environ["WEATHER_API_KEY"]

    db_config = config["database"]
    DB_PATH = db_config["db_path"]

    memes_config = config["memes"]
    MEME_BU = memes_config["base_url"]
    MEME_SUBS = memes_config["subreddits"]
    MEME_NSFW = memes_config["allow_nsfw"]

    weather_config = config["weather"]
    WEATHER_BU = weather_config["base_url"]
    WEATHER_CURRENT = weather_config["current"]

except KeyError:
    print(ERRORS[KEY_ERROR])
    exit()
