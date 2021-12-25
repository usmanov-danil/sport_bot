from aiogram import Dispatcher
from bot.config import ADMINS
from loguru import logger


async def on_startup_notify(dp: Dispatcher, msg: str):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, msg)
        except Exception as err:
            logger.exception(err)
