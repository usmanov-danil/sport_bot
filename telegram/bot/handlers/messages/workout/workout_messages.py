from typing import Text

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery
from bot.handlers.calendar import DialogCalendar, calendar_callback
from bot.handlers.fsm import Workout
from bot.handlers.keyboard import get_workout_group_keyboard, menu, workout
from bot.loader import bot, config_manager, dp
from bot.texts import (
    ASK_TO_REGISTER,
    CHOOSE_DATE,
    INCORRECT_INPUT,
    KEYBOARD,
    WAIT_ADMIN_GROUP,
    WORKOUT_GROUPS,
    WORKOUT_MAIN_TEXT,
)
from services.user_managment import get_user_groups, is_user_exists


# Workout page
@dp.message_handler(Text(KEYBOARD['workout']))
async def process_start_command(message: types.Message):
    # TODO: make more beautiful
    if is_user_exists(config_manager.repository, message.from_user):
        if user_grops := await get_user_groups(config_manager.repository, message.from_user):
            await Dispatcher.get_current().current_state().update_data(groups=user_grops)
            await message.answer(
                WORKOUT_GROUPS, reply_markup=get_workout_group_keyboard(user_grops)
            )
            await Workout.waiting_for_group.set()
        else:
            await message.answer(WAIT_ADMIN_GROUP, reply_markup=menu)
    else:
        await message.answer(ASK_TO_REGISTER)
        return


@dp.message_handler(state=Workout.waiting_for_group)
async def waiting_for_group(message: types.Message, state: FSMContext):
    user_groups = await state.get_data()
    if not (message.text in user_groups.get('groups', {})):
        await message.answer(INCORRECT_INPUT)
        return

    await state.update_data(user_group=message.text)
    await Workout.next()
    await message.answer(WORKOUT_MAIN_TEXT, reply_markup=workout)


@dp.message_handler(Text(KEYBOARD['first_workout']), state=Workout.waiting_for_workout)
async def process_start_command(message: types.Message, state: FSMContext):
    await message.answer('1')


@dp.message_handler(Text(KEYBOARD['second_workout']), state=Workout.waiting_for_workout)
async def process_start_command(message: types.Message, state: FSMContext):
    await message.answer('2')


@dp.message_handler(Text(KEYBOARD['third_workout']), state=Workout.waiting_for_workout)
async def process_start_command(message: types.Message, state: FSMContext):
    await message.answer('3')


# Workout by day
@dp.message_handler(Text(KEYBOARD['date_workout']), state=Workout.waiting_for_workout)
async def calculate_kbgu(message: types.Message, state: FSMContext):
    if is_user_exists(config_manager.repository, message.from_user):
        await message.answer(CHOOSE_DATE, reply_markup=await DialogCalendar().start_calendar())
    else:
        await message.answer(ASK_TO_REGISTER)
        return


@dp.callback_query_handler(calendar_callback.filter(), state=Workout.waiting_for_workout)
async def process_dialog_calendar(
    callback_query: CallbackQuery, callback_data: dict, *args, **kwargs
):
    selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'You selected {date.strftime("%d/%m/%Y")}', reply_markup=workout
        )
