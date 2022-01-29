import re
from typing import Text, Union

from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from bot.handlers.fsm import ProfileKBGU, ProfileRegistration
from bot.handlers.keyboards.keyboard import (
    activity_keyboard,
    profile,
    remove_keyboard,
    sex_keyboard,
)
from bot.handlers.messages.utils import is_valid_height, is_valid_weight, is_valid_years
from bot.loader import config_manager, dp
from bot.texts import (
    ACTIVITY,
    ASK_TO_REGISTER,
    INCORRECT_INPUT,
    KEYBOARD,
    PROFILE_KBGU_STEPS,
    PROFILE_MAIN_TEXT,
    PROFILE_STEPS,
)
from models.base import User
from services.calculation import calculate_kbgu_levels
from services.user_managment import (
    get_user_data,
    is_personal_data_exists,
    is_user_exists,
    save_personal_data,
)


# Profile page
@dp.message_handler(Text(equals=KEYBOARD['profile']))
async def process_profile(message: types.Message):
    await message.reply(PROFILE_MAIN_TEXT, reply_markup=profile)


@dp.message_handler(Text(KEYBOARD['get_profile_info']))
async def get_profile_info(message: types.Message):
    answer = await get_user_data(config_manager.repository, message.from_user)
    await message.answer(answer)


@dp.message_handler(Text(KEYBOARD['change_profile']))
async def change_profile(message: types.Message):
    if is_user_exists(config_manager.repository, message.from_user):
        await message.answer(PROFILE_STEPS['first'], reply_markup=remove_keyboard)
        await ProfileRegistration.waiting_for_weight.set()
    else:
        await message.answer(ASK_TO_REGISTER)
        return


@dp.message_handler(state=ProfileRegistration.waiting_for_weight)
async def weight_setted(message: types.Message, state: FSMContext):
    weight = re.sub('[^0-9.]', '', message.text)
    if not is_valid_weight(weight):
        await message.answer(INCORRECT_INPUT)
        return
    await state.update_data(weight=float(weight))

    await ProfileRegistration.next()
    await message.answer(PROFILE_STEPS['second'])


@dp.message_handler(state=ProfileRegistration.waiting_for_height)
async def height_setted(message: types.Message, state: FSMContext):
    height = re.sub('[^0-9]', '', message.text)
    if not is_valid_height(height):
        await message.answer(INCORRECT_INPUT)
        return
    await state.update_data(height=int(height))

    await ProfileRegistration.next()
    await message.answer(PROFILE_STEPS['third'])


@dp.message_handler(state=ProfileRegistration.waiting_for_year)
async def year_setted(message: types.Message, state: FSMContext):
    years = re.sub('[^0-9]', '', message.text)
    if not is_valid_years(years):
        await message.answer(INCORRECT_INPUT)
        return
    await state.update_data(years=int(years))
    user_data: dict[str, Union[int, float]] = await state.get_data()
    user = User.from_aiogram_user(message.from_user)
    user.set_personal_params(
        height=user_data['height'], weight=user_data['weight'], years=user_data['years']
    )
    msg = await save_personal_data(config_manager.repository, user)
    await message.answer(msg, reply_markup=profile)
    await state.finish()


@dp.message_handler(Text(KEYBOARD['calculate_kbgu']))
async def calculate_kbgu(message: types.Message):
    if is_user_exists(config_manager.repository, message.from_user) and is_personal_data_exists(
        config_manager.repository, message.from_user
    ):
        await message.answer(PROFILE_KBGU_STEPS['first'], reply_markup=sex_keyboard)
        await ProfileKBGU.waiting_for_sex.set()
    else:
        await message.answer(ASK_TO_REGISTER)
        return


@dp.message_handler(state=ProfileKBGU.waiting_for_sex)
async def sex_setted(message: types.Message, state: FSMContext):
    if not (message.text == KEYBOARD['male'] or message.text == KEYBOARD['female']):
        await message.answer(INCORRECT_INPUT)
        return
    await state.update_data(sex=message.text)

    await ProfileKBGU.next()
    await message.answer(PROFILE_KBGU_STEPS['second'], reply_markup=activity_keyboard)


@dp.message_handler(state=ProfileKBGU.waiting_for_activity)
async def activity_setted(message: types.Message, state: FSMContext):
    if not (message.text in ACTIVITY.keys()):
        await message.answer(INCORRECT_INPUT)
        return
    await state.update_data(activity=ACTIVITY[message.text])
    data = await state.get_data()

    msg = await calculate_kbgu_levels(
        config_manager.repository, data['sex'], data['activity'], message.from_user
    )
    await message.answer(msg, reply_markup=profile)
    await state.finish()
