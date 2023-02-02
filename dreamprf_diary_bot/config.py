from pathlib import Path

import tomli


def get_cred_file():
    folder = _get_secrets_folder()
    config = _get_config()
    return folder / config['google']['credentials_filename']


def get_spreadsheet_id():
    config = _get_config()
    return config['google']['spreadsheet_id']


def _get_config():
    folder = _get_secrets_folder()
    with open(folder / 'secrets.toml', 'rb') as f:
        config = tomli.load(f)
    return config


def _get_secrets_folder():
    return Path(__file__).parent.parent / '.secrets'
