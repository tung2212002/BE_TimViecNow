from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
    Depends,
    HTTPException,
    Request,
    status,
)
from sqlalchemy.orm import Session
from redis.asyncio import Redis

from app.db.base import get_db
from app.storage.redis import get_redis
from app.core.auth.user_manager_service import user_manager_service
from app.core.conversation.conversation_service import conversation_service

router = APIRouter()


@router.get("", summary="Get list messages of conversation.")
async def get_conversation(
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
    current_user=Depends(user_manager_service.get_current_account_verify_websocket),
):
    return await conversation_service.get(db, current_user)
