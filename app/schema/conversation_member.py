from pydantic import BaseModel, ConfigDict
from typing import Optional

from app.hepler.enum import MemberType


class ConversationMemberBase(BaseModel):
    type: MemberType = MemberType.MEMBER
    nickname: Optional[str] = None

    model_config = ConfigDict(from_attribute=True, extra="ignore")


# request
class ConversationMemberCreate(ConversationMemberBase):
    conversation_id: int
    account_id: int


class ConversationMemberUpdate(ConversationMemberBase):
    pass
