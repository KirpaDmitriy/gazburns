import uuid

from pydantic import BaseModel, Field


class GenerationParams(BaseModel):
    audience: str | None = None
    product: str | None = None
    width: int
    height: int


class TextParams(BaseModel):
    case_id: str
    title: str | None = None
    subtitle: str | None = None


class PictureInfo(BaseModel):
    id: str
    src: str = Field(..., description="URL файла изображения")
    title: str | None = None
    subtitle: str | None = None


class Case(BaseModel):
    id: str
    images: list[PictureInfo] = Field(
        ..., description="URL файлов изображений из истории генераций для данной сессии"
    )
    meta_information: GenerationParams


class GeneratedFormText(BaseModel):
    title: str
    subtitle: str


MEGA_URL = "https://steamuserimages-a.akamaihd.net/ugc/862857581989807965/89518896478AB5FC4C81035678DB2B441ACE107A/?imw=512&imh=384&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=true"
general_case = Case(
    id=str(uuid.uuid4()),
    images=[
        {"id": "0-1", "src": MEGA_URL},
        {"id": "0-1", "src": MEGA_URL},
        {"id": "0-1", "src": MEGA_URL},
    ],
    meta_information={
        "width": 100,
        "height": 100,
    },
)
