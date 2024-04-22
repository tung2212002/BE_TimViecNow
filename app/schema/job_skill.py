from pydantic import BaseModel, Field, validator, ConfigDict
from typing import Optional


class JobSkilldBase(BaseModel):
    job_id: int
    skill_id: int

    model_config = ConfigDict(from_attribute=True, extra="ignore")


class JobSkillCreate(JobSkilldBase):
    pass


class JobSkillCreateRequest(JobSkilldBase):
    pass


class JobSkillUpdate(JobSkilldBase):
    pass
