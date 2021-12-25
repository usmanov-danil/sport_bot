from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from bot.texts import KEYBOARD

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=KEYBOARD['workout']),
        ],
        [KeyboardButton(text=KEYBOARD['weights']), KeyboardButton(text=KEYBOARD['profile'])],
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
