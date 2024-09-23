from sqlalchemy.orm import Session

from .base import CRUDBase
from app.model import GroupPosition
from app.schema.group_position import (
    GroupPositionCreateRequest,
    GroupPositionUpdateRequest,
)


class CRUDGroupPosition(
    CRUDBase[GroupPosition, GroupPositionCreateRequest, GroupPositionUpdateRequest]
):
    def get_by_name(self, db: Session, name: str):
        return db.query(self.model).filter(self.model.name == name).first()


group_position = CRUDGroupPosition(GroupPosition)
