from sqlalchemy import Column, Integer, ForeignKey, Enum, String, DateTime
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.hepler.enum import JobApprovalStatus


class ApprovalLog(Base):
    job_approval_request_id = Column(
        Integer, ForeignKey("job_approval_request.id"), index=True
    )
    admin_id = Column(Integer, ForeignKey("admin.id"), index=True)
    previous_status = Column(Enum(JobApprovalStatus), nullable=False, index=True)
    new_status = Column(Enum(JobApprovalStatus), nullable=False, index=True)
    reason = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
