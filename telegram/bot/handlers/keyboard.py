from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from bot.texts import ACTIVITY, KEYBOARD

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=KEYBOARD['workout']),
        ],
        [KeyboardButton(text=KEYBOARD['profile'])],
        [
            KeyboardButton(text=KEYBOARD['attendance']),
        ],
    ],
    resize_keyboard=True,
)

workout = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=KEYBOARD['first_workout']),
        ],
        [KeyboardButton(text=KEYBOARD['second_workout'])],
        [
            KeyboardButton(text=KEYBOARD['third_workout']),
        ],
        [
            KeyboardButton(text=KEYBOARD['back']),
        ],
    ],
    resize_keyboard=True,
)

profile = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=KEYBOARD['get_profile_info']),
        ],
        [KeyboardButton(text=KEYBOARD['change_profile'])],
        [
            KeyboardButton(text=KEYBOARD['calculate_kbgu']),
        ],
        [
            KeyboardButton(text=KEYBOARD['back']),
        ],
    ],
    resize_keyboard=True,
)

sex_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=KEYBOARD['male']),
        ],
        [
            KeyboardButton(text=KEYBOARD['female']),
        ],
    ],
    resize_keyboard=True,
)

activity_keyboard = ReplyKeyboardMarkup(
    keyboard=[[item] for item in ACTIVITY.keys()],
    resize_keyboard=True,
)


remove_keyboard = ReplyKeyboardRemove()
