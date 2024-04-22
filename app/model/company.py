from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.hepler.enum import Role, CompanyType


class Company(Base):
    name = Column(String(255), index=True, nullable=False)
    email = Column(String(50), unique=True, index=True, nullable=False)
    type = Column(Enum(CompanyType), default=CompanyType.COMPANY, nullable=False)
    address = Column(String(255), nullable=False)
    phone_number = Column(String(10), nullable=False)
    logo = Column(String(255), nullable=True)
    total_active_jobs = Column(Integer, default=0)
    is_premium = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    label_company_id = Column(Integer, ForeignKey("label_company.id"), nullable=True)
    website = Column(String(255), nullable=True)
    scale = Column(String(20), nullable=False)
    tax_code = Column(String(15), unique=True, index=True, nullable=False)
    company_short_description = Column(String(255), nullable=True)
    follower = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
    business_id = Column(
        Integer, ForeignKey("business.id", ondelete="CASCADE"), nullable=False
    )

    label_company = relationship(
        "LabelCompany", back_populates="company", uselist=False
    )
    fields = relationship("Field", secondary="company_field")
