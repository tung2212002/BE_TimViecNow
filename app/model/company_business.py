from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class CompanyBusiness(Base):
    business_id = Column(Integer, ForeignKey("business.id", ondelete="CASCADE"))
    company_id = Column(Integer, ForeignKey("company.id", ondelete="CASCADE"))
