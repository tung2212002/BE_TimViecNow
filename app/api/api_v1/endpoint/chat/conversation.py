from fastapi import (
    APIRouter,
    Depends,
    Body,
    File,
    UploadFile,
    Query,
)
from sqlalchemy.orm import Session
from redis.asyncio import Redis
from typing import List

from app.db.base import get_db
from app.storage.redis import get_redis
from app.core.auth.user_manager_service import user_manager_service
from app.core.conversation.conversation_service import conversation_service

router = APIRouter()


@router.get("")
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
    -
    """
    args = locals()

    return await conversation_service.get(db, redis, args, current_user)


@router.get("/existing")
async def get_existing_conversation(
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
    current_user=Depends(user_manager_service.get_current_user_or_business_verify),
    members: List[int] = Query(
        ...,
        description="The list of user ids.",
        example=[1, 2],
    ),
):
    """
    Get existing conversation.

    This endpoint allows getting an existing conversation.

    Parameters:
    - members (list): The list of user ids.

    Returns:
    - status_code (200): The conversation has been found successfully.
    - status_code (400): Request is invalid.
    - status_code (404): The conversation is not found.

    """
    args = locals()

    return await conversation_service.get_existing_conversation(
        db, redis, args, current_user
    )


@router.get("/{conversation_id}")
async def get_by_id(
    conversation_id: int,
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
    current_user=Depends(user_manager_service.get_current_user_or_business_verify),
):
    """
    Get conversation by id.

    This endpoint allows getting a conversation by id.

    Parameters:
    - conversation_id (int): The conversation id.

    Returns:
    - status_code (200): The conversation has been found successfully.
    - status_code (404): The conversation is not found.

    """

    return await conversation_service.get_by_id(
        db, redis, conversation_id, current_user
    )


@router.post("")
async def create_conversation(
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
    current_user=Depends(user_manager_service.get_current_user_or_business_verify),
    data: dict = Body(
        ...,
        description="Include the list of members id.",
        example={
            "members": [1, 2],
        },
    ),
):
    """
    Create conversation.

    This endpoint allows creating a conversation.

    Parameters:
    - members (list): The list of members id.

    Returns:
    - status_code (201): The conversation has been created successfully.
    - status_code (400): The conversation is already exists.

    """
    return await conversation_service.create(db, redis, data, current_user)


@router.post("/{conversation_id}/attachment")
async def upload_attachment(
    conversation_id: int,
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
    current_user=Depends(user_manager_service.get_current_user_or_business_verify),
    attachments: List[UploadFile] = File(
        ...,
        description="The list of attachments.",
    ),
):
    """
    Upload attachment.

    This endpoint allows uploading attachments to the conversation.

    Parameters:
    - attachments (list): The list of attachments.

    Returns:
    - status_code (200): The attachments have been uploaded successfully.
    - status_code (404): The conversation is not found.

    """

    return await conversation_service.upload_attachment(
        db,
        redis,
        {"conversation_id": conversation_id, "files": attachments},
        current_user,
    )


@router.put("/{conversation_id}")
async def update_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
    current_user=Depends(user_manager_service.get_current_user_or_business_verify),
    data: dict = Body(
        ...,
        description="New information of the conversation.",
        example={
            "name": "New name",
        },
    ),
):
    """
    Update conversation.

    This endpoint allows updating a conversation.

    Parameters:
    - name (str): The new name of the conversation.

    Returns:
    - status_code (200): The conversation has been updated successfully.
    - status_code (404): The conversation is not found.

    """

    return await conversation_service.update(
        db, redis, {"id": conversation_id, **data}, current_user
    )


@router.put("/{conversation_id}/avatar")
async def update_avatar(
    conversation_id: int,
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
    current_user=Depends(user_manager_service.get_current_user_or_business_verify),
    avatar: UploadFile = File(..., description="The avatar of the conversation."),
):
    """
    Update avatar.

    This endpoint allows updating the avatar of the conversation.

    Parameters:
    - avatar (file): The avatar of the conversation.

    Returns:
    - status_code (200): The avatar has been updated successfully.
    - status_code (404): The conversation is not found.

    """

    return await conversation_service.update_avatar(
        db, redis, {"id": conversation_id, "avatar": avatar}, current_user
    )
