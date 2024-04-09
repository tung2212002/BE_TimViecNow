from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class JobReport(Base):
    job_id = Column(Integer, ForeignKey("job.id"), index=True)
    user_id = Column(Integer, ForeignKey("user.id"), index=True)
    report_type = Column(String(10), index=True)
    report_content = Column(String(100), index=True)
    report_status = Column(String(10), index=True)
    report_created_at = Column(
        DateTime(timezone=True), index=True, server_default=func.now()
    )
    report_updated_at = Column(
        DateTime(timezone=True),
        index=True,
        server_default=func.now(),
        onupdate=func.now(),
    )

    job = relationship("Job", back_populates="job_reports", uselist=False)
    user = relationship("User", back_populates="job_reports", uselist=False)
