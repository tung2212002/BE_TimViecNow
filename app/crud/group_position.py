from sqlalchemy.orm import Session

from .base import CRUDBase
from app.model import GroupPosition
from app.schema.group_position import (
    GroupPositionCreateRequest,
    GroupPositionUpdateRequest,
    GroupPositionItemResponse,
)


class CRUDGroupPosition(
    CRUDBase[GroupPosition, GroupPositionCreateRequest, GroupPositionUpdateRequest]
):
    pass


group_position = CRUDGroupPosition(GroupPosition)
