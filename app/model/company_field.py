from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class CompanyField(Base):
    company_id = Column(
        Integer, ForeignKey("company.id", ondelete="CASCADE"), index=True
    )
    field_id = Column(Integer, ForeignKey("field.id", ondelete="CASCADE"), index=True)

    company = relationship(
        "Company", back_populates="company_field_secondary", overlaps="fields"
    )
