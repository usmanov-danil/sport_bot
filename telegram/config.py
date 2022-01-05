import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel
from pydantic.types import PyObject
from pymongo.mongo_client import MongoClient

PROJECT_PATH = Path(os.path.abspath(os.path.dirname(__file__)))
CONFIG_FILE_PATH = PROJECT_PATH / 'config.json'


class RepositoryConfig(BaseModel):
    repo: PyObject
    connection: str
    port: Optional[int]
    username: Optional[str]
    password: Optional[str]


class Config(BaseModel):
    token: str
    admins: list[str]
    repo: RepositoryConfig


class ConfigurationManager:
    def __init__(self) -> None:
        config_json = open(CONFIG_FILE_PATH).read()
        self._config = Config.parse_raw(config_json)
        self.environment = os.getenv('ENV', 'dev')
        self.admins = self._config.admins
        self.token = self._config.token

        _connection = MongoClient(
            self._config.repo.connection,
            self._config.repo.port,
            username=self._config.repo.username,
            password=self._config.repo.password,
        )
        self.repository = self._config.repo.repo(_connection)
