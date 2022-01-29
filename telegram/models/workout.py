from datetime import date

from async_timeout import Any, Optional
from bot.texts import ROUNDS_LIST
from models.utils import get_decl
from pydantic import BaseModel, fields


class Group(BaseModel):
    name: str
    description: Optional[str] = fields.Field(default=None)


class Exercise(BaseModel):
    name: str
    description: Optional[str] = fields.Field(default=None)
    link: Optional[str] = fields.Field(default=None)


class Gymnastic(BaseModel):
    excercise: Exercise
    description: Optional[str] = fields.Field(default=None)
    value: int

    def render_message(self):
        if self.excercise.link:
            msg = f'*[{self.excercise.name}]({self.excercise.link})* – *{self.value}* '
        else:
            msg = f'*{self.excercise.name}* – *{self.value}* '

        if self.description:
            msg += f'– {self.description}\n'
        else:
            msg += '\n'

        return msg


class Set(BaseModel):
    description: Optional[str] = fields.Field(default=None)
    rounds_amount: int
    gymnastics: list[Gymnastic]

    def render_message(self, number) -> str:
        msg = f'{number} сет – *{self.rounds_amount}* {get_decl(self.rounds_amount, ROUNDS_LIST)}\n'
        for gym in self.gymnastics:
            msg += f'{gym.render_message()}'

        return msg


class Workout(BaseModel):
    description: Optional[str] = fields.Field(default=None)
    order: int
    week_start_date: date
    min_rm_percent: int
    max_rm_percent: int
    group: Group
    sets: list[Set]

    def render_message(self) -> str:  # TODO: generalize text
        msg = f'Группа: *{self.group.name}*\n'
        if self.description:
            msg += f'Описание: {self.description}\n'
        msg += f'Рабочий процент васа: *{self.min_rm_percent}\\-{self.max_rm_percent}%*\n\n'

        for i, set in enumerate(self.sets):
            msg += f'{set.render_message(i + 1)}\n'

        return msg
