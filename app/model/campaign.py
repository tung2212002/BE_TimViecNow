from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.hepler.enum import CampaignStatus


class Campaign(Base):
    title = Column(String(255), nullable=False)
    status = Column(Enum(CampaignStatus), default=CampaignStatus.OPEN)
    is_flash = Column(Boolean, default=False)
    optimal_score = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
    business_id = Column(
        Integer, ForeignKey("business.id", ondelete="CASCADE"), nullable=False
    )

    business = relationship("Business", back_populates="campaign")
    job = relationship("Job", back_populates="campaign")
