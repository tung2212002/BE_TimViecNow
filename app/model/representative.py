from sqlalchemy import Column, Enum, Integer, String, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.hepler.enum import Role, Gender


class Representative(Base):
    manager_base_id = Column(Integer, ForeignKey("manager_base.id"), primary_key=True)
    role = Column(Enum(Role), default=Role.REPRESENTATIVE, nullable=False)
    phone_number = Column(String(10), nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    company = Column(String(255), nullable=False)
    work_position = Column(String(100), nullable=False)
    work_location = Column(String(100), nullable=False)
    district = Column(String(100), nullable=False)
    location_id = Column(Integer, ForeignKey("location.id"), nullable=False)

    manager_base = relationship("ManagerBase", back_populates="representative")
