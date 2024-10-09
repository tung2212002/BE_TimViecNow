import jwt
from datetime import timedelta
from pydantic import BaseModel
from typing import Union, Dict, Any

from app.hepler.enum import TokenType
from app.schema.token import TokenPayload
from app.core.config import settings
from app.db.base_class import Base
from app.hepler.common import CommonHelper
from app.model import Account


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
            iat = CommonHelper.utc_now()
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

    def signJWTRefreshToken(
        self,
        payload: Union[Base, Dict[str, Any], BaseModel],
        token_type: TokenType = TokenType.REFRESH,
        iat=None,
        exp=None,
    ):
        return self.signJWT(
            payload,
            token_type,
            iat,
            exp
            or (CommonHelper.utc_now() + timedelta(seconds=self.refresh_token_expire)),
        )

    def decodeJWT(self, token: str):
        try:
            print("check token", token)
            decode_token = jwt.decode(
                token, self.secret_key, algorithms=[self.algorithm]
            )
            print("decode_token", decode_token)
            return decode_token
        except:
            return {}

    def create_payload(self, account: Account):
        return {
            "id": account.id,
            "role": account.role,
            "type_account": account.type_account,
        }


token_manager = TokenManager()
