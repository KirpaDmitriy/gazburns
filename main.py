from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from handlers.access import router as access_router
from handlers.files_server import router as files_router
from handlers.history import router as history_router
from handlers.images import router as images_router
from handlers.slogans import router as slogans_router
from src.logger import app_logger

log = app_logger(__name__)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(access_router)
app.include_router(history_router)
app.include_router(images_router)
app.include_router(slogans_router)
app.include_router(files_router)
