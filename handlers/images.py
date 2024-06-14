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
    case_as_dict = case.to_dict()
    case_as_dict["images"] = [image.to_dict() for image in case_as_dict["images"]]
    case_as_dict["meta_information"] = case_as_dict["meta_information"].to_dict()
    case_as_dict["username"] = current_user
    await save_case(**case_as_dict)
    return case


@router.post("/add_text", response_model=Case)
async def add_text(params: TextParams, current_user: str = Depends(get_current_user)):
    return general_case
