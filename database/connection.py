import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from yarl import URL

from src.logger import app_logger

log = app_logger(__name__)

async_pg_session = sessionmaker(
    create_async_engine(
        str(
            URL.build(
                scheme="postgresql+asyncpg",
                user=os.environ["DATABASE_USER"],
                password=os.environ["DATABASE_PASSWORD"],
                host=os.environ["DATABASE_HOST"],
                port=int(os.environ["DATABASE_PORT"] or 5432),
                path=f"/{os.environ['DATABASE_NAME']}",
            )
        ),
        echo=True,
    ),
    class_=AsyncSession,
    expire_on_commit=False,
)

BaseTable = declarative_base()
