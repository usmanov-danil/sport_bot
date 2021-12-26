from models.base import User
from repositories.abstract import UserRepository


class FakeUserRepository(UserRepository):
    def save_user_data(self, user: User) -> None:
        pass
