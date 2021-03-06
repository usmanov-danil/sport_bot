import datetime
import uuid
from typing import Optional

from bson.binary import Binary
from loguru import logger
from models.base import User
from models.workout import Workout
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
            self.workout = self.db['bot_training']
        except Exception as err:
            logger.error(err)

    def save_user_data(self, user: User) -> None:
        try:
            if not list(self.users.find({'telegram_id': user.id})):
                self.users.insert_one(
                    {
                        'id': Binary(uuid.uuid4().bytes, 3),
                        'telegram_id': user.id,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'username': user.username,
                        'birth_date': None,
                        'activated': False,
                        'sex': None,
                        'groups': [],
                    }
                )
        except Exception as err:
            logger.error('PIZDA')

    def get_all_user_ids(self) -> list[int]:
        try:
            if data_in_db := list(self.users.find()):
                return [item.telegram_id for item in data_in_db]
            return []
        except Exception as err:
            logger.error(err)
            return []

    def get_user_data_by_id(self, id: int) -> Optional[User]:
        try:
            data_in_db = list(
                self.users.aggregate(
                    [
                        {'$match': {'telegram_id': id}},
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
            )
            if data_in_db:
                return User.from_json(data_in_db[0])
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

    def get_workout(self, group: str, order: int, date: datetime.datetime) -> Optional[Workout]:
        try:
            data_in_db = list(
                self.workout.aggregate(
                    [
                        {
                            '$match': {
                                'week_start_date': date,
                                'order': order,
                            }
                        },
                        {
                            '$lookup': {
                                'from': 'bot_group',
                                'let': {'ids': '$groups_id'},
                                'pipeline': [
                                    {'$match': {'$expr': {'$in': ['$id', '$$ids']}}},
                                    {'$match': {'name': group}},
                                    {'$project': {'_id': 0, 'id': 0}},
                                ],
                                'as': 'group',
                            }
                        },
                        {'$match': {'group': {'$exists': True, '$not': {'$size': 0}}}},
                        {'$addFields': {'group': {'$arrayElemAt': ['$group', 0]}}},
                        {
                            '$lookup': {
                                'from': 'bot_set',
                                'let': {'ids': '$sets_id'},
                                'pipeline': [
                                    {'$match': {'$expr': {'$in': ['$id', '$$ids']}}},
                                    {
                                        '$lookup': {
                                            'from': 'bot_gymnastic',
                                            'let': {'gids': '$gymnastics_id'},
                                            'pipeline': [
                                                {'$match': {'$expr': {'$in': ['$id', '$$gids']}}},
                                                {
                                                    '$project': {
                                                        'id': 0,
                                                        '_id': 0,
                                                        'date_created': 0,
                                                    }
                                                },
                                                {
                                                    '$lookup': {
                                                        'from': 'bot_exercise',
                                                        'localField': 'exercise_id',
                                                        'foreignField': 'id',
                                                        'pipeline': [
                                                            {'$project': {'id': 0, '_id': 0}}
                                                        ],
                                                        'as': 'exercise',
                                                    }
                                                },
                                                {'$project': {'id': 0, '_id': 0, 'exercise_id': 0}},
                                                {
                                                    '$addFields': {
                                                        'exercise': {
                                                            '$arrayElemAt': ['$exercise', 0]
                                                        }
                                                    }
                                                },
                                            ],
                                            'as': 'gymnastics',
                                        }
                                    },
                                    {
                                        '$project': {
                                            'id': 0,
                                            '_id': 0,
                                            'date_created': 0,
                                            'gymnastics_id': 0,
                                        }
                                    },
                                ],
                                'as': 'sets',
                            }
                        },
                        {'$project': {'_id': 0, 'groups_id': 0, 'sets_id': 0, 'id': 0}},
                    ]
                )
            )
            if data_in_db:
                return Workout.parse_obj(data_in_db[0])
            return None
        except Exception as err:
            logger.error(err)

    def get_workout_count(self, group: str, date: datetime.datetime) -> Optional[int]:
        try:
            if data_in_db := list(
                self.workout.aggregate(
                    [
                        {
                            '$match': {
                                'week_start_date': date,
                            }
                        },
                        {
                            '$lookup': {
                                'from': 'bot_group',
                                'let': {'ids': '$groups_id'},
                                'pipeline': [
                                    {'$match': {'$expr': {'$in': ['$id', '$$ids']}}},
                                    {'$match': {'name': group}},
                                    {'$project': {'_id': 0, 'id': 0}},
                                ],
                                'as': 'group',
                            }
                        },
                        {'$match': {'group': {'$exists': True, '$not': {'$size': 0}}}},
                        {'$count': 'id'},
                    ]
                )
            ):
                count_dict = data_in_db[0]
                return count_dict.get('id')
            return 0
        except Exception as err:
            logger.error(err)
            return 0
