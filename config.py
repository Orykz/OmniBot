from dotenv import load_dotenv
import os
from errors import ERRORS, SUCCESS, FILE_ERROR, KEY_ERROR


def _load_env() -> int:
    if not load_dotenv():
        return FILE_ERROR

    return SUCCESS


error = _load_env()
if error:
    print(ERRORS[error])
    exit()

try:
    DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
    WEATHER_API_KEY = os.environ["WEATHER_API_KEY"]
except KeyError:
    print(ERRORS[KEY_ERROR])
    exit()
