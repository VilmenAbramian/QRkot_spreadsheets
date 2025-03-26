from sqlalchemy import Column, Integer, ForeignKey, Text

from .foundbase import FoundBase


class Donation(FoundBase):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
