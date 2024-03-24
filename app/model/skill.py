from sqlalchemy import Column, Integer, ForeignKey, String

from app.db.base_class import Base


class Skill(Base):
    name = Column(String(50), nullable=False)
