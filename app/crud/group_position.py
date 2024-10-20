from sqlalchemy.orm import Session

from .base import CRUDBase
from app.model import GroupPosition
from app.schema.group_position import (
    GroupPositionCreate,
    GroupPositionUpdate,
)


class CRUDGroupPosition(
    CRUDBase[GroupPosition, GroupPositionCreate, GroupPositionUpdate]
):
    def get_by_name(self, db: Session, name: str) -> GroupPosition:
        return db.query(self.model).filter(self.model.name == name).first()


group_position = CRUDGroupPosition(GroupPosition)
