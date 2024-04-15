from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.auth.auth_handler import decodeJWT


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=401, detail="Invalid authentication scheme."
                )
            payload = self.verify_jwt(credentials.credentials)
            if not payload:
                raise HTTPException(
                    status_code=401, detail="Invalid token or expired token."
                )
            return {"token": credentials.credentials, "payload": payload}
        else:
            raise HTTPException(status_code=403, detail="Forbidden")

    def verify_jwt(self, jwtoken: str) -> bool:
        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        return payload
