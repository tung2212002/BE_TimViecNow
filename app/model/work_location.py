from sqlalchemy import Column, Integer, ForeignKey, Text, Index
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class WorkLocation(Base):
    job_id = Column(Integer, ForeignKey("job.id", ondelete="CASCADE"), index=True)
    province_id = Column(
        Integer,
        ForeignKey("province.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    district_id = Column(
        Integer,
        ForeignKey("district.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    description = Column(Text, nullable=True)

    job = relationship(
        "Job",
        back_populates="work_locations",
        single_parent=True,
    )
    province = relationship("Province", back_populates="work_location", uselist=False)
    district = relationship("District", back_populates="work_location", uselist=False)

    __table_args__ = (
        Index("idx_work_location_job_id_province_id", job_id, province_id),
    )
