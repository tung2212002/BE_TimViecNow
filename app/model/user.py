from sqlalchemy import Column, String, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.hepler.enum import Role, Gender, TypeAccount


class User(Base):
    full_name = Column(String(50), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    phone_number = Column(String(10), nullable=True)
    gender = Column(Enum(Gender), nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(Role), default=Role.USER)
    is_verified = Column(Boolean, default=False)
    avatar = Column(String(255), nullable=True)
    type_account = Column(Enum(TypeAccount), default=TypeAccount.NORMAL)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
    last_login = Column(DateTime(timezone=True), default=func.now())

    user_job_save = relationship("UserJobSave", back_populates="user")
    cv_applications = relationship("CVApplication", back_populates="user")
    user_job_requirement = relationship(
        "UserJobRequirement", back_populates="user", uselist=False
    )
    job_reports = relationship("JobReport", back_populates="user")
    social_network = relationship("SocialNetwork", back_populates="user")
