from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.hepler.enum import HistoryType


class BusinessHistory(Base):
    business_id = Column(
        Integer, ForeignKey("business.id", ondelete="CASCADE"), index=True
    )
    content = Column(String(255), nullable=False)
    type = Column(Enum(HistoryType), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    business = relationship(
        "Business", back_populates="business_history", uselist=False
    )
