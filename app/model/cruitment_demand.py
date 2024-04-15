from sqlalchemy import Column, Integer, String, DateTime

from app.db.base_class import Base


class CruitmentDemand(Base):
    key = Column(String(50), nullable=False)
    value = Column(Integer, nullable=False)
    time_scan = Column(DateTime(timezone=True), nullable=False)
