import logging
from typing import Any, Optional

from apiclient import discovery
from config import get_cred_file
from google.oauth2 import service_account

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


class Sheet:
    def __init__(self, spreadsheet_id: str):
        self.spreadsheet_id = spreadsheet_id
        self._cred_filepath = get_cred_file()
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
