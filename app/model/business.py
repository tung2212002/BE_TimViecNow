from sqlalchemy import Column, Enum, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.hepler.enum import Gender


class Business(Base):
    id = Column(
        Integer,
        ForeignKey("manager.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )
    province_id = Column(Integer, ForeignKey("province.id"), nullable=False)
    district_id = Column(Integer, ForeignKey("district.id"), nullable=True)
    gender = Column(Enum(Gender), nullable=False)
    company_name = Column(String(255), nullable=False)
    work_position = Column(String(100), nullable=False)
    work_location = Column(String(100), nullable=True)
    is_verified_email = Column(Boolean, default=False)
    is_verified_phone = Column(Boolean, default=False)
    is_verified_company = Column(Boolean, default=False)
    is_verified_identity = Column(Boolean, default=False)

    manager = relationship(
        "Manager",
        back_populates="business",
        single_parent=True,
        passive_deletes=True,
    )
    province = relationship("Province", back_populates="business", uselist=False)
    district = relationship("District", back_populates="business", uselist=False)
    job = relationship("Job", back_populates="business", passive_deletes=True)
    business_history = relationship("BusinessHistory", back_populates="business")
    campaign = relationship("Campaign", back_populates="business", passive_deletes=True)
    company = relationship(
        "Company",
        secondary="company_business",
        overlaps="company_business",
        lazy="subquery",
        uselist=False,
        passive_deletes=True,
    )
