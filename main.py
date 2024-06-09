import uuid

from fastapi import FastAPI

from database import save_session
from models import Case, GeneratedFormText, GenerationParams, TextParams

app = FastAPI()


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


@app.get("/cases", response_model=list[Case])
async def cases():
    return [general_case, general_case, general_case]


@app.post("/generate", response_model=Case)
async def generate_image(params: GenerationParams):
    save_session(params)
    return general_case


@app.post("/add_text", response_model=Case)
async def add_text(params: TextParams):
    return general_case


@app.get("/generate_text", response_model=GeneratedFormText)
async def generate_text(case_id: str):
    return GeneratedFormText(title="Собака", subtitle="Улыбака")
