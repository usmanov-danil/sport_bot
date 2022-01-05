from aiogram import types
from aiogram.dispatcher.filters import Command
from bot.handlers.keyboard import menu
from bot.loader import bot, config_manager, dp
from bot.texts import HELP_MESSAGE, WELCOME_MESSAGE
from services.user_managment import get_all_user_ids, register_new_user


@dp.message_handler(Command('start'))
async def process_start_command(message: types.Message):
    await register_new_user(config_manager.repository, message.from_user)
    await message.reply(WELCOME_MESSAGE, reply_markup=menu)


@dp.message_handler(Command('help'))
async def process_help_command(message: types.Message):
    await message.reply(HELP_MESSAGE)


@dp.message_handler(Command('all'))
async def notify_users(message: types.Message):
    if message.from_user.id in config_manager.admins:
        text = message.get_args()
        user_ids = await get_all_user_ids(config_manager.repository)
        for uid in user_ids:
            if not (uid in config_manager.admins):
                await bot.send_message(uid, text)
