from sqlalchemy import Column, Integer, ForeignKey

from app.db.base_class import Base


class UserJobRequirementLocation(Base):
    user_job_requirement_id = Column(
        Integer, ForeignKey("user_job_requirement.id"), index=True
    )
    location_id = Column(Integer, ForeignKey("location.id"), index=True)
