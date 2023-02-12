from datetime import datetime, timedelta, timezone


def get_current_datetime() -> datetime:
    now = datetime.now(timezone.utc)
    now = now.astimezone(timezone(timedelta(hours=6)))
    return now - timedelta(days=1) if now.hour < 10 else now  # if night, take previous date

