from datetime import datetime

from bot.texts import KEYBOARD


def is_valid_weight(weight: str):
    return weight.replace('.', '').isnumeric() and float(weight) > 0 and float(weight) < 200


def is_valid_height(height: str):
    return height.isnumeric() and int(height) > 0 and int(height) < 300


def is_valid_years(years: str):
    return years.isnumeric() and int(years) > 0 and int(years) < 100


def get_workout_order(message: str) -> int:
    if message == KEYBOARD['first_workout']:
        return 1
    if message == KEYBOARD['second_workout']:
        return 2
    return 3


def get_order_from_date(date: datetime) -> int:
    if date.weekday() in {0, 1}:
        return 1
    elif date.weekday() in {2, 3}:
        return 2
    return 3
