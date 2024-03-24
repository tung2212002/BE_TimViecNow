from sqlalchemy import Column, Integer, ForeignKey

from app.db.base_class import Base


class JobSkill(Base):
    job_id = Column(Integer, ForeignKey("job.id"), index=True)
    skill_id = Column(Integer, ForeignKey("skill.id"), index=True)
