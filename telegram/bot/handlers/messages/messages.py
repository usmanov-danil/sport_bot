from typing import Text

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from bot.handlers.keyboard import menu
from bot.loader import dp
from bot.texts import KEYBOARD, MAIN_PAGE_TEXT


# Navigation
@dp.message_handler(Text(equals=KEYBOARD['back']), state='*')
async def process_back_command(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(MAIN_PAGE_TEXT, reply_markup=menu)


# Weights page
@dp.message_handler(Text(equals=KEYBOARD['weights']))
async def process_weights_command(message: types.Message):
    await message.reply('Not implemented')
