import logging

from dreamprf_diary_bot import static, config
from dreamprf_diary_bot.services import gsheet, utils
from dreamprf_diary_bot.services.gsheet import Doc

logger = logging.getLogger(__name__)


def add_wake(user_id: int) -> str:
    sid = gsheet.get_spreadsheet_id(user_id)
    if not sid:
        raise KeyError(static.no_sid_message)

    sheet = Doc(spreadsheet_id=sid)
    time = utils.get_current_datetime()
    time_str = time.strftime(config.TIME_FORMAT)
    write_range = sheet.get_next_wake_time_range(time)

    logger.info(f'Insert wake time {time_str} into the cell {write_range}')
    sheet.update(write_range, [[time_str]], sheet_name=sheet.get_sheet(time))

    return time_str


def add_note(user_id: int, note: str, selected_wake_time: str) -> str:
    sid = gsheet.get_spreadsheet_id(user_id)
    if not sid:
        raise KeyError(static.no_sid_message)

    sheet = Doc(spreadsheet_id=sid)
    time = utils.get_current_datetime()
    write_range = sheet.get_note_range(time, selected_wake_time)

    logger.info(f'Insert the "{note}" as note of the wake time {selected_wake_time} into the cell {write_range}')
    sheet.update(write_range, [[note]], sheet_name=sheet.get_sheet(time))

    return selected_wake_time if selected_wake_time else time.strftime(config.TIME_FORMAT)


def get_all_wake_times_and_notes(user_id: int) -> list[str]:
    sid = gsheet.get_spreadsheet_id(user_id)
    if not sid:
        raise KeyError(static.no_sid_message)

    sheet = Doc(spreadsheet_id=sid)
    time = utils.get_current_datetime()
    times_notes_range = sheet.get_all_times_and_notes_range(time)

    logger.info(f'Getting all wake times and notes from the range {times_notes_range}')
    data = sheet.get_data(times_notes_range, sheet_name=sheet.get_sheet(time))

    return [' - '.join(line) for line in data]
