from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.auth.jwt.auth_handler import token_manager
from app.common.exception import CustomException
from fastapi import status


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise CustomException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    msg="Invalid authentication scheme.",
                )

            payload = self.verify_jwt(credentials.credentials)
            if not payload:
                raise CustomException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    msg="Invalid token or expired token.",
                )

            return {"token": credentials.credentials, "payload": payload}
        else:
            raise CustomException(
                status_code=status.HTTP_403_FORBIDDEN,
                msg="Forbidden",
            )

    def verify_jwt(self, jwtoken: str) -> bool:
        try:
            payload = token_manager.decodeJWT(jwtoken)
        except:
            payload = None
        return payload
