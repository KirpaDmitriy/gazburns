from models import Case, GenerationParams, general_case
from src.images_generation import generate_image


def extract_case(params: GenerationParams) -> Case:
    await generate_image(params.audience, params.product)
    return general_case
