from loguru import logger
from models.base import User
from repositories.abstract import UserRepository


async def register_new_user(repo: UserRepository, user: User) -> None:
    repo.save_user_data(user)
    logger.info(f'User {user.username} has registered')


async def get_all_user_ids(repo: UserRepository) -> list[int]:
    return repo.get_all_user_ids()
