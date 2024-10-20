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
from app.core.websocket.websocket_service import websocket_service

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
    current_user=Depends(user_manager_service.get_current_account_verify_websocket),
):
    await websocket_service.connect(websocket, db, redis, current_user)
