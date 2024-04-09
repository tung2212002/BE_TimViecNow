from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


from app.db.base_class import Base
from app.hepler.enum import VerifyCodeStatus


class VerifyCode(Base):
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(6), nullable=False)
    email = Column(String(50), nullable=False)
    status = Column(Enum(VerifyCodeStatus), default=VerifyCodeStatus.ACTIVE)
    failed_attempts = Column(Integer, default=0)
    session_id = Column(String(255), index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    expired_at = Column(DateTime(timezone=True), index=True)
    manager_base_id = Column(Integer, ForeignKey("manager_base.id"))
