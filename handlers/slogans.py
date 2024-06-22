from fastapi import APIRouter, Depends

from database import get_case
from models import GeneratedFormText, RegenParams
from src.access import get_current_user
from src.logger import app_logger
from src.text_generation import generate_product_logo

log = app_logger(__name__)

router = APIRouter()


@router.post("/slogans", response_model=GeneratedFormText)
async def slogans(params: RegenParams, current_user: str = Depends(get_current_user)):
    case_as_dict = await get_case(case_id=params.case_id, username=current_user)

    log.info(f"Found case in /slogans: {case_as_dict}")

    title, description = await generate_product_logo(
        case_as_dict["meta_information"]["product"]
    )

    return {"title": title, "subtitle": description}
