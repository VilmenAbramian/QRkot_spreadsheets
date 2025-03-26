from sqlalchemy import Column, String, Text

from .foundbase import FoundBase
from app.constants import MAX_NAME_LEN


class CharityProject(FoundBase):
    name = Column(String(MAX_NAME_LEN), nullable=False)
    description = Column(Text, nullable=False)
