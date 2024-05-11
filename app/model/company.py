from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Boolean,
    DateTime,
    Enum,
    Text,
    event,
)
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.hepler.enum import CompanyType
from app.model.company_business import CompanyBusiness


class Company(Base):
    name = Column(String(255), index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    type = Column(Enum(CompanyType), default=CompanyType.COMPANY, nullable=False)
    address = Column(String(255), nullable=False)
    phone_number = Column(String(10), nullable=False)
    logo = Column(String(255), nullable=True)
    banner = Column(String(255), nullable=True)
    total_active_jobs = Column(Integer, default=0)
    is_premium = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    label_company_id = Column(Integer, ForeignKey("label_company.id"), nullable=True)
    website = Column(String(255), nullable=True)
    scale = Column(String(20), nullable=False)
    tax_code = Column(String(15), unique=True, index=True, nullable=False)
    company_short_description = Column(Text, nullable=True)
    follower = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
    business_id = Column(
        Integer, ForeignKey("business.id", ondelete="CASCADE"), nullable=False
    )

    business = relationship("Business", back_populates="company")
    label_company = relationship(
        "LabelCompany",
        back_populates="company",
        uselist=False,
        passive_deletes=True,
    )
    fields = relationship(
        "Field",
        secondary="company_field",
        overlaps="fields",
        passive_deletes=True,
    )
    company_field_secondary = relationship(
        "CompanyField",
        back_populates="company",
        overlaps="fields",
        passive_deletes=True,
    )
    businesses = relationship(
        "Business",
        secondary="company_business",
        overlaps="company,company,company_business,business",
        passive_deletes=True,
    )
    campaigns = relationship(
        "Campaign",
        back_populates="company",
        passive_deletes=True,
    )


@event.listens_for(Company, "after_insert")
def receive_after_insert(mapper, connection, target):
    session = Session(bind=connection)
    company_business = CompanyBusiness(
        company_id=target.id, business_id=target.business_id
    )
    session.add(company_business)
    session.commit()
    session.close()
