from datetime import datetime
from typing import Optional

from app.constants import MAX_NAME_LEN, MIN_NAME_LEN
from pydantic import BaseModel, Extra, Field, PositiveInt


class CharityProjectBase(BaseModel):
    name: str = Field(
        ..., min_length=MIN_NAME_LEN, max_length=MAX_NAME_LEN
    )
    description: str = Field(..., min_length=MIN_NAME_LEN)
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):

    class Config(CharityProjectBase.Config):
        schema_extra = {
            'example': {
                'name': 'Пример благотворительного проекта :-)',
                'description': 'Описание демонстрационного проекта :-3',
                'full_amount': 50_000
            }
        }


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(
        None, min_length=MIN_NAME_LEN, max_length=MAX_NAME_LEN,
    )
    description: Optional[str] = Field(None, min_length=MIN_NAME_LEN)
    full_amount: Optional[PositiveInt]

    class Config(CharityProjectBase.Config):
        schema_extra = {
            'example': {
                'name': 'Смена названия :)',
                'description': 'Другое описание :3',
                'full_amount': 100_000
            }
        }


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True