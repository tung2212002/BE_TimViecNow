from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.hepler.enum import Role, Gender


class User(Base):
    full_name = Column(String(50), nullable=False)
    email = Column(String(50), primary_key=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    phone_number = Column(String(10), nullable=True)
    gender = Column(Enum(Gender), nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(Role), default=Role.USER)
    is_verified = Column(Boolean, default=False)
    avatar = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
    last_login = Column(DateTime(timezone=True), default=func.now())

    user_job_save = relationship("UserJobSave", back_populates="user")
    cv_application = relationship("CVApplication", back_populates="user")
    user_job_requirement = relationship(
        "UserJobRequirement", back_populates="user", uselist=False
    )
    job_report = relationship("JobReport", back_populates="user")
