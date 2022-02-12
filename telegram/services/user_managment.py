import datetime
from re import escape
from typing import Optional

from aiogram.types.user import User as UserRaw
from bot.handlers.messages.utils import get_start_week
from bot.texts import ASK_TO_REGISTER, DATA_IS_SAVED, UNKNOW, USER_DATA_TEMPLATE
from loguru import logger
from models.base import User
from models.workout import Workout
from repositories.abstract import UserRepository


async def register_new_user(repo: UserRepository, user: User) -> None:
    repo.save_user_data(user)


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
        birth_date = data.birth_date if data.birth_date else UNKNOW
        activated = data.activated if data.activated else UNKNOW
        sex = data.sex if data.sex else UNKNOW
        groups = data.groups if data.groups else UNKNOW
        return escape(
            USER_DATA_TEMPLATE.format(
                birth_date=birth_date, activated=activated, sex=sex, groups=groups
            )
        )
    return ASK_TO_REGISTER


async def get_user_groups(repo: UserRepository, user: UserRaw) -> Optional[list[str]]:
    return repo.get_user_data_by_id(user.id).groups


async def get_workout(
    repo: UserRepository, group: str, order: int, date: datetime.datetime = None
) -> Optional[Workout]:
    return repo.get_workout(group, order, get_start_week(date))


async def get_workout_count(repo: UserRepository, group: str, date: datetime.datetime) -> int:
    return repo.get_workout_count(group, get_start_week(date))
