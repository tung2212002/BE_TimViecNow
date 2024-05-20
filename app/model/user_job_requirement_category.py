from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


from app.db.base_class import Base


class UserJobRequirementCategory(Base):
    category_id = Column(
        Integer, ForeignKey("category.id", ondelete="CASCADE"), index=True
    )
    user_job_requirement_id = Column(
        Integer, ForeignKey("user_job_requirement.id", ondelete="CASCADE"), index=True
    )

    category = relationship(
        "Category",
        back_populates="user_job_requirement_category",
        overlaps="categories",
    )

    user_job_requirement = relationship(
        "UserJobRequirement",
        back_populates="user_job_requirement_category",
        overlaps="user_job_requirements",
    )
