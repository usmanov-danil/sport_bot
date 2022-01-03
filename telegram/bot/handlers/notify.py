from aiogram import Dispatcher
from config import ConfigurationManager
from loguru import logger


async def on_startup_notify(dp: Dispatcher, msg: str):
    for admin in ConfigurationManager().admins:
        try:
            await dp.bot.send_message(admin, msg)
        except Exception as err:
            logger.exception(err)
