from aiogram import Dispatcher, types
from loguru import logger


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            types.BotCommand('start', 'Запустить бота'),
            types.BotCommand('help', 'Вывести справку'),
        ]
    )
    logger.debug('Default commands are setted')
