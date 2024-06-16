from datetime import timedelta

from fastapi import APIRouter, HTTPException, status

from models import User
from src.access import (ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user,
                        create_access_token, register_user)
from src.logger import app_logger

log = app_logger(__name__)

router = APIRouter()


@router.post("/token")
async def login_for_access_token(auth_user: User):
    user = await authenticate_user(auth_user.username, auth_user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register")
async def register(auth_user: User):
    try:
        await register_user(auth_user.username, auth_user.password)
        message = {"ok": 1}
    except Exception:
        message = {"ok": 0, "error": "Login is not unique"}
    return message
