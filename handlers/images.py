import os
import uuid
from io import BytesIO

import httpx
from fastapi import APIRouter, Depends
from PIL import Image

from database import add_image_to_case, get_case, save_case
from models import Case, GenerationParams, TextParams
from src.access import get_current_user
from src.images_generation import add_text_to_image
from src.logger import app_logger
from src.utils import extract_case

log = app_logger(__name__)

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
    log.info(f"Case as dict: {case_as_dict}")
    try:
        await save_case(**case_as_dict)
    except Exception as exep:
        log.error(f"Saving case in /generate_image died: {exep}")
    return case


@router.post("/add_text", response_model=Case)
async def add_text(params: TextParams, current_user: str = Depends(get_current_user)):
    case_as_dict = await get_case(case_id=params.case_id, username=current_user)

    log.info(f"Found case in /add_text: {case_as_dict}")
    image_url = case_as_dict["images"][-1]["src"]
    async with httpx.AsyncClient() as client:
        response = await client.get(image_url)
        image = Image.open(BytesIO(response.content))

    file_id = str(uuid.uuid4())
    await add_text_to_image(image, params.title, file_id)

    case_as_dict["images"].append(
        {
            "id": file_id,
            "src": f"{os.environ['FS_HOST']}/{file_id}_text.png",
        }
    )
    log.info(f"Case as dict: {case_as_dict}")

    try:
        await add_image_to_case(
            case_id=case_as_dict["id"], images=case_as_dict["images"]
        )
    except Exception as exep:
        log.error(f"Saving case in /add_text died: {exep}")

    return case_as_dict
