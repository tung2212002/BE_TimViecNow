from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.hepler.enum import HistoryType


class RepresentativeHistory(Base):
    content = Column(String(255), nullable=False)
    type = Column(Enum(HistoryType), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
