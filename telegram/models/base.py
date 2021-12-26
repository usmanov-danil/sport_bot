from typing import Optional, Tuple

from aiogram.types.user import User as UserRaw
from aiogram.types.user import base, fields


class User(UserRaw):
    weight: Optional[base.Float] = fields.Field(default=None)
    height: Optional[base.Integer] = fields.Field(default=None)
    years: Optional[base.Integer] = fields.Field(default=None)

    @staticmethod
    def from_tuple(user_tuple: Tuple[int, str, str, str, int, float, int]):
        return User(
            id=user_tuple[0],
            first_name=user_tuple[1],
            last_name=user_tuple[2],
            username=user_tuple[3],
            weight=user_tuple[4],
            height=user_tuple[5],
            years=user_tuple[6],
        )

    def set_personal_params(self, weight: float, height: int, years: int) -> None:
        self.weight = weight
        self.height = height
        self.years = years

    @classmethod
    def from_aiogram_user(cls, ai_user: UserRaw):
        # Create new b_obj
        user_obj = cls()
        # Copy all values of A to B
        # It does not have any problem since they have common template
        for key, value in ai_user.__dict__.items():
            user_obj.__dict__[key] = value
        return user_obj

    def has_personal_data(self) -> bool:
        return self.weight and self.height and self.years
