import logging
import os
from datetime import datetime

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

from gsheet import Sheet

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_DREAMPRF_TOKEN')
SPREADSHEET_ID = '14eDErJv8k2dLD1xdeGsWhRVL785LOX5vk_OMecsYWtU'
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


if not TELEGRAM_BOT_TOKEN:
    exit('Specify TELEGRAM_BOT_DREAMPRF_TOKEN as environment variable')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)
sheet = Sheet(spreadsheet_id=SPREADSHEET_ID)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    response = """
    Привет! \nЯ бот для работы с дневником сна от Екатерины Парфеновой (ekaterina.prf).
    """
    await message.reply(response)


@dp.message_handler(commands=['first'])
async def send_first_night(message: types.Message):
    data = sheet.get_data(sheet_range=RANGE)
    response = '\n'.join(get_first_night(data))
    await message.reply(response)


@dp.message_handler(commands="night")
async def cmd_night(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Добавить НП")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Добавьте ночное пробуждение"
    )
    await message.answer("Что было ночью?", reply_markup=keyboard)


@dp.message_handler(Text(equals="Добавить НП"))
async def post_night_wake(message: types.Message):
    time = datetime.now()
    time_str = time.strftime("%H:%M")
    write_range = get_night_wake_range(time)
    logging.info(f'Night wake-up at {time_str}. Log into range {write_range}')
    sheet.update(write_range, [[time_str]])
    await message.reply(f"Записано НП в {time_str}")


@dp.message_handler(commands="reset")
async def cmd_night(message: types.Message):
    await message.reply("Убрали кнопки", reply_markup=types.ReplyKeyboardRemove())


def get_first_night(data: list[list[str]]):
    return [f'{v[TIME_COL]} - {v[NOTES_COL]}' for v in data[NIGHT_ROW_INDEX:NIGHT_ROW_INDEX+NIGHT_LENGTH]]


def get_night_wake_range(time: datetime):
    dates = sheet.get_data(sheet_range=DATES_RANGE)
    col_to_write = dates[0].index(time.strftime('%d.%m.%Y'))
    filled_col = sheet.get_data(sheet_range=_get_night_range(RANGE, col_to_write))
    last_row_ix = len(filled_col)
    write_range = _get_night_write_range(RANGE, col_to_write, last_row_ix)
    return write_range


def _get_night_range(r: str, col_ix: int) -> str:
    sheet_name = r.split('!')[0]
    return f'{sheet_name}!R1C{col_ix+1}:R1000C{col_ix+1}'


def _get_night_write_range(r: str, col_ix: int, row_ix: int) -> str:
    sheet_name = r.split('!')[0]
    return f'{sheet_name}!R{row_ix+1}C{col_ix+1}:R{row_ix+1}C{col_ix+1}'


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
