from typing import Text

from aiogram import types
from aiogram.dispatcher.filters import Text
from bot.handlers.keyboard import menu, workout
from bot.loader import dp
from bot.texts import KEYBOARD, MAIN_PAGE_TEXT, WORKOUT_MAIN_TEXT


# Navigation
@dp.message_handler(Text(equals=KEYBOARD['back']))
async def process_start_command(message: types.Message):
    await message.answer(MAIN_PAGE_TEXT, reply_markup=menu)


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


# Weights page
@dp.message_handler(Text(equals=KEYBOARD['weights']))
async def process_start_command(message: types.Message):
    await message.reply('Not implemented')


# Profile page
@dp.message_handler(Text(equals=KEYBOARD['profile']))
async def process_start_command(message: types.Message):
    await message.reply('Not implemented')


# Attendance page
@dp.message_handler(Text(equals=KEYBOARD['attendance']))
async def process_start_command(message: types.Message):
    await message.reply('Not implemented')
