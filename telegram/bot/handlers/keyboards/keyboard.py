from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from bot.texts import ACTIVITY, KEYBOARD

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=KEYBOARD['workout']),
        ],
        # [
        #     KeyboardButton(text=KEYBOARD['profile'])
        # ],
    ],
    resize_keyboard=True,
)

# TODO redo
# workout = ReplyKeyboardMarkup(
#     keyboard=[
#         [
#             KeyboardButton(text=KEYBOARD['1_workout']),
#             KeyboardButton(text=KEYBOARD['2_workout']),
#             KeyboardButton(text=KEYBOARD['3_workout']),
#         ],
#         [
#             KeyboardButton(text=KEYBOARD['date_workout']),
#         ],
#         [
#             KeyboardButton(text=KEYBOARD['back']),
#         ],
#     ],
#     resize_keyboard=True,
# )

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


def get_workout_group_keyboard(groups: list[str]) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[[item] for item in groups], resize_keyboard=True)


def get_workout_trainings_keyboard(trainings_number: int) -> ReplyKeyboardMarkup:
    trainings = [[str(KEYBOARD[f'{training + 1}_workout'])] for training in range(trainings_number)]
    trainings.append([str(KEYBOARD['date_workout'])])
    trainings.append([str(KEYBOARD['back'])])
    workout = ReplyKeyboardMarkup(
        keyboard=trainings,
        resize_keyboard=True,
    )
    return workout
