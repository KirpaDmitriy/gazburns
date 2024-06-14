from sqlalchemy import JSON, Column, Integer, Sequence, String

from .connection import BaseTable


class User(BaseTable):
    __tablename__ = "user"

    id = Column(
        Integer,
        Sequence("user_id_seq"),
        primary_key=True,
        nullable=False,
        index=True,
    )
    username = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )
    hashed_password = Column(
        String,
        nullable=False,
    )


class Case(BaseTable):
    __tablename__ = "case"

    id = Column(
        String,
        primary_key=True,
        nullable=False,
        index=True,
    )
    username = Column(
        String,
        nullable=False,
        index=True,
    )
    images = Column(JSON)
    meta_information = Column(JSON)
