from sqlalchemy import Column, String

from app.db.base_class import Base


class JobPosition(Base):
    name = Column(String(50), nullable=False)
