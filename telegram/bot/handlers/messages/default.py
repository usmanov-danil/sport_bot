from aiogram import types
from aiogram.dispatcher.filters import Command
from bot.config import ADMINS
from bot.handlers.keyboard import menu
from bot.loader import bot, dp
from bot.texts import HELP_MESSAGE, WELCOME_MESSAGE
from config_manger import sqlite_repo
from services.user_managment import get_all_user_ids, register_new_user


@dp.message_handler(Command('start'))
async def process_start_command(message: types.Message):
    await register_new_user(sqlite_repo, message.from_user)
    await message.reply(WELCOME_MESSAGE, reply_markup=menu)


@dp.message_handler(Command('help'))
async def process_help_command(message: types.Message):
    await message.reply(HELP_MESSAGE)


@dp.message_handler(Command('all'))
async def notify_users(message: types.Message):
    text = message.get_args()
    user_ids = await get_all_user_ids(sqlite_repo)
    print(text)
    print(user_ids)
    for uid in user_ids:
        if uid not in ADMINS:
            await bot.send_message(uid, text)
