from sqlalchemy import Column, Enum, Integer, String, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.hepler.enum import Role, Gender


class Representative(Base):
    manager_base_id = Column(Integer, ForeignKey("manager_base.id"), primary_key=True)
    province_id = Column(Integer, ForeignKey("province.id"), nullable=False)
    district_id = Column(Integer, ForeignKey("district.id"), nullable=True)
    phone_number = Column(String(10), nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    company = Column(String(255), nullable=False)
    work_position = Column(String(100), nullable=False)
    work_location = Column(String(100), nullable=True)

    manager_base = relationship("ManagerBase", back_populates="representative")
    province = relationship("Province", back_populates="representative", uselist=False)
    district = relationship("District", back_populates="representative", uselist=False)
    job_approval_request = relationship(
        "JobApprovalRequest", back_populates="representative"
    )
    job = relationship("Job", back_populates="representative")
    representative_history = relationship(
        "RepresentativeHistory", back_populates="representative"
    )
    companies = relationship("Company", back_populates="representative")
