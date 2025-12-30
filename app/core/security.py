import os
from datetime import datetime, timedelta
from pathlib import Path

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException
from passlib.context import CryptContext

# env_path = Path(__file__).resolve().parents[2] / ".env"
# load_dotenv(dotenv_path=env_path)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: int):
    payload = {"sub": str(user_id), "exp": datetime.utcnow() + timedelta(minutes=30)}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="invalid token")
