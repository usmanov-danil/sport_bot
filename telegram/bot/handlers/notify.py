from aiogram import Dispatcher
from config import ConfigurationManager
from loguru import logger


async def notify_admins(dp: Dispatcher, msg: str):
    for admin in ConfigurationManager().admins:
        try:
            await dp.bot.send_message(admin, msg)
        except Exception as err:
            logger.exception(err)


async def notify_trainers(dp: Dispatcher, msg: str):
    for trainer in ConfigurationManager().trainers:
        try:
            await dp.bot.send_message(trainer, msg)
        except Exception as err:
            logger.exception(err)
