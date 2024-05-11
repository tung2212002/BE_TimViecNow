from sqlalchemy import Column, String, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.hepler.enum import JobApprovalStatus


class JobApprovalRequest(Base):
    job_id = Column(Integer, ForeignKey("job.id", ondelete="CASCADE"), index=True)
    status = Column(
        Enum(JobApprovalStatus),
        nullable=False,
        index=True,
        default=JobApprovalStatus.PENDING,
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), index=True)

    job = relationship(
        "Job",
        back_populates="job_approval_request",
        uselist=False,
    )
    approval_log = relationship("ApprovalLog", back_populates="job_approval_request")
