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
    segment: list[str]

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
            "segment": self.segment,
        }


class TextParams(BaseModel):
    case_id: str
    picture_id: str
    title: str | None = None
    subtitle: str | None = None


class RegenParams(BaseModel):
    case_id: str


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
