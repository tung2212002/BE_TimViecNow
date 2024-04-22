from sqlalchemy import Column, Enum, Integer, String, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.hepler.enum import Role, Gender


class Business(Base):
    manager_base_id = Column(
        Integer, ForeignKey("manager_base.id", ondelete="CASCADE"), primary_key=True
    )
    province_id = Column(Integer, ForeignKey("province.id"), nullable=False)
    district_id = Column(Integer, ForeignKey("district.id"), nullable=True)
    phone_number = Column(String(10), nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    company_name = Column(String(255), nullable=False)
    work_position = Column(String(100), nullable=False)
    work_location = Column(String(100), nullable=True)
    is_verified_email = Column(Boolean, default=False)
    is_verified_phone = Column(Boolean, default=False)
    is_verified_company = Column(Boolean, default=False)
    is_verified_identity = Column(Boolean, default=False)
    company_id = Column(Integer, ForeignKey("company.id"), nullable=True)

    manager_base = relationship("ManagerBase", back_populates="business")
    province = relationship("Province", back_populates="business", uselist=False)
    district = relationship("District", back_populates="business", uselist=False)
    job = relationship("Job", back_populates="business")
    business_history = relationship("BusinessHistory", back_populates="business")
    campaign = relationship("Campaign", back_populates="business")
