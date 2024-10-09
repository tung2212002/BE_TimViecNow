from sqlalchemy import Column, ForeignKey, Integer, String, Enum, DateTime
from sqlalchemy.sql import func


from app.db.base_class import Base
from app.hepler.enum import VerifyCodeStatus


class VerifyCode(Base):
    code = Column(String(6), nullable=False)
    email = Column(String(255), nullable=False)
    status = Column(Enum(VerifyCodeStatus), default=VerifyCodeStatus.ACTIVE)
    failed_attempts = Column(Integer, default=0, nullable=False)
    session_id = Column(String(255), index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
    expired_at = Column(DateTime(timezone=True), index=True)
    manager_id = Column(
        Integer, ForeignKey("manager.id", ondelete="CASCADE"), nullable=False
    )
