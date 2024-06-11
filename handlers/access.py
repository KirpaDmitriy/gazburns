from datetime import timedelta

from fastapi import APIRouter, HTTPException, status

from src.access import (ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user,
                        create_access_token)

router = APIRouter()


@router.post("/token")
async def login_for_access_token(username: str, password: str):
    user = await authenticate_user({}, username, password)
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
