from aiogram.dispatcher.filters.state import State, StatesGroup


class ProfileRegistration(StatesGroup):
    waiting_for_weight = State()
    waiting_for_height = State()
    waiting_for_year = State()


class ProfileKBGU(StatesGroup):
    waiting_for_sex = State()
    waiting_for_activity = State()


class Workout(StatesGroup):
    waiting_for_group = State()
    waiting_for_workout = State()
