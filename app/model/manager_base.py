from sqlalchemy import Column, String, Enum, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.hepler.enum import Role, Gender, TypeAccount
from app.db.base_class import Base


class ManagerBase(Base):
    full_name = Column(String(50), nullable=False)
    email = Column(String(50), primary_key=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    avatar = Column(String(255), nullable=True)
    role = Column(Enum(Role), default=Role.BUSINESS)
    type_account = Column(Enum(TypeAccount), default=TypeAccount.BUSINESS)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
    last_login = Column(DateTime(timezone=True), default=func.now())

    admin = relationship(
        "Admin", back_populates="manager_base", lazy=True, uselist=False
    )
    business = relationship(
        "Business", back_populates="manager_base", lazy=True, uselist=False
    )
