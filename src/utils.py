import os
import uuid

from models import Case, GenerationParams
from src.images_generation import generate_image


async def extract_case(params: GenerationParams) -> Case:
    file_id = str(uuid.uuid4())
    filename = f"picture_{file_id}"
    await generate_image(params.audience, params.product, filename=filename)
    return Case(
        id=str(uuid.uuid4()),
        images=[
            {
                "id": file_id,
                "src": f"{os.environ['APP_HOST']}/{os.environ['IMAGES_PATH']}/{filename}.png",
            },
        ],
        meta_information=params,
    )
