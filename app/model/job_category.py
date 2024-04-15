from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class JobCategory(Base):
    job_id = Column(Integer, ForeignKey("job.id", ondelete="CASCADE"), index=True)
    category_id = Column(
        Integer, ForeignKey("category.id", ondelete="CASCADE"), index=True
    )
