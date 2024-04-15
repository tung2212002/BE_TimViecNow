from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class JobSkill(Base):
    job_id = Column(Integer, ForeignKey("job.id", ondelete="CASCADE"), index=True)
    skill_id = Column(Integer, ForeignKey("skill.id", ondelete="CASCADE"), index=True)
