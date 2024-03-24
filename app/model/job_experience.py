from sqlalchemy import Column, String

from app.db.base_class import Base


class JobExperience(Base):
    name = Column(String(50), nullable=False)
