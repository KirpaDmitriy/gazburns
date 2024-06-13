from sqlalchemy import Column, Integer, Sequence, String

from .connection import BaseTable


class User(BaseTable):
    __tablename__ = "user"

    id = Column(
        Integer,
        Sequence("auth_user_id_seq"),
        primary_key=True,
        nullable=False,
        index=True,
    )
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
