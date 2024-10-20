from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class PinnedMessageCreate(BaseModel):
    message_id: int
    account_id: int
    conversation_id: int

    model_config = ConfigDict(from_attribute=True, extra="ignore")
