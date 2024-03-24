from sqlalchemy import Column, ForeignKey, Integer

from app.db.base_class import Base


class CompanyPresentative(Base):
    presentative_id = Column(Integer, ForeignKey("representative.id"))
    company_id = Column(Integer, ForeignKey("company.id"))
