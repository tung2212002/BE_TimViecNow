from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class WorkingTime(Base):
    job_id = Column(Integer, ForeignKey("job.id"))
    ưorking_times = Column(String(255), nullable=False)
