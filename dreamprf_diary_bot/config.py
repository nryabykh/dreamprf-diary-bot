import json
import logging
import os
from pathlib import Path
from typing import Optional

import tomli

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_DREAMPRF_TOKEN')
RANGE = '0-14 дней!A:DH'
DATES_RANGE = '0-14 дней!A3:GH3'

TIME_COL = 3
NOTES_COL = 4
PERIOD = 8
DAY_ROW_INDEX = 6
DAY_LENGTH = 6
EVENING_ROW_INDEX = 38
EVENING_LENGTH = 6
NIGHT_ROW_INDEX = 46
NIGHT_LENGTH = 12


def get_cred_file():
    folder = _get_secrets_folder()
    config = _get_config()
    return folder / config['google']['credentials_filename']


def _get_config():
    folder = _get_secrets_folder()
    with open(folder / 'secrets.toml', 'rb') as f:
        config = tomli.load(f)
    return config


def _get_secrets_folder():
    return Path(__file__).parent.parent / '.secrets'


def get_spreadsheet_id(user_id: int) -> Optional[str]:
    with open('user_sid.json', 'r') as f:
        data = json.load(f)
    return data.get(str(user_id), None)


# SPREADSHEET_ID = get_spreadsheet_id()