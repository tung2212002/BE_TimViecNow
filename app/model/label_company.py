from sqlalchemy import Column, String

from app.db.base_class import Base


class LabelCompany(Base):
    name = Column(String(10), nullable=False)
