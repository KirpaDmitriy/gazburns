from fastapi import APIRouter, Depends

from database import save_case
from models import Case, GenerationParams, TextParams, general_case
from src.access import get_current_user
from src.utils import extract_case

router = APIRouter()


@router.post("/generate", response_model=Case)
async def generate_image(
    params: GenerationParams, current_user: str = Depends(get_current_user)
):
    case = await extract_case(params)
    await save_case(case)
    return case


@router.post("/add_text", response_model=Case)
async def add_text(params: TextParams, current_user: str = Depends(get_current_user)):
    return general_case
