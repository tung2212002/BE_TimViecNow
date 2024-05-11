from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class JobPosition(Base):
    name = Column(String(50), nullable=False)
    slug = Column(String(50), nullable=False)
    count = Column(Integer, default=0)
    group_position_id = Column(Integer, ForeignKey("group_position.id"))

    group_position = relationship(
        "GroupPosition",
        back_populates="job_positions",
        single_parent=True,
    )
