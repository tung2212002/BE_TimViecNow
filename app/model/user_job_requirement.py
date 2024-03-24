from sqlalchemy import Column, String, ForeignKey, Integer

from app.db.base_class import Base


class UserJobRequirement(Base):
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True, index=True)
    job_salary_id = Column(Integer, ForeignKey("job_salary.id"))
    job_experience_id = Column(Integer, ForeignKey("job_experience.id"))
