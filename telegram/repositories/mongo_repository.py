from typing import Optional

from loguru import logger
from models.base import User
from pymongo.mongo_client import MongoClient
from repositories.abstract import UserRepository


class MongoUserRepository(UserRepository):
    def __init__(self, conn: MongoClient) -> None:
        self._conn = conn
        self._init_db()

    def _init_db(self) -> None:
        try:
            self.db = self._conn['bot_db']
            self.users = self.db['bot_user']
        except Exception as err:
            logger.error(err)

    def save_user_data(self, user: User) -> None:
        try:
            self.users.insert_one(
                {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'username': user.username,
                    'birth_date': False,
                    'activated': None,
                    'sex': None,
                    'groups': None,
                }
            )
        except Exception as err:
            logger.error(err)

    def get_all_user_ids(self) -> list[int]:
        try:
            if data_in_db := self.users.find():
                return [item.id for item in data_in_db]
            return []
        except Exception as err:
            logger.error(err)
            return []

    def get_user_data_by_id(self, id: int) -> Optional[User]:
        try:
            if data_in_db := self.users.find_one({'id': id}):
                return User.from_json(data_in_db)
            return None
        except Exception as err:
            logger.error(err)

    def save_personal_info(self, user: User) -> None:
        try:
            if self.get_user_data_by_id(user.id):
                self.users.find_one_and_update(
                    {
                        'id': user.id,
                    },
                    {
                        '$set': {
                            'birth_date': user.birth_date,
                            'activated': user.activated,
                            'sex': user.sex,
                            'groups': user.groups,
                        }
                    },
                )
        except Exception as err:
            logger.error(err)

    def get_personal_info(self, id: int) -> Optional[User]:
        data = self.get_user_data_by_id(id)
        if data.has_personal_data():
            return data
        return None
