from pydantic import BaseModel, Field


class GenerationParams(BaseModel):
    audience: str | None = None
    product: str | None = None


class GenerationSessionId(BaseModel):
    session_id: str


class TextParams(BaseModel):
    session_id: str
    title: str | None = None
    subtitle: str | None = None


class PictureInfo(BaseModel):
    id: str
    src: str = Field(..., description="URL файла изображения")


class GenerationResult(BaseModel):
    id: str
    title: str | None
    description: str | None
    data: PictureInfo = Field(..., description="Данные об изображении")
