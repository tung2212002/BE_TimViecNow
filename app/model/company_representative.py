from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class CompanyPresentative(Base):
    presentative_id = Column(
        Integer, ForeignKey("representative.id", ondelete="CASCADE")
    )
    company_id = Column(Integer, ForeignKey("company.id", ondelete="CASCADE"))
