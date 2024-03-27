from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class JobWorkingTime(Base):
    job_id = Column(Integer, ForeignKey("job.id"), index=True, nullable=False)
    working_time_id = Column(
        Integer, ForeignKey("working_time.id"), index=True, nullable=False
    )
