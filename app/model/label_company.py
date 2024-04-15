from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class LabelCompany(Base):
    name = Column(String(10), nullable=False)
    description = Column(String(255), nullable=True)

    company = relationship("Company", back_populates="label_company")
