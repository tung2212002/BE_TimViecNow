from pydantic import BaseModel, ConfigDict, validator, Field
from typing import List, Union, Optional
from datetime import datetime

from app.hepler.enum import WebsocketActionType
from app.schema.user import UserBasicResponse
from app.schema.business import BusinessBasicInfoResponse
from app.hepler.enum import MessageType, ConversationType
from app.schema.account import AccountBasicResponse
from app.schema.message_reaction import MessageReactionResponse
from app.schema.message_image import AttachmentResponse


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attribute=True, extra="ignore")


class NewMessageSchema(BaseSchema):
    content: str = Field(..., min_length=1, max_length=255)
    members: List[int] = []
    conversation_id: int = None
    type: MessageType = MessageType.TEXT
    parent_id: int = None
    attachments: List[str] = []

    @validator("conversation_id")
    def contain_members_or_conversation(cls, v, values):
        if "members" not in values and "conversation_id" not in values:
            raise ValueError("Must contain members or conversation_id")
        return v


class ResponseMessageSchema(BaseSchema):
    id: int
    conversation_id: int
    account_id: int
    type: WebsocketActionType = WebsocketActionType.NEW_MESSAGE
    content: str
    created_at: datetime
    dislike_count: Optional[int] = 0
    like_count: Optional[int] = 0
    is_pinned: Optional[bool] = False
    parent_id: Optional[int] = None
    parent: Optional[dict] = None
    reaction: Optional[MessageReactionResponse] = None
    atttachments: Optional[List[AttachmentResponse]] = None
    user: AccountBasicResponse


class UserTypingSchema(BaseSchema):
    type: WebsocketActionType = WebsocketActionType.USER_TYPING
    user_id: int
    conversation_id: int


class ResponseUserTypingSchema(BaseSchema):
    user_id: int
    conversation_id: int


class NewConversationSchema(BaseSchema):
    type: WebsocketActionType = WebsocketActionType.NEW_CONVERSATION
    id: int
    name: Optional[str] = None
    conversation_type: ConversationType
    created_at: datetime
    members: List[AccountBasicResponse]


class AddMemberSchema(BaseSchema):
    type: WebsocketActionType = WebsocketActionType.ADD_MEMBER
    conversation_id: int
    user_id: int
    member_type: str


class UpdateConversationSchema(BaseSchema):
    type: WebsocketActionType = WebsocketActionType.UPDATE_CONVERSATION
    id: int
    name: Optional[str] = None
    updated_at: str


class UpdateAvatarConversationSchema(BaseSchema):
    type: WebsocketActionType = WebsocketActionType.UPDATE_AVATAR_CONVERSATION
    id: int
    avatar: str
    updated_at: str
