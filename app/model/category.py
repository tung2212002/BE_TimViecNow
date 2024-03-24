from sqlalchemy import Column, String

from app.db.base_class import Base


class Category(Base):
    name = Column(String(50), nullable=False)
