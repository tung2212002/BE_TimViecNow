from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class JobExperience(Base):
    name = Column(String(50), nullable=False)
    slug = Column(String(50), nullable=False)

    user_job_requirement = relationship(
        "UserJobRequirement", back_populates="job_experience"
    )
    job = relationship("Job", back_populates="job_experience")
