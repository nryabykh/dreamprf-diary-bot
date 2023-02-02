from google.oauth2 import service_account
from apiclient import discovery

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
filepath = '/Users/nikolai.ryabih/dev/.creds/client_secret.json'
creds = service_account.Credentials.from_service_account_file(filepath)

spreadsheet_id = '14eDErJv8k2dLD1xdeGsWhRVL785LOX5vk_OMecsYWtU'

service = discovery.build('sheets', 'v4', credentials=creds)

SAMPLE_RANGE_NAME = '0-14 дней!A:DH'

sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=spreadsheet_id, range=SAMPLE_RANGE_NAME).execute()
values = result.get('values', [])

TIME_COL = 3
NOTES_COL = 4
PERIOD = 8
DAY_ROW_INDEX = 6
DAY_LENGTH = 6
EVENING_ROW_INDEX = 38
EVENING_LENGTH = 6
NIGHT_ROW_INDEX = 46
NIGHT_LENGTH = 12


def get_first_night():
    return [f'{v[TIME_COL]} - {v[NOTES_COL]}' for v in values[NIGHT_ROW_INDEX:NIGHT_ROW_INDEX+NIGHT_LENGTH]]
