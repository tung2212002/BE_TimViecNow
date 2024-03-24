from sqlalchemy import Column, ForeignKey, Integer, String

from app.db.base_class import Base


class UserJobRequirementSkill(Base):
    user_job_requirement_id = Column(
        Integer, ForeignKey("user_job_requirement.id"), index=True
    )
    job_skill_id = Column(Integer, ForeignKey("job_skill.id"), index=True)
