from pydantic import BaseModel, ConfigDict


class CompanyBusinessBase(BaseModel):
    company_id: int
    field_id: int

    model_config = ConfigDict(from_attribute=True, extra="ignore")


class CompanyBusinessCreate(CompanyBusinessBase):
    pass


class CompanyBusinessCreateRequest(CompanyBusinessBase):
    pass


class CompanyBusinessUpdate(CompanyBusinessBase):
    pass
