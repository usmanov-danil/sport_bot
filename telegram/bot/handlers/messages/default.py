from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from bot.handlers.keyboards.keyboard import menu
from bot.loader import bot, config_manager, dp
from bot.texts import HELP_MESSAGE, MAIN_PAGE_TEXT, WELCOME_MESSAGE
from services.user_managment import get_all_user_ids, register_new_user


@dp.message_handler(Command('start'))
async def process_start_command(message: types.Message, state: FSMContext):
    await register_new_user(config_manager.repository, message.from_user)
    await message.reply(WELCOME_MESSAGE, reply_markup=menu)
    # await state.finish()


@dp.message_handler(Command('menu'), state='*')
async def process_menu_command(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(MAIN_PAGE_TEXT, reply_markup=menu)


@dp.message_handler(Command('help'), state='*')
async def process_help_command(message: types.Message, *args, **kwargs):
    await message.reply(HELP_MESSAGE)


@dp.message_handler(Command('all'))
async def notify_users(message: types.Message):
    if message.from_user.id in config_manager.admins:
        text = message.get_args()
        user_ids = await get_all_user_ids(config_manager.repository)
        for uid in user_ids:
            if not (uid in config_manager.admins):
                await bot.send_message(uid, text)
