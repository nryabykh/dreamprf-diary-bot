import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_DREAMPRF_TOKEN')
CRED_FILENAME = os.getenv('DREAMPRF_GSHEET_CRED_PATH')

# internal file paths
BASE_DIR = Path(__file__).resolve().parent
STATE_PATH = './db/state.json'
USERS_PATH = './db/user_sid.json'

# default sheet names
FIRST_SHEET = '0-14 дней'
SECOND_SHEET = '14-27 дней'

# default sheet ranges
RANGE = 'A:DH'
DATES_RANGE = 'A3:GH3'

# default ranges and column and row numbers
TIME_COL = 3
NOTES_COL = 4
DAY_ROW_INDEX = 6
EVENING_ROW_INDEX = 38
EVENING_LENGTH = 6
NIGHT_ROW_INDEX = 46
NIGHT_LENGTH = 12
PERIOD = 8
DAY_LENGTH = 6

DATE_FORMAT = '%d.%m.%Y'
TIME_FORMAT = '%H:%M'
