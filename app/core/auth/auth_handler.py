from sqlalchemy.orm import Session
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends
from pydantic import BaseModel
from typing import Union, Dict, Any

from app.hepler.enum import TokenType
from app.schema.token import TokenPayload
from app.core.security import pwd_context
from app.core.config import settings
from app.db.base_class import Base
from app.hepler.common import utc_now

ACCESS_TOKEN_EXPIRE = settings.ACCESS_TOKEN_EXPIRE
REFRESH_TOKEN_EXPIRE = settings.REFRESH_TOKEN_EXPIRE
SECRET_KEY = settings.TOKENS_SECRET_KEY
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


class TokenManager:

    def __init__(
        self,
        *,
        secret_key: str = settings.TOKENS_SECRET_KEY,
        algorithm: str = settings.SECURITY_ALGORITHM,
        access_token_expire: str = settings.ACCESS_TOKEN_EXPIRE,
        refresh_token_expire: str = settings.REFRESH_TOKEN_EXPIRE
    ) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire = access_token_expire
        self.refresh_token_expire = refresh_token_expire

    def signJWT(
        self,
        payload: Union[Base, Dict[str, Any], BaseModel],
        token_type: TokenType = TokenType.ACCESS,
        iat=None,
        exp=None,
    ):
        if iat is None:
            iat = utc_now()
        if exp is None:
            exp = iat + timedelta(seconds=self.access_token_expire)
        if isinstance(payload, Base):
            payload = payload.__dict__
        elif isinstance(payload, BaseModel):
            payload = payload.model_dump()
        elif isinstance(payload, dict):
            payload = payload
        payload.update({"iat": iat, "exp": exp, "type": token_type.value})
        data = TokenPayload(**payload)
        token = jwt.encode(data.model_dump(), self.secret_key, algorithm=self.algorithm)
        return token

    def decodeJWT(self, token: str):
        try:
            decode_token = jwt.decode(
                token, self.secret_key, algorithms=[self.algorithm]
            )
            return decode_token
        except:
            return {}
