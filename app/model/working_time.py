from sqlalchemy import Column, ForeignKey, Integer, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class WorkingTime(Base):
    job_id = Column(Integer, ForeignKey("job.id", ondelete="CASCADE"), index=True)
    start_time = Column(Time, default=func.CURRENT_TIME(), nullable=False)
    end_time = Column(Time, default=func.CURRENT_TIME(), nullable=False)
    date_from = Column(Integer, nullable=False)
    date_to = Column(Integer, nullable=False)

    job = relationship("Job", back_populates="working_times")
