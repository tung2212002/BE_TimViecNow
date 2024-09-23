from pydantic import BaseModel, ConfigDict

from app.hepler.enum import JobSkillType


class JobSkilldBase(BaseModel):
    job_id: int
    skill_id: int
    type: JobSkillType = JobSkillType.MUST_HAVE

    model_config = ConfigDict(from_attribute=True, extra="ignore")


# request
class JobSkillCreateRequest(JobSkilldBase):
    pass


# schema
class JobSkillCreate(JobSkilldBase):
    pass


class JobSkillUpdate(JobSkilldBase):
    pass
