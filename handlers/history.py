from fastapi import APIRouter, Depends

from database import get_cases
from models import Case
from src.access import get_current_user
from src.logger import app_logger

log = app_logger(__name__)

router = APIRouter()


@router.get("/cases", response_model=list[Case])
async def cases(current_user: str = Depends(get_current_user)):
    return await get_cases(username=current_user)
