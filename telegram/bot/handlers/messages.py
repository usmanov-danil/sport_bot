from typing import Text

from aiogram import types
from aiogram.dispatcher.filters import Command, Text
from bot.handlers.keyboard import menu, workout
from bot.loader import dp
from bot.texts import HELP_MESSAGE, KEYBOARD, WELCOME_MESSAGE


@dp.message_handler(Command('start'))
async def process_start_command(message: types.Message):
    await message.reply(WELCOME_MESSAGE, reply_markup=menu)


@dp.message_handler(Command('help'))
async def process_start_command(message: types.Message):
    await message.reply(HELP_MESSAGE)


@dp.message_handler(Text(KEYBOARD['workout']))
async def process_start_command(message: types.Message):
    await message.reply('t', reply_markup=workout)


@dp.message_handler(Text(equals=KEYBOARD['weights']))
async def process_start_command(message: types.Message):
    await message.reply('Not implemented')


@dp.message_handler(Text(equals=KEYBOARD['profile']))
async def process_start_command(message: types.Message):
    await message.reply('Not implemented')


@dp.message_handler(Text(equals=KEYBOARD['attendance']))
async def process_start_command(message: types.Message):
    await message.reply('Not implemented')
