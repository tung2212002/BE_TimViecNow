from sqlalchemy import Column, String, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.hepler.enum import JobStatus


class JobApprovalRequest(Base):
    job_id = Column(Integer, ForeignKey("job.id"), index=True)
    representative_id = Column(Integer, ForeignKey("representative.id"), index=True)
    status = Column(
        Enum(JobStatus), nullable=False, index=True, default=JobStatus.PENDING
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
