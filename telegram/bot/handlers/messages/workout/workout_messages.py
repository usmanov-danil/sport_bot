import datetime

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery
from bot.handlers.fsm import Workout
from bot.handlers.keyboards.calendar import DialogCalendar, calendar_callback
from bot.handlers.keyboards.inline import WorkoutInline, workout_callback
from bot.handlers.keyboards.keyboard import (
    get_workout_group_keyboard,
    get_workout_trainings_keyboard,
    menu,
)
from bot.handlers.messages.utils import (
    get_naive_date,
    get_start_week,
    get_week_from_date,
    get_workout_order,
)
from bot.loader import config_manager, dp
from bot.texts import (
    ASK_TO_REGISTER,
    CHOOSE_DATE,
    INCORRECT_INPUT,
    KEYBOARD,
    LAST_WEEK,
    THIS_WEEK,
    WAIT_ADMIN_GROUP,
    WORKOUT_DONT_EXIST,
    WORKOUT_GROUPS,
    WORKOUT_MAIN_TEXT,
    WORKOUT_WEEK_DONT_EXIST,
)
from repositories.abstract import UserRepository
from services.user_managment import get_user_groups, get_workout, get_workout_count, is_user_exists


# Workout page
@dp.message_handler(Text(KEYBOARD['workout']))
async def process_workout(message: types.Message):
    # TODO: make more beautiful
    if is_user_exists(config_manager.repository, message.from_user):
        if user_grops := await get_user_groups(config_manager.repository, message.from_user):
            await Dispatcher.get_current().current_state().update_data(groups=user_grops)
            await Dispatcher.get_current().current_state().update_data(
                date=datetime.datetime.today()
            )
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
    if message.text in user_groups.get('groups', {}):
        group = message.text
        await state.update_data(user_group=group)
    elif "user_group" in user_groups:
        group = user_groups.get("user_group", "")
    else:
        await message.answer(INCORRECT_INPUT)
        return
    date = user_groups.get('date', datetime.datetime.today())
    training_count = await get_workout_count(config_manager.repository, group, date)
    if training_count < 1:
        await Workout.waiting_for_workout.set()
        await message.reply(
            text=f"{WORKOUT_WEEK_DONT_EXIST} {get_week_from_date(date)}",
            reply_markup=get_workout_trainings_keyboard(0),
        )
        return
    await message.answer(
        f"{WORKOUT_MAIN_TEXT} {get_week_from_date(date)}: ",
        reply_markup=get_workout_trainings_keyboard(training_count),
    )
    await Workout.waiting_for_workout.set()


@dp.message_handler(Text(KEYBOARD['1_workout']), state=Workout.waiting_for_workout)
@dp.message_handler(Text(KEYBOARD['2_workout']), state=Workout.waiting_for_workout)
@dp.message_handler(Text(KEYBOARD['3_workout']), state=Workout.waiting_for_workout)
@dp.message_handler(Text(KEYBOARD['4_workout']), state=Workout.waiting_for_workout)
@dp.message_handler(Text(KEYBOARD['5_workout']), state=Workout.waiting_for_workout)
@dp.message_handler(Text(KEYBOARD['6_workout']), state=Workout.waiting_for_workout)
@dp.message_handler(Text(KEYBOARD['7_workout']), state=Workout.waiting_for_workout)
@dp.message_handler(Text(KEYBOARD['8_workout']), state=Workout.waiting_for_workout)
@dp.message_handler(Text(KEYBOARD['9_workout']), state=Workout.waiting_for_workout)
@dp.message_handler(Text(KEYBOARD['10_workout']), state=Workout.waiting_for_workout)
async def process_workout(message: types.Message, state: FSMContext):
    if is_user_exists(config_manager.repository, message.from_user):
        user_groups = await state.get_data()
        group = user_groups.get('user_group')
        date = user_groups.get('date', datetime.datetime.today())
        order = get_workout_order(message.text)
        if workout := await get_workout(config_manager.repository, group, order, date=date):
            await message.reply(
                workout.render_message(), disable_web_page_preview=True
            )  # , reply_markup=await WorkoutInline(workout).start()
        else:
            await message.reply(
                f"{WORKOUT_DONT_EXIST}: {group} №{order} {get_week_from_date(date)}"
            )
    else:
        await message.answer(ASK_TO_REGISTER)
        return


@dp.callback_query_handler(workout_callback.filter(), state=Workout.waiting_for_workout)
async def process_workout_inline(
    callback_query: CallbackQuery, callback_data: dict, state: FSMContext, *args, **kwargs
):
    await WorkoutInline.process_selection(callback_query, callback_data)


# Workout by day
@dp.message_handler(Text(KEYBOARD['date_workout']), state=Workout.waiting_for_workout)
async def process_date_workout(message: types.Message, state: FSMContext):
    if is_user_exists(config_manager.repository, message.from_user):
        await state.update_data(msg_id=message.message_id)
        await message.answer(CHOOSE_DATE, reply_markup=await DialogCalendar().start_calendar())
    else:
        await message.answer(ASK_TO_REGISTER)
        return


@dp.callback_query_handler(calendar_callback.filter(), state=Workout.waiting_for_workout)
async def process_dialog_calendar(
    callback_query: CallbackQuery, callback_data: dict, state: FSMContext, *args, **kwargs
):
    selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
    if selected:
        user_groups = await state.get_data()
        msg_id = user_groups.get('msg_id')
        await state.update_data(date=date)
        callback_query.message.message_id = msg_id
        await Workout.waiting_for_group.set()
        await waiting_for_group(callback_query.message, state)
