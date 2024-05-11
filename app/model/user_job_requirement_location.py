from sqlalchemy import Column, Integer, ForeignKey

from app.db.base_class import Base


class UserJobRequirementLocation(Base):
    province_id = Column(
        Integer,
        ForeignKey("province.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    district_id = Column(
        Integer,
        ForeignKey("district.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    user_job_requirement_id = Column(
        Integer, ForeignKey("user_job_requirement.id"), index=True, nullable=False
    )
