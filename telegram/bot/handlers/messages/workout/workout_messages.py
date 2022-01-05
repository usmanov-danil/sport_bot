from typing import Text

from aiogram import types
from aiogram.dispatcher.filters import Text
from bot.handlers.keyboard import workout
from bot.loader import dp
from bot.texts import KEYBOARD, WORKOUT_MAIN_TEXT


# Workout page
@dp.message_handler(Text(KEYBOARD['workout']))
async def process_start_command(message: types.Message):
    await message.reply(WORKOUT_MAIN_TEXT, reply_markup=workout)


@dp.message_handler(Text(KEYBOARD['first_workout']))
async def process_start_command(message: types.Message):
    await message.answer('1')


@dp.message_handler(Text(KEYBOARD['second_workout']))
async def process_start_command(message: types.Message):
    await message.answer('2')


@dp.message_handler(Text(KEYBOARD['third_workout']))
async def process_start_command(message: types.Message):
    await message.answer('3')
