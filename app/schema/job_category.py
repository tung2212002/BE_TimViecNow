from pydantic import BaseModel, Field, validator, ConfigDict
from typing import Optional


class JobCategorydBase(BaseModel):
    job_id: int
    category_id: int

    model_config = ConfigDict(from_attribute=True, extra="ignore")


class JobCategoryCreate(JobCategorydBase):
    pass


class JobCategoryCreateRequest(JobCategorydBase):
    pass


class JobCategoryUpdate(JobCategorydBase):
    pass
