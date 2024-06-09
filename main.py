import uuid

from fastapi import FastAPI

from models import (GenerationParams, GenerationResult, GenerationSessionId,
                    TextParams)

app = FastAPI()


@app.post("/generate", response_model=GenerationSessionId)
async def generate(params: GenerationParams):
    return GenerationSessionId(session_id=str(uuid.uuid4()))


@app.post("/add_text", response_model=GenerationResult)
async def add_text(params: TextParams):
    return GenerationResult(
        id=str(uuid.uuid4()),
        title="Собака",
        description="Улыбака",
        data={
            "id": str(uuid.uuid4()),
            "src": "https://steamuserimages-a.akamaihd.net/ugc/862857581989807965/89518896478AB5FC4C81035678DB2B441ACE107A/?imw=512&imh=384&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=true",
        },
    )
