from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

from app.hepler.enum import ReactionType


class MessageReactionCreate(BaseModel):
    message_id: int
    account_id: int
    type: ReactionType = ReactionType.LIKE

    model_config = ConfigDict(from_attribute=True, extra="ignore")


class MessageReactionResponse(BaseModel):
    id: int
    message_id: int
    account_id: int
    type: ReactionType
    created_at: datetime

    model_config = ConfigDict(from_attribute=True, extra="ignore")
