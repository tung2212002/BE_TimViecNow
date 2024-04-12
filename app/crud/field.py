from sqlalchemy.orm import Session

from .base import CRUDBase
from app.model import Field
from app.schema.field import FieldCreate, FieldUpdate


class CRUDField(CRUDBase[Field, FieldCreate, FieldUpdate]):
    def get_by_name(self, db: Session, name: str) -> Field:
        return db.query(self.model).filter(self.model.name == name).first()


field = CRUDField(Field)
