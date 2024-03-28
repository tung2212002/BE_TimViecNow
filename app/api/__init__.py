from fastapi import APIRouter

from app.api.api_v1.endpoint import user_auth, user, business_auth, business, admin

api_router = APIRouter(prefix="/v1/api")

api_router.include_router(user_auth.router, prefix="/user", tags=["user_auth"])
api_router.include_router(user.router, prefix="/user/users", tags=["user"])

api_router.include_router(
    business_auth.router, prefix="/business", tags=["business_auth"]
)
api_router.include_router(business.router, prefix="/business", tags=["business"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
