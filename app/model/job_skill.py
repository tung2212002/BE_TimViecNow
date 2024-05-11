from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class JobSkill(Base):
    job_id = Column(Integer, ForeignKey("job.id", ondelete="CASCADE"), index=True)
    skill_id = Column(Integer, ForeignKey("skill.id", ondelete="CASCADE"), index=True)

    job = relationship(
        "Job",
        back_populates="job_skill_secondary",
        overlaps="must_have_skills,should_have_skills",
        single_parent=True,
    )

    skill = relationship(
        "Skill",
        back_populates="job_skill_secondary",
        overlaps="must_have_skills,should_have_skills",
        single_parent=True,
    )
