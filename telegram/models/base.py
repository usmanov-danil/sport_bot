from typing import Optional, Tuple

from aiogram.types.user import User as UserRaw


class User(UserRaw):
    height: Optional[float]
    weight: Optional[float]
    years: Optional[int]

    @staticmethod
    def from_tuple(user_tuple: Tuple[int, str, str, str, float, float, int]):
        return User(
            id=user_tuple[0],
            first_name=user_tuple[1],
            last_name=user_tuple[2],
            username=user_tuple[3],
            height=user_tuple[4],
            weight=user_tuple[5],
            years=user_tuple[6],
        )
