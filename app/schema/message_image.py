from pydantic import BaseModel, ConfigDict, validator
from datetime import datetime
from typing import List
from fastapi import UploadFile

from app.hepler.schema_validator import SchemaValidator


# request
class AttachmentCreateRequest(BaseModel):
    files: List[UploadFile]
    conversation_id: int

    @validator("files")
    def validate_files(cls, v):
        return SchemaValidator.validate_files(v)

    model_config = ConfigDict(from_attribute=True, extra="ignore")


# schema
class MessageImageCreate(BaseModel):
    message_id: int
    url: str
    position: int

    model_config = ConfigDict(from_attribute=True, extra="ignore")


# response
class MessageImageResponse(BaseModel):
    id: int
    message_id: int
    url: str
    position: int

    model_config = ConfigDict(from_attribute=True, extra="ignore")


class AttachmentResponse(BaseModel):
    upload_filename: str
    url: str = None

    @validator("url", pre=True)
    def validate_url(cls, v, values):
        return SchemaValidator.validate_attachment_url(v, values)
