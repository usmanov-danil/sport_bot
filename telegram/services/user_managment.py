from re import escape

from aiogram.types.user import User as UserRaw
from bot.texts import ASK_TO_REGISTER, DATA_IS_SAVED, UNKNOW, USER_DATA_TEMPLATE
from loguru import logger
from models.base import User
from repositories.abstract import UserRepository


async def register_new_user(repo: UserRepository, user: User) -> None:
    repo.save_user_data(user)
    logger.info(f'User {user.username} has registered')


async def get_all_user_ids(repo: UserRepository) -> list[int]:
    return repo.get_all_user_ids()


def is_user_exists(repo: UserRepository, user: UserRaw) -> bool:
    return not (repo.get_user_data_by_id(user.id) is None)


def is_personal_data_exists(repo: UserRepository, user: UserRaw) -> bool:
    return not (repo.get_personal_info(user.id) is None)


async def save_personal_data(repo: UserRepository, user: UserRaw) -> str:
    if is_user_exists(repo, user):
        repo.save_personal_info(user)
        logger.info(f'User {user.username} has saved his personal info')
        return DATA_IS_SAVED
    return ASK_TO_REGISTER


async def get_user_data(repo: UserRepository, user: User) -> str:
    if data := repo.get_user_data_by_id(user.id):
        weight = data.weight if data.weight else UNKNOW
        height = data.height if data.height else UNKNOW
        year = data.years if data.years else UNKNOW
        return escape(USER_DATA_TEMPLATE.format(weight=weight, height=height, year=year))
    return ASK_TO_REGISTER