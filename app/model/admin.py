from sqlalchemy import Column, String, Enum, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.hepler.enum import Role, Gender
from app.db.base_class import Base


class Admin(Base):
    manager_base_id = Column(
        Integer, ForeignKey("manager_base.id"), primary_key=True, index=True
    )
    is_verified = Column(Boolean, default=False)
    phone_number = Column(String(10), nullable=False)
    gender = Column(Enum(Gender), nullable=True)
    role = Column(Enum(Role), default=Role.ADMIN)

    manager_base = relationship("ManagerBase", back_populates="admin")