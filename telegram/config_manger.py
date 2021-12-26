import sqlite3
from importlib import import_module

from repositories.sqlite_repository import SqliteUserRepository

path_to_db = 'bot.db'
connection = sqlite3.connect(path_to_db)
sqlite_repo: SqliteUserRepository = import_module(
    'repositories.sqlite_repository'
).SqliteUserRepository(connection)
