from fastapi import APIRouter, Depends, Body, Path, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from redis.asyncio import Redis
from typing import List

from app.db.base import get_db
from app.storage.redis import get_redis
from app.core.auth.user_manager_service import user_manager_service
from app.core.cv_applications.cv_applications_service import cv_applications_service
from app.hepler.enum import OrderType, SortBy, CVApplicationStatus

router = APIRouter()


@router.get("", summary="Get list of cv applications by User.")
async def get_cv_applications(
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
    current_user=Depends(user_manager_service.get_current_user),
    skip: int = Query(None, description="The number of cv to skip.", example=0),
    limit: int = Query(None, description="The number of cv to return.", example=10),
    sort_by: SortBy = Query(
        None, description="The field to sort by.", example=SortBy.CREATED_AT
    ),
    order_by: OrderType = Query(
        None, description="The order to sort by.", example=OrderType.DESC
    ),
    status: CVApplicationStatus = Query(
        None,
        description="The status of cv application.",
        example=CVApplicationStatus.PENDING,
    ),
):
    """
    Get list of cv applications by User.

    This endpoint allows getting a list of cv applications by User.

    Parameters:
    - skip (int): The number of cv to skip.
    - limit (int): The number of cv to return.
    - sort_by (str): The field to sort by.
    - order_by (str): The order to sort by.
    - status (str): The status of cv application.

    Returns:
    - status_code (200): The list of cv applications has been found successfully.
    - status_code (400): The request is invalid.
    - status_code (403): The permission is denied.

    """
    args = locals()

    return await cv_applications_service.get(db, redis, args, current_user)


@router.get("/{id}", summary="Get cv application by id.")
async def get_cv_application_by_id(
    db: Session = Depends(get_db),
    current_user=Depends(user_manager_service.get_current_user),
    id: int = Path(..., description="The id of the cv application.", example=1),
):
    """
    Get cv application by id.

    This endpoint allows getting a cv application by id.

    Parameters:
    - id (int): The id of the cv application.

    Returns:
    - status_code (200): The cv application has been found successfully.
    - status_code (404): The cv application is not found.
    - status_code (403): The permission is denied.

    """
    return await cv_applications_service.get_by_id(db, id, current_user)


@router.post("", summary="Create cv application.")
async def create_cv_application(
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
    current_user=Depends(user_manager_service.get_current_user),
    full_name: str = Form(
        ...,
        description="The full name of the user.",
        json_schema_extra={"example": "Ong Tung"},
    ),
    email: str = Form(
        ...,
        description="The email of the user.",
        json_schema_extra={"example": "ongtung@mail.com"},
    ),
    phone_number: str = Form(
        ...,
        description="The phone number of the user.",
        json_schema_extra={"example": "0123456789"},
    ),
    job_id: int = Form(
        ...,
        description="The job id.",
        json_schema_extra={"example": 1},
    ),
    letter_cover: str = Form(
        None,
        description="The letter cover.",
        json_schema_extra={"example": "I am a student."},
    ),
    cv: UploadFile = File(
        ...,
        description="The cv file and not permitted to be empty.",
    ),
):
    """
    Create cv application.

    This endpoint allows creating cv application.

    Parameters:
    - job_id (int): The job id.
    - cv (str): The cv file.
    - message (str): The message.

    Returns:
    - status_code (201): The cv application has been created successfully.
    - status_code (400): The request is invalid.
    - status_code (403): The permission is denied.

    """
    data = locals()

    return await cv_applications_service.create(db, redis, data, current_user)
