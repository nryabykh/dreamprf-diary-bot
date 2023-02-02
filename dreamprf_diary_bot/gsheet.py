import logging
from pathlib import Path
from typing import Any

import tomli
from google.oauth2 import service_account
from apiclient import discovery

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def get_cred_file():
    folder = Path(__file__).parent.parent / '.secrets'
    with open(folder / 'secrets.toml', 'rb') as f:
        config = tomli.load(f)
    return folder / config['google']['filename']


class Sheet:
    def __init__(self, spreadsheet_id: str):
        self.spreadsheet_id = spreadsheet_id
        self._cred_filepath = get_cred_file()
        self._creds = service_account.Credentials.from_service_account_file(self._cred_filepath)
        self._service = discovery.build('sheets', 'v4', credentials=self._creds)
        self._sheet = self._service.spreadsheets()

    def get_service(self):
        return self._service

    def get_data(self, sheet_range: str):
        get_sheet = self._sheet.values().get(spreadsheetId=self.spreadsheet_id, range=sheet_range).execute()
        values = get_sheet.get('values', [])
        return values

    def update(self, sheet_range: str, values: list[list[Any]]):
        # TODO Check size of `sheet_range` and size of `values`

        body = {'values': values}
        result = self._sheet.values().update(
            spreadsheetId=self.spreadsheet_id,
            range=sheet_range,
            valueInputOption='USER_ENTERED',
            body=body
        ).execute()
        logging.info(f"{result.get('updatedCells')} cells updated")
        return
