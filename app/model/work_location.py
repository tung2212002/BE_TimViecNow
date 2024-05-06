from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class WorkLocation(Base):
    job_id = Column(Integer, ForeignKey("job.id", ondelete="CASCADE"), index=True)
    province_id = Column(Integer, ForeignKey("province.id"), nullable=False)
    district_id = Column(Integer, ForeignKey("district.id"), nullable=True)
    description = Column(Text, nullable=True)

    job = relationship("Job", back_populates="work_locations")
    province = relationship("Province", back_populates="work_location", uselist=False)
    district = relationship("District", back_populates="work_location", uselist=False)
