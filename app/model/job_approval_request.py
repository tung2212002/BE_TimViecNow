from sqlalchemy import Column, String, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.hepler.enum import JobStatus


class JobApprovalRequest(Base):
    job_id = Column(Integer, ForeignKey("job.id", ondelete="CASCADE"), index=True)
    representative_id = Column(Integer, ForeignKey("representative.id"), index=True)
    status = Column(
        Enum(JobStatus), nullable=False, index=True, default=JobStatus.PENDING
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    job = relationship("Job", back_populates="job_approval_request", uselist=False)
    representative = relationship(
        "Representative", back_populates="job_approval_request", uselist=False
    )
    approval_log = relationship("ApprovalLog", back_populates="job_approval_request")
