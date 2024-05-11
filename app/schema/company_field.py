from pydantic import BaseModel, ConfigDict


class CompanyFieldBase(BaseModel):
    company_id: int
    field_id: int

    model_config = ConfigDict(from_attribute=True, extra="ignore")


class CompanyFieldCreate(CompanyFieldBase):
    pass


class CompanyFieldCreateRequest(CompanyFieldBase):
    pass


class CompanyFieldUpdate(CompanyFieldBase):
    pass
