from datetime import date

from async_timeout import Any, Optional
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


class Set(BaseModel):
    description: Optional[str] = fields.Field(default=None)
    rounds_amount: int
    gymnastics: list[Gymnastic]


class Workout(BaseModel):
    description: Optional[str] = fields.Field(default=None)
    order: int
    week_start_date: date
    min_rm_percent: int
    max_rm_percent: int
    group: Group
    sets: list[Set]
