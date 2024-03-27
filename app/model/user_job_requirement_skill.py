from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class UserJobRequirementSkill(Base):
    user_job_requirement_id = Column(
        Integer, ForeignKey("user_job_requirement.id", ondelete="CASCADE"), index=True
    )
    skill_id = Column(Integer, ForeignKey("skill.id", ondelete="CASCADE"), index=True)
