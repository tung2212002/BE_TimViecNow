from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class District(Base):
    name = Column(String(100), nullable=False, index=True)
    code = Column(String(10), unique=True, index=True)
    name_with_type = Column(String(100), nullable=False, index=True)
    slug = Column(String(100), nullable=False, index=True)
    type = Column(String(100), nullable=False)
    province_id = Column(
        Integer, ForeignKey("province.id", ondelete="CASCADE"), nullable=False
    )

    province = relationship("Province", back_populates="district", uselist=False)
    representative = relationship("Representative", back_populates="district")
