from fastapi import APIRouter

from app.api.api_v1.endpoint import auth, user

api_router = APIRouter(prefix="/v1/api")

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
