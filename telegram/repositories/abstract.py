import datetime
from abc import ABC, abstractmethod
from typing import Optional

from models.base import User
from models.workout import Workout


class UserRepository(ABC):
    @abstractmethod
    def save_user_data(self, user: User) -> None:
        raise NotImplemented

    @abstractmethod
    def get_all_user_ids(self) -> list[int]:
        raise NotImplemented

    @abstractmethod
    def get_user_data_by_id(self, id: int) -> Optional[User]:
        raise NotImplemented

    @abstractmethod
    def save_personal_info(self, user: User) -> None:
        raise NotImplemented

    @abstractmethod
    def get_personal_info(self, id: int) -> Optional[User]:
        raise NotImplemented

    @abstractmethod
    def get_workout(self, group: str, order: int, date: datetime.datetime) -> Optional[Workout]:
        raise NotImplemented
