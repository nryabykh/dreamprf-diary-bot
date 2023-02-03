import json
import logging
import re
from datetime import datetime, timedelta, timezone

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.files import JSONStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State

import static
from config import TELEGRAM_BOT_TOKEN, TIME_COL, NOTES_COL, NIGHT_ROW_INDEX, NIGHT_LENGTH, DATES_RANGE, \
    RANGE, get_spreadsheet_id
from gsheet import Sheet


if not TELEGRAM_BOT_TOKEN:
    exit('Specify TELEGRAM_BOT_DREAMPRF_TOKEN as environment variable')

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot, storage=JSONStorage('state.json'))


class NightRegister(StatesGroup):
    start = State()


@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    response = static.start_message
    await message.reply(response, reply=False)


@dp.message_handler(commands='help')
async def send_welcome(message: types.Message):
    response = static.help_message
    await message.reply(response, reply=False)


@dp.message_handler(commands='night', state='*')
async def cmd_night(message: types.Message, state: FSMContext):
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
    await message.answer("Включили режим записи ночных пробуждений.", reply_markup=keyboard)
    await state.set_state(NightRegister.start.state)


@dp.message_handler(Text(equals="Добавить НП"), state=NightRegister.start)
async def post_night_wake(message: types.Message, state: FSMContext):
    sid = get_spreadsheet_id(message.from_user.id)
    if not sid:
        await message.reply('Не удалось найти ссылку на таблицу для вас. Отправьте ссылку на таблицу боту, не находясь в режиме записи пробуждений')
        return
    sheet = Sheet(spreadsheet_id=sid)
    time = get_datetime_to_fill()
    time_str = time.strftime("%H:%M")
    write_range = get_night_wake_range(sheet, time)
    logging.info(f'Night wake-up at {time_str}. Log into range {write_range}')
    sheet.update(write_range, [[time_str]])
    await message.reply(f"Записано НП в {time_str}", reply=False)


@dp.message_handler(commands="end", state=NightRegister.start)
async def cmd_night(message: types.Message, state: FSMContext):
    await message.reply(
        "Вышли из режима записи ночных пробуждений.", reply_markup=types.ReplyKeyboardRemove(), reply=False
    )
    await state.finish()


@dp.message_handler(state=NightRegister.start)
async def note(message: types.Message, state: FSMContext):
    sid = get_spreadsheet_id(message.from_user.id)
    if not sid:
        await message.reply('Не удалось найти ссылку на таблицу для вас. Отправьте ссылку на таблицу боту, не находясь в режиме записи пробуждений')
        return
    sheet = Sheet(spreadsheet_id=sid)
    cmt = message.text
    time = get_datetime_to_fill()
    write_range = get_night_comment_range(sheet, time)
    if not write_range:
        return
    logging.info(f'Comment for the last night wake-up. Log into range {write_range}')
    last_night_time = get_last_night_time(sheet, time)
    sheet.update(write_range, [[cmt]])
    await message.reply(f'Добавили комментарий к просыпанию в {last_night_time}', reply=False)


@dp.message_handler()
async def echo(message: types.Message):
    pattern = 'https://docs.google.com/spreadsheets/d/(.*?)/'
    match = re.match(pattern, message.text)
    if match:
        sid = match.groups(1)[0]
        user_id = message.from_user.id
        with open('user_sid.json', 'r+') as f:
            data = json.load(f)
            if user_id in data:
                data.pop(user_id)
            data[user_id] = sid
            f.seek(0)
            json.dump(data, f, indent=4)
        await message.reply('Идентификатор таблицы сохранен', reply=False)
    else:
        await message.reply(f'Для записи комментария к НП перейдите в режим /night и добавьте НП.')


def get_first_night(data: list[list[str]]):
    return [f'{v[TIME_COL]} - {v[NOTES_COL]}' for v in data[NIGHT_ROW_INDEX:NIGHT_ROW_INDEX+NIGHT_LENGTH]]


def get_datetime_to_fill():
    now = datetime.now(timezone.utc)
    now = now.astimezone(timezone(timedelta(hours=6)))
    return now - timedelta(days=1) if now.hour < 10 else now


def get_night_wake_range(sheet: Sheet, time: datetime):
    dates = sheet.get_data(sheet_range=DATES_RANGE)
    col_to_write = dates[0].index(time.strftime('%d.%m.%Y'))
    filled_col = sheet.get_data(sheet_range=_get_night_range(RANGE, col_to_write))
    last_row_ix = len(filled_col)
    write_range = _get_night_write_range(RANGE, col_to_write, last_row_ix)
    return write_range


def get_night_comment_range(sheet: Sheet, time: datetime):
    dates = sheet.get_data(sheet_range=DATES_RANGE)
    col_to_write = dates[0].index(time.strftime('%d.%m.%Y'))
    filled_col = sheet.get_data(sheet_range=_get_night_range(RANGE, col_to_write))
    last_row_ix = len(filled_col)
    if last_row_ix == 45:
        return None
    write_range = _get_night_write_range(RANGE, col_to_write + 1, last_row_ix - 1)
    return write_range


def get_last_night_time(sheet: Sheet, time: datetime):
    dates = sheet.get_data(sheet_range=DATES_RANGE)
    col_to_write = dates[0].index(time.strftime('%d.%m.%Y'))
    return sheet.get_data(sheet_range=_get_night_range(RANGE, col_to_write))[-1][0]


def _get_night_range(r: str, col_ix: int) -> str:
    sheet_name = r.split('!')[0]
    return f'{sheet_name}!R1C{col_ix+1}:R1000C{col_ix+1}'


def _get_night_write_range(r: str, col_ix: int, row_ix: int) -> str:
    sheet_name = r.split('!')[0]
    return f'{sheet_name}!R{row_ix+1}C{col_ix+1}:R{row_ix+1}C{col_ix+1}'


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
