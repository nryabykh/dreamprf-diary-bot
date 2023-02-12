import json
import os.path
import re
from typing import Optional

from dreamprf_diary_bot import config


def register(user_id: int, link: str) -> Optional[str]:
    pattern = 'https://docs.google.com/spreadsheets/d/(.*?)/'
    match = re.match(pattern, link)
    if not match:
        return None

    sid = match.groups(1)[0]
    user = str(user_id)
    if not os.path.exists(config.USERS_PATH):
        with open(config.USERS_PATH, 'w') as fw:
            data = {user: sid}
            json.dump(data, fw, indent=4)
    else:
        with open(config.USERS_PATH, 'r+') as fw:
            data = json.load(fw)
            if user in data:
                data.pop(user)
            data[user] = sid
            fw.seek(0)
            json.dump(data, fw, indent=4)

    return sid
