from contextlib import closing
from sqlite3 import Connection
from typing import Optional, Tuple

from loguru import logger
from models.base import User
from repositories.abstract import UserRepository


class SqliteUserRepository(UserRepository):
    def __init__(self, conn: Connection) -> None:
        self._conn = conn
        self._init_db()

    def _init_db(self) -> None:
        try:
            with closing(self._conn.cursor()) as cursor:
                query = """CREATE TABLE IF NOT EXISTS users
                        (id INT UNIQUE,
                        fisrt_name VARCHAR(32),
                        last_name VARCHAR(32),
                        username VARCHAR(32),
                        weight FLOAT,
                        height FLOAT,
                        years INT)"""

                cursor.execute(query)
                self._conn.commit()
        except Exception as err:
            logger.error(err)

    def save_user_data(self, user: User) -> None:
        try:
            with closing(self._conn.cursor()) as cursor:
                query = f"""INSERT OR REPLACE INTO users (id, fisrt_name, last_name, username)
                        VALUES ({user.id}, '{user.first_name}', '{user.last_name}', '{user.username}')"""
                cursor.execute(query)
                self._conn.commit()
        except Exception as err:
            logger.error(err)

    def get_all_users(self) -> list[User]:
        try:
            with closing(self._conn.cursor()) as cursor:
                query = """SELECT * FROM users;"""
                cursor.execute(query)
                if data_in_db := cursor.fetchall():
                    print(*data_in_db)
                    return [User.from_tuple(item) for item in data_in_db if len(item) == 7]
            return []
        except Exception as err:
            logger.error(err)
            return []

    def get_all_user_ids(self) -> list[int]:
        users = self.get_all_users()
        return [item.id for item in users]
