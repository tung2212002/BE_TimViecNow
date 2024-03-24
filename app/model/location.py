from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class Location(Base):
    city = Column(String(50), nullable=True)
    province = Column(String(50), nullable=True)
    district = Column(String(50), nullable=True)
    country = Column(String(50), nullable=False, default="Vietnam")
