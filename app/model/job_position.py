from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class JobPosition(Base):
    name = Column(String(50), nullable=False)
    slug = Column(String(50), nullable=False)

    job = relationship("Job", back_populates="job_position")
