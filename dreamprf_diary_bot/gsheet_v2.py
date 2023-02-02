"""
Template for using gspread without bare Google API
https://github.com/burnash/gspread
"""

from pathlib import Path

import tomli


def get_cred_file():
    folder = Path(__file__).parent.parent / '.secrets'
    with open(folder / 'secrets.toml', 'rb') as f:
        config = tomli.load(f)
    return folder / config['google']['filename']
