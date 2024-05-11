from pydantic import BaseModel, ConfigDict


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
