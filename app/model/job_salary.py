from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class JobSalary(Base):
    id = Column(Integer, primary_key=True, index=True)
    salary = Column(Integer, unique=True, nullable=False)
