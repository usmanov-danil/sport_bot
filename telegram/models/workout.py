from datetime import date

from async_timeout import Optional
from bot.texts import ROUNDS_LIST
from models.utils import get_decl
from pydantic import BaseModel, fields


def to_esc(line: str) -> str:
    line = str(line)
    return line.translate(
        str.maketrans(
            {
                "-": r"\-",
                "]": r"\]",
                "\\": r"\\",
                "^": r"\^",
                "$": r"\$",
                "+": r"\+",
                "*": r"\*",
                ".": r"\.",
            }
        )
    )


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
    value: str

    def render_message(self):
        if self.excercise.link:
            msg = f' \-*[{to_esc(self.excercise.name)}]({self.excercise.link})*: *{to_esc(self.value)}* '
        else:
            msg = f' \-*{to_esc(self.excercise.name)}*: *{to_esc(self.value)}* '

        if self.description:
            msg += f'({to_esc(self.description)})'

        msg += '\n'
        return msg


class Set(BaseModel):
    description: Optional[str] = fields.Field(default=None)
    rounds_amount: int
    gymnastics: list[Gymnastic]

    def render_message(self, number) -> str:
        msg = (
            f'*Set {number}*/ *{self.rounds_amount}* {get_decl(self.rounds_amount, ROUNDS_LIST)} '
            f'{to_esc(self.description)}\n'
        )
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
        msg = f'Тренировка № {self.order}\n'
        msg += f'Группа: *{to_esc(self.group.name)}*\n'
        if self.description:
            msg += f'Описание: {to_esc(self.description)}\n'
        msg += f'Рабочий процент веса: *{self.min_rm_percent}\-{self.max_rm_percent}%*\n\n'

        for i, set in enumerate(self.sets):
            msg += f'{set.render_message(i + 1)}\n'

        return msg

    def get_gymnastics(self) -> list[Exercise]:
        gymnastics = []
        for set in self.sets:
            for gym in set.gymnastics:
                gymnastics.append(gym)

        return gymnastics
