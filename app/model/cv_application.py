from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.hepler.enum import CVApplicationStatus


class CVApplication(Base):
    campaign_id = Column(
        Integer,
        ForeignKey("campaign.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id = Column(
        Integer,
        ForeignKey("user.id"),
        nullable=False,
        index=True,
    )
    cv = Column(String(255), nullable=False)
    full_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    phone_number = Column(String(10), nullable=False)
    letter_cover = Column(String(500), nullable=True)
    count_view = Column(Integer, default=0, nullable=False)
    status = Column(
        Enum(CVApplicationStatus), default=CVApplicationStatus.PENDING, nullable=False
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    campaign = relationship(
        "Campaign",
        back_populates="cv_applications",
        uselist=False,
        single_parent=True,
    )
    user = relationship(
        "User",
        back_populates="cv_applications",
        uselist=False,
        single_parent=True,
    )
