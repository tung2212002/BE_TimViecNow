from sqlalchemy.orm import Session
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends

from app.core import constant
from app import crud, model, schema
from app.core.security import pwd_context
from app.core.config import settings

ACCESS_TOKEN_EXPIRE = settings.ACCESS_TOKEN_EXPIRE_SECONDS
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.SECURITY_ALGORITHM


def signJWT(payload: dict):
    iat = datetime.utcnow()
    exp = iat + timedelta(seconds=ACCESS_TOKEN_EXPIRE)
    payload.update({"iat": iat, "exp": exp})
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return access_token


def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decode_token
    except:
        return {}
