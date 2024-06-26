import os
import random
import uuid

from models import Case, GenerationParams
from src.images_generation import generate_image
from src.logger import app_logger

log = app_logger(__name__)


async def extract_case(params: GenerationParams) -> Case:
    file_id = str(uuid.uuid4())
    filename = f"picture_{file_id}"
    await generate_image(
        random.choice(params.segment),
        product=params.product,
        filename=filename,
        banner_size=(params.height, params.width),
    )
    return Case(
        id=str(uuid.uuid4()),
        images=[
            {
                "id": file_id,
                "src": f"{os.environ['FS_HOST']}/{filename}.png",
                "object": f"{os.environ['FS_HOST']}/{filename}_object.png",
            },
        ],
        meta_information=params,
    )
