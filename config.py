import os
import json
from dotenv import load_dotenv
from typing import Dict, Any
from errors import ERRORS, FILE_404_ERROR, KEY_ERROR

CONFIG_PATH = "data/config.json"
DOTENV_PATH = "data/.env"


def _get_config(config_path: str) -> Dict[str, Any]:
    try:
        with open(config_path, "r") as json_file:
            config = json.load(json_file)
        return config

    except FileNotFoundError:
        print(ERRORS[FILE_404_ERROR].replace("<name>", "config"))
        exit()


# Load all configurations to the bot application for use
config = _get_config(CONFIG_PATH)
if not load_dotenv(DOTENV_PATH):
    print(ERRORS[FILE_404_ERROR].replace("<name>", "env"))
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

    reminders_config = config["reminders"]
    REM_LOOP_SEC = reminders_config["loop_sec"]
    REM_NOTE_IND = reminders_config["note_ind"]

except KeyError:
    print(ERRORS[KEY_ERROR])
    exit()
