from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Province(Base):
    name = Column(String(50), nullable=False, unique=True, index=True)
    code = Column(String(10), index=True, unique=True)
    name_with_type = Column(String(50), nullable=False, unique=True, index=True)
    slug = Column(String(50), nullable=False, unique=True, index=True)
    type = Column(String(50), nullable=False)
    country = Column(String(50), default="Việt Nam")

    district = relationship("District", back_populates="province")
    business = relationship("Business", back_populates="province")
    work_location = relationship("WorkLocation", back_populates="province")
