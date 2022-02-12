from datetime import datetime, timedelta, timezone

from bot.texts import KEYBOARD, LAST_WEEK, THIS_WEEK


def is_valid_weight(weight: str):
    return weight.replace('.', '').isnumeric() and float(weight) > 0 and float(weight) < 200


def is_valid_height(height: str):
    return height.isnumeric() and int(height) > 0 and int(height) < 300


def is_valid_years(years: str):
    return years.isnumeric() and int(years) > 0 and int(years) < 100


def get_workout_order(message: str) -> int:
    return int(message.split(' ')[0])


def get_week_from_date(date: datetime) -> str:
    start_week = get_start_week(date)
    end_week = start_week + timedelta(days=6)
    today = get_naive_date(datetime.today())
    week_dates = start_week.strftime("%d/%m") + " \- " + end_week.strftime("%d/%m")
    if start_week <= today <= end_week:
        week_dates += f"\({THIS_WEEK}\)"
    if start_week <= today - timedelta(days=7) <= end_week:
        week_dates += f"\({LAST_WEEK}\)"
    return week_dates


def get_start_week(date: datetime):
    today = datetime.today()
    date = date if date else today
    date = get_naive_date(date)
    start_week_date = date - timedelta(days=date.weekday())
    return start_week_date


def get_naive_date(date: datetime):
    return date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
