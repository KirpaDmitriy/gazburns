from sqlalchemy import insert, select

from models import Case, general_case

from .connection import async_pg_session
from .tables import Case as CaseTable
from .tables import User


async def get_user(username: str) -> dict:
    async with async_pg_session() as session:
        selected_user = (
            await session.execute(
                select(User.username, User.hashed_password).where(
                    User.username == username
                )
            )
        ).one_or_none()

        if not selected_user:
            return {}

        return {
            "username": selected_user[0],
            "hashed_password": selected_user[1],
        }


async def save_case(**kwargs) -> None:
    async with async_pg_session() as session:
        await session.execute(insert(CaseTable).values(**kwargs))
        await session.commit()


async def add_image_to_case(case_id: str, images: list[str]) -> None:
    async with async_pg_session() as session:
        selected_case = (
            await session.execute(select(CaseTable).where(CaseTable.id == case_id))
        ).scalar()

        if selected_case:
            selected_case.images = images
            await session.commit()


async def get_case(case_id: str, username: str) -> dict:
    async with async_pg_session() as session:
        case = (
            await session.execute(
                select(CaseTable.id, CaseTable.images, CaseTable.meta_information).where(id=case_id, username=username)
            )
        ).one_or_none()
        if case:
            return {
                "id": case[0],
                "images": case[1],
                "meta_information": case[2],
            }
        return {}


async def get_cases() -> list[Case]:
    return [general_case, general_case, general_case]
