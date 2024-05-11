from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class UserJobRequirementPosition(Base):
    user_job_requirement_id = Column(
        Integer, ForeignKey("user_job_requirement.id", ondelete="CASCADE"), index=True
    )
    job_position_id = Column(
        Integer, ForeignKey("job_position.id", ondelete="CASCADE"), index=True
    )

    user_job_requirement = relationship(
        "UserJobRequirement",
        back_populates="user_job_requirement_position",
        overlaps="user_job_requirements",
        single_parent=True,
    )
