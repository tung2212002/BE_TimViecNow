from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from redis.asyncio import Redis

from app.db.base import get_db
from app.storage.redis import get_redis
from app.core.chat.chat_service import chat_service
from app.core.auth.user_manager_service import user_manager_service
from app.model import Account


router = APIRouter()


@router.get("/contactables", summary="Get list of contactables.")
async def get_contactables(
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
    current_user: Account = Depends(
        user_manager_service.get_current_user_or_business_verify
    ),
    skip: int = Query(
        None, description="The number of contactable to skip.", example=0
    ),
    limit: int = Query(
        None, description="The number of contactable to return.", example=10
    ),
):
    """
    Get list of contactables.

    This endpoint allows getting a list of contactables.

    Parameters:
    - skip (int): The number of contactables to skip.
    - limit (int): The number of contactables to return.

    Returns:
    - status_code (200): The list of contactables has been found successfully.
    - status_code (401): The user is not authorized.
    """

    args = locals()

    return await chat_service.get_contactables(db, redis, args, current_user)


@router.get("", summary="Get list of conversations.")
async def get_conversation(
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
    current_user=Depends(user_manager_service.get_current_user_or_business_verify),
    skip: int = Query(
        None, description="The number of conversation to skip.", example=0
    ),
    limit: int = Query(
        None, description="The number of conversation to return.", example=100
    ),
):
    """
    Get list of conversations.

    This endpoint allows getting a list of conversations.

    Parameters:
    - skip (int): The number of conversations to skip.
    - limit (int): The number of conversations to return.

    Returns:
    - status_code (200): The list of conversations has been found successfully.
    - status_code (401): The user is not authorized.
    - status_code (400): The request is invalid.
    """

    return await chat_service.get(db, redis, current_user, skip, limit)
