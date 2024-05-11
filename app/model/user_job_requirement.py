from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class UserJobRequirement(Base):
    user_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True, index=True
    )
    job_salary_id = Column(Integer, ForeignKey("job_salary.id"))
    job_experience_id = Column(Integer, ForeignKey("job_experience.id"))

    user = relationship(
        "User",
        back_populates="user_job_requirement",
        uselist=False,
        single_parent=True,
    )
    job_salary = relationship(
        "JobSalary", back_populates="user_job_requirement", uselist=False
    )
    job_experience = relationship(
        "JobExperience", back_populates="user_job_requirement", uselist=False
    )
    job_positions = relationship(
        "JobPosition",
        secondary="user_job_requirement_position",
        overlaps="user_job_requirement",
    )
    province = relationship(
        "Province", secondary="user_job_requirement_location", overlaps="province"
    )
    district = relationship(
        "District",
        secondary="user_job_requirement_location",
        overlaps="district,province",
    )
    skill = relationship(
        "Skill",
        secondary="user_job_requirement_skill",
        overlaps="skill,user_job_requirement_skill,user_job_requirement",
    )
    user_job_requirement_category = relationship(
        "UserJobRequirementCategory",
        back_populates="user_job_requirement",
        overlaps="user_job_requirement,user_job_requirement_skill",
    )
    user_job_requirement_position = relationship(
        "UserJobRequirementPosition",
        back_populates="user_job_requirement",
        overlaps="job_positions",
    )
    user_job_requirement_skill = relationship(
        "UserJobRequirementSkill",
        back_populates="user_job_requirement",
        overlaps="user_job_requirement_skill,skill",
    )
