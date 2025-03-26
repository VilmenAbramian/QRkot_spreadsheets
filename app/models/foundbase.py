from datetime import datetime

from sqlalchemy import (
    Boolean, CheckConstraint, Column, DateTime, Integer
)

from app.core.db import Base


class FoundBase(Base):
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, nullable=False, default=datetime.now)
    close_date = Column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint(
            'full_amount >= 0',
            name='full_amount is positive'
        ),
        CheckConstraint(
            '0 <= invested_amount <= full_amount',
            name='check_invested_between_0_and_full_amount'
        )
    )

    __abstract__ = True
