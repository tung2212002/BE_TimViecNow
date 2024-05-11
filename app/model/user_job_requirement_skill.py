from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class UserJobRequirementSkill(Base):
    user_job_requirement_id = Column(
        Integer, ForeignKey("user_job_requirement.id", ondelete="CASCADE"), index=True
    )
    skill_id = Column(Integer, ForeignKey("skill.id", ondelete="CASCADE"), index=True)

    user_job_requirement = relationship(
        "UserJobRequirement",
        back_populates="user_job_requirement_skill",
        overlaps="user_job_requirements",
    )

    skill = relationship(
        "Skill",
        back_populates="user_job_requirement_skill",
        overlaps="skills",
    )
