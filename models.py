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
