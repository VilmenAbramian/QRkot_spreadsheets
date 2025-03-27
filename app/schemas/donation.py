from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationBaseModel(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBaseModel):
    pass


class DonationGet(DonationBaseModel):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationGet):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
