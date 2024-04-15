from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class UserJobSave(Base):
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), index=True)
    job_id = Column(Integer, ForeignKey("job.id", ondelete="CASCADE"), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )

    user = relationship("User", back_populates="user_job_save", uselist=False)
    job = relationship("Job", back_populates="user_job_save", uselist=False)
