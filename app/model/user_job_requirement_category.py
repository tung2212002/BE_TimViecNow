from sqlalchemy import Column, String, Integer, ForeignKey


from app.db.base_class import Base


class UserJobRequirementCategory(Base):
    category_id = Column(
        Integer, ForeignKey("category.id", ondelete="CASCADE"), index=True
    )
    user_job_requirement_id = Column(
        Integer, ForeignKey("user_job_requirement.id", ondelete="CASCADE"), index=True
    )
