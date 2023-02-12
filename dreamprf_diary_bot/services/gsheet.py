import json
import logging
import os
from datetime import datetime, timezone, timedelta
from typing import Any, Optional

from apiclient import discovery
from google.oauth2 import service_account

from dreamprf_diary_bot import config
from dreamprf_diary_bot.services import utils

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


class Doc:
    def __init__(self, spreadsheet_id: str):
        self.spreadsheet_id = spreadsheet_id
        self._cred_filepath = config.CRED_FILENAME
        self._creds = service_account.Credentials.from_service_account_file(self._cred_filepath)
        self._service = discovery.build('sheets', 'v4', credentials=self._creds)
        self._sheet = self._service.spreadsheets()
        self._start_date = self.get_data('D3:D3')[0][0]

    def get_service(self):
        return self._service

    def get_start_date(self):
        return self._start_date

    def get_data(self, sheet_range: str, sheet_name: Optional[str] = None):
        if sheet_name:
            sheet_range = f'{sheet_name}!{sheet_range}'
        get_sheet = self._sheet.values().get(spreadsheetId=self.spreadsheet_id, range=sheet_range).execute()
        values = get_sheet.get('values', [[]])
        return values

    def update(self, sheet_range: str, values: list[list[Any]], sheet_name: Optional[str] = None):
        # TODO Check size of `sheet_range` and size of `values`

        if sheet_name:
            sheet_range = f'{sheet_name}!{sheet_range}'

        body = {'values': values}
        result = self._sheet.values().update(
            spreadsheetId=self.spreadsheet_id,
            range=sheet_range,
            valueInputOption='USER_ENTERED',
            body=body
        ).execute()
        logging.info(f"{result.get('updatedCells')} cells updated")
        return

    def get_sheet(self, time: datetime = None):
        if not time:
            time = utils.get_current_datetime()
        tz = timezone(timedelta(hours=6))
        start_date = datetime.strptime(self._start_date, config.DATE_FORMAT).astimezone(tz)
        sheet_name = config.FIRST_SHEET if time < start_date + timedelta(days=14) else config.SECOND_SHEET
        return sheet_name

    def get_all_dates_on_sheet(self, sheet: str = None):
        if not sheet:
            sheet = self.get_sheet()
        return self.get_data(sheet_range=config.DATES_RANGE, sheet_name=sheet)

    def get_night_col(self, time: datetime):
        dates = self.get_all_dates_on_sheet()[0]
        current_date = time.strftime(config.DATE_FORMAT)
        if current_date not in dates:
            raise KeyError(f'Date {current_date} not found in the list of dates: {dates}')

        col_ix = dates.index(current_date)
        col_data = self.get_data(sheet_range=get_time_col_range(col_ix), sheet_name=self.get_sheet())

        return col_ix, col_data

    def get_next_wake_time_range(self, time: datetime):
        col_ix, col_data = self.get_night_col(time)

        # empty cells not included in response, so len(col_data) is the index of the cell right after the last filled
        row_ix = len(col_data)

        return get_cell_range_from_ids(row_ix, col_ix)

    def get_note_range(self, current_time: datetime, time_to_edit: str = None):
        col_ix, col_data = self.get_night_col(current_time)

        # add leading zero to the times in col_data if needed (0:46 --> 00:46)
        for i, cell in enumerate(col_data[config.NIGHT_ROW_INDEX:]):
            if cell and ':' in cell[0] and len(cell[0]) < 5:
                col_data[config.NIGHT_ROW_INDEX + i] = [f'0{cell[0]}']

        if not time_to_edit:
            row_ix = len(col_data) - 1
        else:
            if len(time_to_edit) < 5:
                time_to_edit = f'0{time_to_edit}'
            row_ix = col_data.index([time_to_edit])

        if row_ix == config.NIGHT_ROW_INDEX - 1:
            return None

        return get_cell_range_from_ids(row_ix, col_ix + 1)

    def get_all_times_and_notes_range(self, time: datetime) -> str:
        col_ix, _ = self.get_night_col(time)

        return get_range_from_ids(config.NIGHT_ROW_INDEX, config.NIGHT_LENGTH, col_ix, 2)


def get_spreadsheet_id(user_id: int) -> Optional[str]:
    if not os.path.exists(config.USERS_PATH):
        return None

    with open(config.USERS_PATH, 'r') as f:
        data = json.load(f)
    return data.get(str(user_id), None)


def get_time_col_range(col_ix: int) -> str:
    return f'R1C{col_ix + 1}:R1000C{col_ix + 1}'


def get_cell_range_from_ids(row_ix: int, col_ix: int) -> str:
    # rows and columns numeration starts with 1 in Google Sheets
    row_number = row_ix + 1
    col_number = col_ix + 1

    return f'R{row_number}C{col_number}:R{row_number}C{col_number}'


def get_range_from_ids(start_row_ix: int, rows: int, start_col_ix: int, cols: int) -> str:
    start_row_number = start_row_ix + 1
    start_col_number = start_col_ix + 1

    return f'R{start_row_number}C{start_col_number}:R{start_row_number + rows - 1}C{start_col_number + cols - 1}'
