from datetime import datetime

from dreamprf_diary_bot.config import DATES_RANGE
from dreamprf_diary_bot.services.gsheet import Doc


def get_night_wake_range(sheet: Doc, time: datetime):
    dates = sheet.get_data(sheet_range=DATES_RANGE, sheet_name=get_sheet_name(sheet))
    col_to_write = dates[0].index(time.strftime('%d.%m.%Y'))
    filled_col = sheet.get_data(sheet_range=_get_night_range(RANGE, col_to_write), sheet_name=get_sheet_name(sheet))
    last_row_ix = len(filled_col)
    write_range = _get_night_write_range(RANGE, col_to_write, last_row_ix)
    return write_range