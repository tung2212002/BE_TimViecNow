from fastapi import APIRouter

from app.api.api_v1.endpoint import (
    user_auth,
    user,
    business_auth,
    business,
    business_admin,
    location,
    position,
    category,
    field,
    verify,
    business_campaign,
    business_company,
    business_job,
)

api_router = APIRouter(prefix="/v1/api")

api_router.include_router(user_auth.router, prefix="/user", tags=["user_auth"])
api_router.include_router(user.router, prefix="/user/users", tags=["user"])
api_router.include_router(verify.router, prefix="/verify", tags=["verify"])
api_router.include_router(location.router, prefix="/location", tags=["location"])
api_router.include_router(position.router, prefix="/position", tags=["position"])
api_router.include_router(category.router, prefix="/category", tags=["category"])
api_router.include_router(field.router, prefix="/field", tags=["field"])

api_router.include_router(
    business_company.router, prefix="/business/company", tags=["company"]
)
api_router.include_router(business_job.router, prefix="/business/job", tags=["job"])
api_router.include_router(
    business_campaign.router, prefix="/business/campaign", tags=["campaign"]
)
api_router.include_router(business_admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(business.router, prefix="/business", tags=["business"])
api_router.include_router(
    business_auth.router, prefix="/business", tags=["business_auth"]
)
