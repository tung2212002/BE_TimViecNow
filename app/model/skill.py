from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Skill(Base):
    name = Column(String(50), nullable=False)
    slug = Column(String(50), nullable=False)

    job_skill_secondary = relationship(
        "JobSkill",
        back_populates="skill",
    )

    user_job_requirement_skill = relationship(
        "UserJobRequirementSkill",
        back_populates="skill",
    )
