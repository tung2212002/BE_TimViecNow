from fastapi import WebSocket
from sqlalchemy.orm import Session
from redis.asyncio import Redis
from typing import List, Union

from app.core.websocket.websocket_manager import WebsocketManager
from app.model import (
    Message,
    MessageImage,
    MessageReaction,
    PinnedMessage,
    ConversationMember,
    Account,
    Conversation,
)
from app.schema.websocket import (
    NewMessageSchema,
    NewConversationSchema,
    UpdateConversationSchema,
    UserTypingSchema,
    AddMemberSchema,
    ResponseMessageSchema,
)
from app.schema.account import AccountBasicResponse
from app.schema.message import MessageCreate, MessageUpdate
from app.schema.message_image import MessageImageCreate
from app.schema.message_reaction import MessageReactionCreate
from app.schema.pinned_message import PinnedMessageCreate
from app.schema.conversation_member import ConversationMemberCreate
from app.schema.conversation import (
    ConversationCreate,
    ConversationUpdate,
    ConversationResponse,
)
from app.schema.user import UserBasicResponse
from app.schema.business import BusinessBasicInfoResponse
from app.crud import (
    message as messageCRUD,
    message_image as message_imageCRUD,
    message_reaction as message_reactionCRUD,
    pinned_message as pinned_messageCRUD,
    conversation_member as conversation_memberCRUD,
    conversation as conversationCRUD,
    account as accountCRUD,
)
from app.core.conversation.conversation_helper import conversation_helper
from app.hepler.enum import WebsocketActionType, TypeAccount, MessageType
from app.common.exception import CustomException
from app.core.websocket.websocket_helper import websocket_helper
from app.storage.cache.message_cache_service import message_cache_service


class WebsocketHandler:
    def __init__(self, websocket_manager: WebsocketManager):
        self.websocket_manager: WebsocketManager = websocket_manager
        self.websocket_manager.handler_register(
            WebsocketActionType.NEW_MESSAGE, self.new_message_handler
        )
        self.websocket_manager.handler_register(
            WebsocketActionType.USER_TYPING, self.user_typing_handler
        )

    async def new_message_handler(
        self,
        websocket: WebSocket,
        db: Session,
        redis: Redis,
        incoming_message: dict,
        current_user: Account,
    ):
        try:
            new_message_data: NewMessageSchema = NewMessageSchema(**incoming_message)
        except ValueError as e:
            await self.websocket_manager.send_error(
                websocket, "Invalid message format."
            )
            return

        conversation_id: int = new_message_data.conversation_id

        if not conversation_id:
            if not new_message_data.members:
                await self.websocket_manager.send_error(
                    websocket, "Conversation id or members is required."
                )
                return

            member_ids: List[int] = conversation_helper.filter_member(
                new_message_data.members, current_user
            )

            response_conversation, members = await websocket_helper.new_conversation(
                db, redis, websocket, current_user, member_ids, websocket_manager
            )
            user_id_to_websocket: dict = websocket_manager.user_id_to_websocket
            for member in members:
                websockets = user_id_to_websocket.get(member.id)
                if websockets:
                    for ws in websockets:
                        await websocket_manager.add_conversation(
                            response_conversation.id, ws
                        )

            outcoming_message: NewConversationSchema = NewConversationSchema(
                id=response_conversation.id,
                name=response_conversation.name,
                avatar=response_conversation.avatar,
                members=response_conversation.members,
                created_at=response_conversation.created_at,
                conversation_type=response_conversation.type,
            )

            await websocket_manager.broadcast(
                response_conversation.id, outcoming_message.model_dump_json()
            )
            conversation_id = response_conversation.id

        else:
            is_valid_conversation = await conversation_helper.is_join_conversation(
                db, redis, conversation_id, current_user.id
            )
            if not is_valid_conversation:
                await self.websocket_manager.send_error(
                    websocket,
                    f"Conversation {conversation_id} not found in your conversations.",
                )
                return
        type = new_message_data.type
        if type == MessageType.TEXT:
            outcoming_message: ResponseMessageSchema = (
                await websocket_helper.create_text_message(
                    db, redis, current_user, conversation_id, new_message_data
                )
            )
            await websocket_manager.broadcast(
                conversation_id, outcoming_message.model_dump_json()
            )

    async def user_typing_handler(
        self,
        websocket: WebSocket,
        db: Session,
        redis: Redis,
        incoming_message: dict,
        current_user: Account,
    ):
        user_typing_data: UserTypingSchema = UserTypingSchema(**incoming_message)
        conversation_id: int = user_typing_data.conversation_id

        is_join_conversation = await conversation_helper.is_join_conversation(
            db, redis, conversation_id, current_user.id
        )

        if not is_join_conversation:
            await self.websocket_manager.send_error(
                websocket,
                f"Conversation {conversation_id} not found in your conversations.",
            )
            return

        await websocket_manager.broadcast(
            conversation_id, user_typing_data.model_dump_json()
        )

    async def add_user_to_conversation_handler(
        self,
        websocket: WebSocket,
        db: Session,
        redis: Redis,
        incoming_message: dict,
        current_user: Account,
    ):
        pass

    async def remove_user_from_conversation_handler(
        self,
        websocket: WebSocket,
        db: Session,
        redis: Redis,
        incoming_message: dict,
        current_user: Account,
    ):
        pass

    async def update_conversation_handler(
        self,
        websocket: WebSocket,
        db: Session,
        redis: Redis,
        incoming_message: dict,
        current_user: Account,
    ):
        pass

    async def reaction_message_handler(
        self,
        websocket: WebSocket,
        db: Session,
        redis: Redis,
        incoming_message: dict,
        current_user: Account,
    ):
        pass


websocket_manager = WebsocketManager()
websocket_handler = WebsocketHandler(websocket_manager)
