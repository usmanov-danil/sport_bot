from aiogram import Dispatcher, executor
from bot.handlers.commands import set_default_commands
from bot.handlers.notify import notify_admins
from bot.loader import dp
from bot.texts import SHUTDOWN_NOTIFICATION, STARTUP_NOTIFICATION
from loguru import logger


async def on_startup(dispatcher: Dispatcher):
    await set_default_commands(dispatcher)  # Set default commands
    await notify_admins(dispatcher, STARTUP_NOTIFICATION)  # Notify admins
    logger.info('Bot started')


async def on_shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    await notify_admins(dispatcher, SHUTDOWN_NOTIFICATION)  # Notify admins
    logger.info('Bot stopped')


def start_bot():
    try:
        executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
    except Exception as err:
        logger.critical(f'Bot failed to start: {err}')
