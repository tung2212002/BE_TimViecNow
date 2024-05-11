from sqlalchemy.orm import Session
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends
from typing import Union, Dict, Any

from app.hepler.enum import TokenType
from app.schema.token import TokenPayload
from app.core.security import pwd_context
from app.core.config import settings
from app.db.base_class import Base
from pydantic import BaseModel


ACCESS_TOKEN_EXPIRE = settings.ACCESS_TOKEN_EXPIRE_SECONDS
REFRESH_TOKEN_EXPIRE = settings.REFRESH_TOKEN_EXPIRE_SECONDS
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.SECURITY_ALGORITHM


def signJWT(payload: Union[Base, Dict[str, Any], BaseModel]):
    iat = datetime.now(timezone.utc)
    exp = iat + timedelta(seconds=ACCESS_TOKEN_EXPIRE)
    if isinstance(payload, Base):
        payload = payload.__dict__
        payload.update({"iat": iat, "exp": exp, "type": TokenType.ACCESS.value})
    elif isinstance(payload, BaseModel):
        payload = payload.model_dump()
        payload.update({"iat": iat, "exp": exp, "type": TokenType.ACCESS.value})
    data = TokenPayload(**payload)
    access_token = jwt.encode(data.model_dump(), SECRET_KEY, algorithm=ALGORITHM)
    return access_token


def signJWTRefreshToken(payload: Union[Base, Dict[str, Any], BaseModel]):
    iat = datetime.now(timezone.utc)
    exp = iat + timedelta(seconds=REFRESH_TOKEN_EXPIRE)
    if isinstance(payload, Base):
        payload = payload.__dict__
        payload.update({"iat": iat, "exp": exp, "type": TokenType.REFRESH.value})
    elif isinstance(payload, BaseModel):
        payload = payload.model_dump()
        payload.update({"iat": iat, "exp": exp, "type": TokenType.REFRESH.value})
    data = TokenPayload(**payload)
    refresh_token = jwt.encode(data.model_dump(), SECRET_KEY, algorithm=ALGORITHM)
    return refresh_token


def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decode_token
    except:
        return {}
