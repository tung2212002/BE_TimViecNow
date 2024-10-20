from pydantic import BaseModel
from typing import Optional


# schema
class ManagerCreate(BaseModel):
    id: int
    email: str
    password: str
    phone_number: str


class ManagerUpdate(BaseModel):
    password: Optional[str] = None
    phone_number: Optional[str] = None
