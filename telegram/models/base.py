import typing
from typing import Optional, Tuple

from aiogram.types.user import User as UserRaw
from aiogram.types.user import base, fields
from pydantic.types import Json


class User(UserRaw):
    activated: Optional[base.Boolean] = fields.Field(default=False)
    birth_date: Optional[base.String] = fields.Field(default=None)
    sex: Optional[base.String] = fields.Field(default=None)
    groups: Optional[typing.List[base.String]] = fields.ListField(base=base.String, default=None)

    @staticmethod
    def from_tuple(user_tuple: Tuple[int, str, str, str, str, bool, str, list]):
        return User(
            id=user_tuple[0],
            first_name=user_tuple[1],
            last_name=user_tuple[2],
            username=user_tuple[3],
            birth_date=user_tuple[4],
            activated=user_tuple[5],
            sex=user_tuple[6],
            groups=user_tuple[7],
        )

    @staticmethod
    def from_json(user_json: Json):
        return User(
            id=user_json['telegram_id'],
            first_name=user_json['first_name'],
            last_name=user_json['last_name'],
            username=user_json['username'],
            birth_date=user_json['birth_date'].strftime('%m/%d/%Y'),
            activated=user_json['activated'],
            sex=user_json['sex'],
            groups=[item['name'] for item in user_json['groups']],
        )

    def set_personal_params(self, birth_data: str, activated: bool, sex: str, groups: list) -> None:
        self.birth_date = birth_data
        self.activated = activated
        self.sex = sex
        self.groups = groups

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
        return self.birth_date and self.sex and self.groups
