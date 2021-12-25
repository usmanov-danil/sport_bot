from abc import ABC, abstractmethod

from models.base import User


class UserRepository(ABC):
    @abstractmethod
    def save_user_data(self, user: User) -> None:
        raise NotImplemented

    @abstractmethod
    def get_all_users(self) -> list[User]:
        raise NotImplemented

    @abstractmethod
    def get_all_user_ids(self) -> list[int]:
        raise NotImplemented
