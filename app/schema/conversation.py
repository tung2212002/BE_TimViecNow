from pydantic import BaseModel, ConfigDict, validator
from fastapi import UploadFile, File
from typing import Optional
from datetime import datetime
from typing import List

from app.hepler.enum import ConversationType
from app.hepler.schema_validator import SchemaValidator
from app.schema.account import AccountBasicResponse
from app.schema.message import MessageBasicResponse


# request
class ConversationCreateRequest(BaseModel):
    members: List[int]

    @validator("members")
    def validate_member(cls, v):
        return SchemaValidator.validate_list_member(v)

    model_config = ConfigDict(from_attribute=True, extra="ignore")


class ConversationUpdateRequest(BaseModel):
    id: int
    name: Optional[str] = None

    model_config = ConfigDict(from_attribute=True, extra="ignore")


class ConversationGetExistWithListMemberRequest(BaseModel):
    members: List[int]

    @validator("members")
    def validate_member(cls, v):
        return SchemaValidator.validate_list_member(v)

    model_config = ConfigDict(from_attribute=True, extra="ignore")


class ConversationUpdateAvatarRequest(BaseModel):
    id: int
    avatar: Optional[UploadFile]

    @validator("avatar")
    def validate_avatar(cls, v):
        return SchemaValidator.validate_avatar_upload_file(v)

    model_config = ConfigDict(from_attribute=True, extra="ignore")


# schema
class ConversationCreate(BaseModel):
    type: ConversationType = ConversationType.PRIVATE
    name: Optional[str] = None
    avatar: Optional[str] = None
    count_member: int = 2
    account_id: int

    model_config = ConfigDict(from_attribute=True, extra="ignore")


class ConversationUpdate(BaseModel):
    name: Optional[str] = None
    avatar: Optional[str] = None

    model_config = ConfigDict(from_attribute=True, extra="ignore")


# response
class ConversationResponse(BaseModel):
    id: int
    type: ConversationType
    name: Optional[str] = None
    avatar: Optional[str] = None
    count_member: int
    members: List[AccountBasicResponse]
    last_message: Optional[MessageBasicResponse] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attribute=True, extra="ignore")
