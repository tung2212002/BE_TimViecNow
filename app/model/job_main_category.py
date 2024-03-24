from sqlalchemy import Column, Integer, ForeignKey

from app.db.base_class import Base


class JobMainCategory(Base):
    job_id = Column(Integer, ForeignKey("job.id"), index=True)
    main_category_id = Column(Integer, ForeignKey("category.id"), index=True)
