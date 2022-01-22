import uuid
from typing import Optional

from bson.binary import Binary
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
            if not self.users.find({'telegram_id': user.id}):
                self.users.insert_one(
                    {
                        'telegram_id': user.id,
                    },
                    {
                        '$set': {
                            'id': Binary(uuid.uuid4().bytes, 3),
                            'telegram_id': user.id,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'username': user.username,
                            'birth_date': None,
                            'activated': False,
                            'sex': None,
                            'groups_id': [],
                        }
                    },
                )
                logger.info(f'User {user.username} has registered')
        except Exception as err:
            logger.error(err)

    def get_all_user_ids(self) -> list[int]:
        try:
            if data_in_db := self.users.find():
                return [item.telegram_id for item in data_in_db]
            return []
        except Exception as err:
            logger.error(err)
            return []

    def get_user_data_by_id(self, id: int) -> Optional[User]:
        try:
            data_in_db = self.users.aggregate(
                [
                    {'$match': {'telegram_id': 129931780}},
                    {
                        '$lookup': {
                            'from': 'bot_group',
                            'let': {'ids': '$groups_id'},
                            'pipeline': [
                                {'$match': {'$expr': {'$in': ['$id', '$$ids']}}},
                                {'$project': {'name': 1, '_id': 0}},
                            ],
                            'as': 'groups',
                        }
                    },
                    {'$project': {"groups_id": 0}},
                ]
            )
            if data_in_db:
                return User.from_json(list(data_in_db)[0])
            return None
        except Exception as err:
            logger.error(err)

    def save_personal_info(self, user: User) -> None:
        try:
            if self.get_user_data_by_id(user.id):
                self.users.find_one_and_update(
                    {
                        'telegram_id': user.id,
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
