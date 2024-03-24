from sqlalchemy import Column, Integer, ForeignKey

from app.db.base_class import Base


class JobSubCategory(Base):
    job_id = Column(Integer, ForeignKey("job.id"), index=True)
    sub_category_id = Column(Integer, ForeignKey("category.id"), index=True)
