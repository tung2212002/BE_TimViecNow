from sqlalchemy import Column, ForeignKey, Integer

from app.db.base_class import Base


class UserJobRequirementPosition(Base):
    user_job_requirement_id = Column(
        Integer, ForeignKey("user_job_requirement.id"), index=True
    )
    job_position_id = Column(Integer, ForeignKey("job_position.id"), index=True)
