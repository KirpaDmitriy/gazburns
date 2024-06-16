from fastapi import APIRouter, Depends

from models import GeneratedFormText
from src.access import get_current_user
from src.logger import app_logger

log = app_logger(__name__)

router = APIRouter()


@router.get("/generate_text", response_model=GeneratedFormText)
async def generate_text(case_id: str, current_user: str = Depends(get_current_user)):
    return GeneratedFormText(title="Собака", subtitle="Улыбака")
