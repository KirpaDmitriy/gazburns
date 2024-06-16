import uuid
from enum import Enum

from pydantic import BaseModel, Field


class MyEnum(Enum):
    male = "male"
    female = "female"
    null = ""


class GenerationParams(BaseModel):
    ageTo: int | None = None
    ageFrom: int | None = None
    salaryFrom: float | None = None
    salaryTo: float | None = None
    product: str | None = None
    gender: MyEnum = MyEnum.null
    audience: str | None = None
    width: int
    height: int

    def to_dict(self) -> dict:
        return {
            "ageTo": self.ageTo,
            "ageFrom": self.ageFrom,
            "salaryFrom": self.salaryFrom,
            "salaryTo": self.salaryTo,
            "product": self.product,
            "gender": self.gender.value,
            "audience": self.audience,
            "width": self.width,
            "height": self.height,
        }


class TextParams(BaseModel):
    case_id: str
    picture_id: str
    title: str | None = None
    subtitle: str | None = None


class PictureInfo(BaseModel):
    id: str
    src: str = Field(..., description="URL файла изображения")
    title: str | None = None
    subtitle: str | None = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "src": self.src,
            "title": self.title,
            "subtitle": self.subtitle,
        }


class Case(BaseModel):
    id: str
    images: list[PictureInfo] = Field(
        ..., description="URL файлов изображений из истории генераций для данной сессии"
    )
    meta_information: GenerationParams = Field(
        ...,
        description="Базовые параметры генерации: описание кластера и продукта, размеры изображения",
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "images": self.images,
            "meta_information": self.meta_information,
        }


class GeneratedFormText(BaseModel):
    title: str
    subtitle: str


class User(BaseModel):
    username: str
    password: str


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
