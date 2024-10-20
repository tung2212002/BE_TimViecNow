from fastapi import APIRouter, Depends, Request, Query, Path
from sqlalchemy.orm import Session
from redis.asyncio import Redis

from app.db.base import get_db
from app.storage.redis import get_redis
from app.core.auth.user_manager_service import user_manager_service
from app.core.conversation.conversation_service import conversation_service
from app.core.message.message_service import message_service

router = APIRouter()


@router.get("/{conversation_id}/messages", summary="Get list of messages.")
async def get_conversation(
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
    current_user=Depends(user_manager_service.get_current_user_or_business_verify),
    conversation_id: int = Path(..., description="The conversation id.", example=1),
    skip: int = Query(
        None, description="The number of conversation to skip.", example=0
    ),
    limit: int = Query(
        None, description="The number of conversation to return.", example=100
    ),
):
    """
    Get list of messages.

    This endpoint allows getting a list of messages.

    Parameters:
    - skip (int): The number of messages to skip.
    - limit (int): The number of messages to return.

    Returns:
    - status_code (200): The list of messages has been found successfully.
    - status_code (401): The user is not authorized.
    """

    args = locals()

    return await message_service.get(db, redis, args, current_user)
