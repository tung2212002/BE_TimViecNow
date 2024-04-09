from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GroupPosition(Base):
    name = Column(String(50), nullable=False, index=True)
    slug = Column(String(50), nullable=False, index=True)

    job_positions = relationship(
        "JobPosition", back_populates="group_position", uselist=True
    )
