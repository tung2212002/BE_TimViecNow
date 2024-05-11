from sqlalchemy.orm import Session

from .base import CRUDBase
from app.model import Category
from app.schema.category import CategoryCreate, CategoryUpdate


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    def get_by_name(self, db: Session, name: str) -> Category:
        return db.query(self.model).filter(self.model.name == name).first()


category = CRUDCategory(Category)
