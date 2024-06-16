import os

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from src.access import get_current_user

router = APIRouter()


@router.get("/files/{file_path:path}")
async def read_file(file_path: str):  # , current_user: str = Depends(get_current_user)):
    file_location = f"{os.environ['PICTURES_FOLDER']}/{file_path}"
    if os.path.exists(file_location):
        return FileResponse(file_location)
    else:
        return {"error": "File not found"}
