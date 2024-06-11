import os
import uuid
from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

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


SECRET_KEY = os.environ["JWT_SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$6M6D0QlV4o5n8c3gK5ZtAePfFqJeeX0yA1tN6zVowHdQrR7aW8p3G",  # Password is "secret"
    }
}


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Get user
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return user_dict


def authenticate_user(fake_users_db, username: str, password: str) -> dict | None:
    user = get_user(fake_users_db, username)
    if user and verify_password(password, user["hashed_password"]):
        return {
            "username": "johndoe",
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "hashed_password": "$2b$12$6M6D0QlV4o5n8c3gK5ZtAePfFqJeeX0yA1tN6zVowHdQrR7aW8p3G",
        }


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post("/token")
async def login_for_access_token(username: str, password: str):
    user = authenticate_user(fake_users_db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(authorization: str = Header(...)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise credentials_exception
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except (ValueError, JWTError):
        raise credentials_exception
    return username


@app.get("/cases", response_model=list[Case])
async def cases(current_user: str = Depends(get_current_user)):
    return [general_case, general_case, general_case]


@app.post("/generate", response_model=Case)
async def generate_image(
    params: GenerationParams, current_user: str = Depends(get_current_user)
):
    save_session(params)
    return general_case


@app.post("/add_text", response_model=Case)
async def add_text(params: TextParams, current_user: str = Depends(get_current_user)):
    return general_case


@app.get("/generate_text", response_model=GeneratedFormText)
async def generate_text(case_id: str, current_user: str = Depends(get_current_user)):
    return GeneratedFormText(title="Собака", subtitle="Улыбака")
