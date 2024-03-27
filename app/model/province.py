from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Province(Base):
    name = Column(String(100), nullable=False, unique=True, index=True)
    code = Column(String(10), index=True, primary_key=True)
    name_with_type = Column(String(100), nullable=False, unique=True, index=True)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    type = Column(String(100), nullable=False)
    country = Column(String(100), default="Việt Nam")

    district = relationship("District", back_populates="province")
    representative = relationship("Representative", back_populates="province")
