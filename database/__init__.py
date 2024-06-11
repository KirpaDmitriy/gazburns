from models import Case, general_case


async def save_case(*args, **kwargs) -> None: ...


async def get_user(db, username: str):
    return {
        "username": "johndoe",
        "hashed_password": "$2b$12$k6PEkL2pEY5wIw1SRHP6IuAECTFrjMAs1dx4aG9Xs2IvcsCk4HQXi",
    }


async def get_cases() -> list[Case]:
    return [general_case, general_case, general_case]
