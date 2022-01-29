from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from config import ConfigurationManager

config_manager = ConfigurationManager()

bot = Bot(token=config_manager.token, parse_mode=types.ParseMode.MARKDOWN_V2)
dp = Dispatcher(bot, storage=config_manager.mongo_storage)
dp.middleware.setup(LoggingMiddleware())
