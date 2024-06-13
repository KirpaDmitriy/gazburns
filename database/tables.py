from sqlalchemy import Column, String

from .connection import BaseTable


class User(BaseTable):
    __tablename__ = "user"

    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
